from agents.base_agent import BaseAgent
from models.prompts import NARRATOR_SYSTEM
from typing import Dict, Any, List


class NarratorAgent(BaseAgent):
    """叙事Agent - 将互动转化为小说文本"""
    
    def __init__(self):
        super().__init__(
            name="叙事者",
            role="Narrator",
            system_prompt=NARRATOR_SYSTEM
        )
        self.writing_style = "文学性"
        self.tone = "中立"
    
    def set_style(self, style: str, tone: str):
        """设置写作风格"""
        self.writing_style = style
        self.tone = tone
        self.remember(f"风格设置：{style}，基调：{tone}", "style")
    
    def transform_interaction(self, interactions: List[Dict[str, str]], 
                             scene_description: str = "") -> str:
        """将角色互动转化为小说文本"""
        interaction_text = "\n".join([
            f"{item['character']}: {item['action']}"
            for item in interactions
        ])
        
        prompt = f"""
        场景描述：{scene_description}
        
        角色互动记录：
        {interaction_text}
        
        请将这些互动转化为精彩的小说段落。要求：
        1. 运用文学手法（展示而非告知）
        2. 添加环境描写和心理描写
        3. 保持文风一致，基调为：{self.tone}
        4. 长度约500-800字
        5. 营造沉浸感和戏剧张力
        """
        
        narrative = self.think(prompt, temperature=0.8)
        self.remember(f"转化了{len(interactions)}个互动", "transformation")
        return narrative
    
    def enhance_description(self, basic_description: str) -> str:
        """增强描写"""
        prompt = f"""
        基础描写：{basic_description}
        
        请用更文学、更生动的语言重写这段描写。要求：
        1. 使用具体的意象和修辞手法
        2. 营造氛围和情感
        3. 保持原意，但更加精彩
        4. 长度保持相近
        """
        
        enhanced = self.think(prompt, temperature=0.8)
        return enhanced
    
    def generate_chapter_opening(self, chapter_num: int, chapter_theme: str) -> str:
        """生成章节开头"""
        prompt = f"""
        第{chapter_num}章
        章节主题：{chapter_theme}
        
        请生成一个精彩的章节开头（100-150字）。要求：
        1. 吸引读者注意力
        2. 暗示本章的主要内容
        3. 与前一章形成自然衔接
        4. 基调为：{self.tone}
        """
        
        opening = self.think(prompt, temperature=0.8)
        return opening
    
    def generate_chapter_ending(self, chapter_num: int, chapter_summary: str) -> str:
        """生成章节结尾"""
        prompt = f"""
        第{chapter_num}章
        章节内容摘要：{chapter_summary}
        
        请生成一个精彩的章节结尾（100-150字）。要求：
        1. 总结本章的关键发展
        2. 为下一章埋下悬念
        3. 给读者留下深刻印象
        4. 基调为：{self.tone}
        """
        
        ending = self.think(prompt, temperature=0.8)
        return ending
    
    def add_internal_monologue(self, character_name: str, 
                              character_state: str, situation: str) -> str:
        """添加内心独白"""
        prompt = f"""
        角色：{character_name}
        角色状态：{character_state}
        当前情况：{situation}
        
        请为这个角色写一段内心独白（50-100字）。要求：
        1. 反映角色的真实想法和感受
        2. 符合角色的性格和语气
        3. 增加读者对角色的理解
        4. 自然融入故事
        """
        
        monologue = self.think(prompt, temperature=0.8)
        return monologue
    
    def check_consistency(self, text: str, previous_text: str = "") -> Dict[str, Any]:
        """检查文本一致性"""
        prompt = f"""
        前文：{previous_text}
        
        新文本：{text}
        
        请检查新文本是否与前文保持一致：
        1. 文风是否一致？
        2. 基调是否一致？
        3. 是否有逻辑矛盾？
        4. 人物性格是否一致？
        
        如有问题，请指出并建议改进。
        """
        
        check_result = self.think(prompt, temperature=0.5)
        return {
            "consistent": "一致" in check_result,
            "feedback": check_result
        }
