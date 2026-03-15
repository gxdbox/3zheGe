from agents.base_agent import BaseAgent
from models.prompts import CHARACTER_THINK_PROMPT, CHARACTER_ACT_PROMPT
from typing import Dict, Any, Optional


class CharacterAgent(BaseAgent):
    """角色Agent - 动态生成的角色"""
    
    def __init__(self, name: str, personality: str, background: str, 
                 goal: str, motivation: str, relationships: Dict[str, str]):
        system_prompt = f"""你是小说中的角色：{name}

性格特点：{personality}
背景故事：{background}
目标：{goal}
动机：{motivation}

你应该根据自己的性格、背景和目标来思考和行动。"""
        
        super().__init__(
            name=name,
            role="Character",
            system_prompt=system_prompt
        )
        
        self.personality = personality
        self.background = background
        self.goal = goal
        self.motivation = motivation
        self.relationships = relationships
        
        self.status = "正常"
        self.current_location = ""
        self.current_emotion = ""
        self.abilities = []
        self.items = []
        self.secrets = []
    
    def think_about_situation(self, scene_context: str, other_characters: list = None) -> str:
        """思考当前情况"""
        other_chars_info = ""
        if other_characters:
            other_chars_info = "\n".join([
                f"- {char}: {self.relationships.get(char, '陌生人')}"
                for char in other_characters
            ])
        
        prompt = f"""
场景信息：{scene_context}

其他角色：
{other_chars_info}

根据你的性格、背景和当前处境，深入思考：
1. 你的真实想法和感受
2. 你对这个情况的理解
3. 你的动机和目标如何影响你的反应
4. 你对其他角色的看法
5. 你可能采取的行动方向

用第一人称深入思考，不要过于简短。
"""
        
        thought = self.think(prompt, temperature=0.8)
        self.remember(f"思考了情况：{scene_context[:50]}", "thought")
        return thought
    
    def decide_action(self, situation: str, options: list = None) -> Dict[str, str]:
        """决定行动"""
        options_text = ""
        if options:
            options_text = "\n".join([f"- {opt}" for opt in options])
        
        prompt = f"""
当前情况：{situation}

可选行动：
{options_text}

基于你的思考，你将采取什么行动？

行动类型可以是：
1. 说话 - 与其他角色对话
2. 行动 - 做出具体的行为
3. 反应 - 对他人的行为做出反应
4. 决策 - 做出重要的选择

请明确描述你的行动，包括具体的对话或行为描述。
"""
        
        action_response = self.think(prompt, temperature=0.8)
        
        # 解析行动
        action_type = "未知"
        if "说" in action_response or "话" in action_response:
            action_type = "说话"
        elif "行动" in action_response or "做" in action_response:
            action_type = "行动"
        elif "反应" in action_response:
            action_type = "反应"
        elif "决定" in action_response or "选择" in action_response:
            action_type = "决策"
        
        self.remember(f"采取了{action_type}：{action_response[:50]}", "action")
        
        return {
            "type": action_type,
            "description": action_response
        }
    
    def respond_to_character(self, other_character: str, message: str) -> str:
        """回应其他角色"""
        relationship = self.relationships.get(other_character, "陌生人")
        
        prompt = f"""
{other_character}对你说："{message}"

你与{other_character}的关系：{relationship}

请用符合你性格的方式回应。考虑：
1. 你对这个人的感受
2. 这句话对你的影响
3. 你的真实想法
4. 你的回应方式

直接给出你的回应，不需要额外说明。
"""
        
        response = self.think(prompt, temperature=0.8)
        self.remember(f"回应了{other_character}", "interaction")
        return response
    
    def update_relationship(self, other_character: str, change: str):
        """更新与其他角色的关系"""
        current = self.relationships.get(other_character, "陌生人")
        self.relationships[other_character] = f"{current} -> {change}"
        self.remember(f"与{other_character}的关系改变：{change}", "relationship")
    
    def set_status(self, status: str):
        """设置角色状态"""
        self.status = status
        self.remember(f"状态改变：{status}", "status")
    
    def set_emotion(self, emotion: str):
        """设置情感状态"""
        self.current_emotion = emotion
        self.remember(f"情感状态：{emotion}", "emotion")
    
    def set_location(self, location: str):
        """设置位置"""
        self.current_location = location
        self.remember(f"位置：{location}", "location")
    
    def add_ability(self, ability: str):
        """添加能力"""
        if ability not in self.abilities:
            self.abilities.append(ability)
            self.remember(f"获得能力：{ability}", "ability")
    
    def add_item(self, item: str):
        """获得物品"""
        if item not in self.items:
            self.items.append(item)
            self.remember(f"获得物品：{item}", "item")
    
    def remove_item(self, item: str):
        """失去物品"""
        if item in self.items:
            self.items.remove(item)
            self.remember(f"失去物品：{item}", "item")
    
    def add_secret(self, secret: str):
        """添加秘密"""
        self.secrets.append(secret)
        self.remember(f"秘密：{secret}", "secret")
    
    def get_profile(self) -> Dict[str, Any]:
        """获取角色档案"""
        return {
            "name": self.name,
            "personality": self.personality,
            "background": self.background,
            "goal": self.goal,
            "motivation": self.motivation,
            "relationships": self.relationships,
            "status": self.status,
            "location": self.current_location,
            "emotion": self.current_emotion,
            "abilities": self.abilities,
            "items": self.items,
            "secrets": self.secrets
        }
    
    def __repr__(self) -> str:
        return f"角色({self.name}) - {self.status}"
