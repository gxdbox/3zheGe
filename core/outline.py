from typing import Dict, List, Any, Optional


class OutlineManager:
    """大纲管理器 - 处理故事框架和约束"""
    
    def __init__(self):
        self.llm = None
        try:
            from models.llm_client import get_llm_client
            self.llm = get_llm_client()
        except ValueError:
            # API密钥未设置，继续使用基础功能
            pass
        
        self.outline = {}
        self.current_act = None
        self.must_events = []
        self.forbidden_events = []
    
    def set_outline(self, outline: Dict[str, Any]):
        """设置大纲"""
        self.outline = outline
        self._extract_constraints()
    
    def _extract_constraints(self):
        """提取约束条件"""
        self.must_events = []
        self.forbidden_events = []
        
        for act_key, act_info in self.outline.items():
            if isinstance(act_info, dict):
                self.must_events.extend(act_info.get("must_events", []))
                self.forbidden_events.extend(act_info.get("forbidden_events", []))
    
    def get_current_act_info(self, chapter_num: int) -> Optional[Dict[str, Any]]:
        """获取当前幕的信息"""
        # 简化版：根据章节数估算当前幕
        if chapter_num <= 10:
            return self.outline.get("act1", {})
        elif chapter_num <= 25:
            return self.outline.get("act2", {})
        elif chapter_num <= 40:
            return self.outline.get("act3", {})
        else:
            return self.outline.get("act4", {})
    
    def check_must_event_completion(self, chapter_num: int) -> Dict[str, Any]:
        """检查必须事件完成情况"""
        act_info = self.get_current_act_info(chapter_num)
        if not act_info:
            return {"completed": [], "pending": []}
        
        must_events = act_info.get("must_events", [])
        
        return {
            "must_events": must_events,
            "total": len(must_events)
        }
    
    def check_forbidden_event_violation(self, proposed_event: str, chapter_num: int) -> Dict[str, Any]:
        """检查是否违反禁止事件"""
        act_info = self.get_current_act_info(chapter_num)
        if not act_info:
            return {"violated": False, "reason": ""}
        
        forbidden_events = act_info.get("forbidden_events", [])
        
        # 简单的文本匹配检查
        for forbidden in forbidden_events:
            if forbidden.lower() in proposed_event.lower():
                return {
                    "violated": True,
                    "reason": f"违反禁止事件：{forbidden}"
                }
        
        return {"violated": False, "reason": ""}
    
    def get_outline_summary(self) -> str:
        """获取大纲摘要"""
        summary = "故事大纲：\n"
        
        for act_key, act_info in self.outline.items():
            if isinstance(act_info, dict):
                summary += f"\n{act_info.get('name', act_key)}：\n"
                summary += f"  目标：{act_info.get('goal', '')}\n"
                
                must_events = act_info.get("must_events", [])
                if must_events:
                    summary += f"  必须事件：{', '.join(must_events)}\n"
                
                forbidden = act_info.get("forbidden_events", [])
                if forbidden:
                    summary += f"  禁止事件：{', '.join(forbidden)}\n"
        
        return summary
    
    def suggest_next_plot_point(self, chapter_num: int, current_context: str) -> str:
        """建议下一个情节点"""
        act_info = self.get_current_act_info(chapter_num)
        
        if not act_info:
            return "无法获取大纲信息"
        
        prompt = f"""
当前章节：{chapter_num}
当前幕信息：{act_info}
当前背景：{current_context}

基于大纲，建议下一个情节点或事件。要求：
1. 符合当前幕的目标
2. 推进故事发展
3. 避免禁止事件
4. 确保必须事件会发生
"""
        
        suggestion = self.llm.generate(prompt, temperature=0.7)
        return suggestion
    
    def validate_chapter_against_outline(self, chapter_content: str, chapter_num: int) -> Dict[str, Any]:
        """验证章节是否符合大纲"""
        act_info = self.get_current_act_info(chapter_num)
        
        if not act_info:
            return {"valid": True, "issues": []}
        
        prompt = f"""
大纲信息：{act_info}

章节内容：{chapter_content[:500]}...

请检查这一章是否符合大纲框架：
1. 是否朝着幕的目标发展？
2. 是否包含了必须事件？
3. 是否违反了禁止事件？
4. 节奏是否合适？

列出所有问题。
"""
        
        validation = self.llm.generate(prompt, temperature=0.5)
        
        has_issues = "问题" in validation or "违反" in validation
        
        return {
            "valid": not has_issues,
            "validation": validation
        }
    
    def get_outline_progress(self, current_chapter: int, total_chapters: int = 100) -> Dict[str, Any]:
        """获取大纲进度"""
        progress_percent = (current_chapter / total_chapters) * 100
        
        # 估算当前所在的幕
        if current_chapter <= 10:
            current_act = "act1"
            act_progress = (current_chapter / 10) * 100
        elif current_chapter <= 25:
            current_act = "act2"
            act_progress = ((current_chapter - 10) / 15) * 100
        elif current_chapter <= 40:
            current_act = "act3"
            act_progress = ((current_chapter - 25) / 15) * 100
        else:
            current_act = "act4"
            act_progress = ((current_chapter - 40) / 60) * 100
        
        return {
            "overall_progress": progress_percent,
            "current_act": current_act,
            "act_progress": act_progress,
            "current_chapter": current_chapter
        }
