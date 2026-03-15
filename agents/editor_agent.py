from agents.base_agent import BaseAgent
from models.prompts import EDITOR_SYSTEM
from typing import Dict, Any, List


class EditorAgent(BaseAgent):
    """编辑Agent - 质量把控和文本润色"""
    
    def __init__(self):
        super().__init__(
            name="编辑",
            role="Editor",
            system_prompt=EDITOR_SYSTEM
        )
        self.quality_threshold = 0.7
        self.revision_history = []
    
    def check_quality(self, text: str) -> Dict[str, Any]:
        """检查文本质量"""
        prompt = f"""
        文本内容：
        {text}
        
        请从以下方面评估文本质量（1-10分）：
        1. 可读性（语言流畅度）
        2. 文学性（修辞和意象使用）
        3. 逻辑性（内容连贯性）
        4. 情感表现（情感深度）
        5. 沉浸感（代入感）
        
        给出总体评分和改进建议。
        """
        
        assessment = self.think(prompt, temperature=0.6)
        
        return {
            "assessment": assessment,
            "needs_revision": True  # 默认需要修改
        }
    
    def check_logic(self, text: str, context: str = "") -> Dict[str, Any]:
        """检查逻辑"""
        prompt = f"""
        背景信息：{context}
        
        文本内容：
        {text}
        
        请检查以下逻辑问题：
        1. 是否有自相矛盾的地方？
        2. 因果关系是否合理？
        3. 时间顺序是否正确？
        4. 人物行为是否符合逻辑？
        
        列出所有发现的问题。
        """
        
        check_result = self.think(prompt, temperature=0.5)
        
        has_issues = "问题" in check_result or "矛盾" in check_result
        return {
            "has_issues": has_issues,
            "issues": check_result
        }
    
    def polish_text(self, text: str, focus_areas: List[str] = None) -> str:
        """润色文本"""
        focus = ", ".join(focus_areas) if focus_areas else "整体"
        
        prompt = f"""
        原文：
        {text}
        
        重点润色方向：{focus}
        
        请润色这段文本。要求：
        1. 保留原意
        2. 改进表达质量
        3. 增强文学性
        4. 提升可读性
        5. 长度保持相近
        """
        
        polished = self.think(prompt, temperature=0.7)
        self.revision_history.append({
            "original": text,
            "polished": polished,
            "focus": focus
        })
        return polished
    
    def check_character_consistency(self, character_name: str, 
                                   character_profile: str, 
                                   text: str) -> Dict[str, Any]:
        """检查角色一致性"""
        prompt = f"""
        角色设定：
        {character_profile}
        
        文本中的角色表现：
        {text}
        
        请检查：
        1. 角色的语气和说话方式是否一致？
        2. 角色的行为是否符合性格设定？
        3. 角色的决策是否符合动机？
        4. 是否有OOC（出戏）的地方？
        
        列出所有不一致的地方。
        """
        
        check_result = self.think(prompt, temperature=0.5)
        
        is_consistent = "一致" in check_result
        return {
            "consistent": is_consistent,
            "feedback": check_result
        }
    
    def check_pacing(self, text: str, expected_length: int = 3000) -> Dict[str, Any]:
        """检查节奏"""
        prompt = f"""
        文本内容：
        {text}
        
        预期长度：{expected_length}字
        
        请评估：
        1. 节奏是否合适？
        2. 是否有拖沓的地方？
        3. 是否有跳跃感？
        4. 场景转换是否自然？
        5. 对话与描写的比例是否合理？
        
        给出改进建议。
        """
        
        assessment = self.think(prompt, temperature=0.6)
        
        return {
            "assessment": assessment
        }
    
    def suggest_improvements(self, text: str, aspect: str = "overall") -> List[str]:
        """提出改进建议"""
        prompt = f"""
        文本内容：
        {text}
        
        改进方向：{aspect}
        
        请提出3-5个具体的改进建议。每个建议应该：
        1. 清晰明确
        2. 可操作
        3. 有助于提升质量
        
        格式为列表。
        """
        
        suggestions = self.think(prompt, temperature=0.7)
        
        return suggestions.split("\n")
    
    def final_review(self, chapter_content: str, chapter_num: int) -> Dict[str, Any]:
        """最终审核"""
        prompt = f"""
        第{chapter_num}章内容：
        {chapter_content}
        
        请进行最终审核，包括：
        1. 整体质量评分（1-10）
        2. 是否可以发布？
        3. 如果不能，主要问题是什么？
        4. 关键改进点
        
        返回结构化的审核意见。
        """
        
        review = self.think(prompt, temperature=0.6)
        
        can_publish = "可以发布" in review or "通过" in review
        return {
            "can_publish": can_publish,
            "review": review
        }
    
    def get_revision_history(self) -> List[Dict[str, Any]]:
        """获取修改历史"""
        return self.revision_history
