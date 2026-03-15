from agents.base_agent import BaseAgent
from models.prompts import DIRECTOR_SYSTEM
from typing import Dict, Any, List


class DirectorAgent(BaseAgent):
    """导演Agent - 把控整体情节走向"""
    
    def __init__(self):
        super().__init__(
            name="导演",
            role="Director",
            system_prompt=DIRECTOR_SYSTEM
        )
        self.outline = None
        self.current_act = None
        self.current_chapter = 0
    
    def set_outline(self, outline: Dict[str, Any]):
        """设置故事大纲"""
        self.outline = outline
        self.remember(f"大纲已设置：{outline}", "outline")
    
    def analyze_current_scene(self, scene_context: str) -> str:
        """分析当前场景"""
        prompt = f"""
        当前场景信息：
        {scene_context}
        
        请分析：
        1. 当前场景是否符合大纲框架？
        2. 需要什么样的冲突或转折？
        3. 应该如何推进情节？
        4. 是否需要引入新的角色或事件？
        """
        analysis = self.think(prompt, temperature=0.7)
        return analysis
    
    def guide_character_action(self, character_name: str, situation: str) -> str:
        """引导角色行动"""
        prompt = f"""
        角色：{character_name}
        当前情况：{situation}
        
        作为导演，你应该如何引导这个角色的行动来推进情节？
        考虑：
        1. 这个角色的性格和目标
        2. 当前的故事节奏
        3. 大纲中的必须事件
        """
        guidance = self.think(prompt, temperature=0.8)
        return guidance
    
    def check_constraint_violation(self, proposed_event: str) -> Dict[str, Any]:
        """检查是否违反约束"""
        if not self.outline or not self.current_act:
            return {"violated": False, "reason": ""}
        
        current_act_info = self.outline.get(self.current_act, {})
        forbidden_events = current_act_info.get("forbidden_events", [])
        
        prompt = f"""
        拟议事件：{proposed_event}
        禁止事件列表：{forbidden_events}
        
        这个事件是否违反了禁止事件的约束？
        请回答：是或否，并说明原因。
        """
        
        response = self.think(prompt, temperature=0.5)
        
        violated = "是" in response or "违反" in response
        return {
            "violated": violated,
            "reason": response
        }
    
    def inject_surprise_event(self, context: str) -> str:
        """注入意外事件"""
        prompt = f"""
        当前故事背景：{context}
        
        设计一个意外事件来增加故事的精彩度，但不违反大纲约束。
        事件应该：
        1. 自然合理
        2. 推动情节发展
        3. 增加冲突
        4. 给角色带来挑战
        """
        event = self.think(prompt, temperature=0.9)
        return event
    
    def assess_pacing(self, chapters_content: List[str]) -> Dict[str, Any]:
        """评估节奏"""
        prompt = f"""
        最近几章的内容摘要：
        {chapters_content}
        
        请评估故事的节奏：
        1. 当前节奏是快还是慢？
        2. 是否需要加快或减速？
        3. 是否有拖沓的地方？
        4. 建议如何调整？
        """
        assessment = self.think(prompt, temperature=0.6)
        return {
            "assessment": assessment
        }
