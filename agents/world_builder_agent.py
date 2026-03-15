from agents.base_agent import BaseAgent
from models.prompts import WORLD_BUILDER_SYSTEM
from typing import Dict, Any, List


class WorldBuilderAgent(BaseAgent):
    """世界构建Agent - 管理世界设定和一致性"""
    
    def __init__(self):
        super().__init__(
            name="世界构建者",
            role="WorldBuilder",
            system_prompt=WORLD_BUILDER_SYSTEM
        )
        self.world_settings = {}
        self.timeline = []
        self.locations = {}
    
    def initialize_world(self, genre: str, setting_details: str) -> Dict[str, Any]:
        """初始化世界设定"""
        prompt = f"""
        题材：{genre}
        设定细节：{setting_details}
        
        请为这个故事世界建立基础设定，包括：
        1. 时代背景（古代/现代/未来）
        2. 地理环境（主要地点和地理关系）
        3. 社会结构（权力体系、组织）
        4. 特殊系统（如武功体系、魔法系统等）
        5. 文化习俗（重要的文化特征）
        
        返回JSON格式的详细设定。
        """
        
        world_info = self.think(prompt, temperature=0.7)
        self.world_settings = {"genre": genre, "details": world_info}
        self.remember(f"世界设定已初始化：{genre}", "world_init")
        return self.world_settings
    
    def add_location(self, location_name: str, description: str, 
                    significance: str) -> Dict[str, Any]:
        """添加地点"""
        location_info = {
            "name": location_name,
            "description": description,
            "significance": significance
        }
        self.locations[location_name] = location_info
        self.remember(f"添加地点：{location_name}", "location")
        return location_info
    
    def generate_scene_description(self, location: str, time_of_day: str, 
                                   weather: str, mood: str) -> str:
        """生成场景描写"""
        location_info = self.locations.get(location, {})
        
        prompt = f"""
        地点：{location}
        地点描述：{location_info.get('description', '')}
        
        时间：{time_of_day}
        天气：{weather}
        氛围：{mood}
        
        请生成一段精彩的场景描写（150-200字）。要求：
        1. 符合世界观设定
        2. 营造指定的氛围
        3. 包含具体的环境细节
        4. 为故事的发展奠定基础
        """
        
        scene = self.think(prompt, temperature=0.8)
        return scene
    
    def record_timeline_event(self, chapter_num: int, event: str, 
                             timestamp: str = "") -> None:
        """记录时间线事件"""
        timeline_entry = {
            "chapter": chapter_num,
            "event": event,
            "timestamp": timestamp
        }
        self.timeline.append(timeline_entry)
        self.remember(f"时间线事件：第{chapter_num}章 - {event}", "timeline")
    
    def check_world_consistency(self, new_content: str) -> Dict[str, Any]:
        """检查世界观一致性"""
        world_summary = str(self.world_settings)
        
        prompt = f"""
        当前世界设定：
        {world_summary}
        
        新内容：
        {new_content}
        
        请检查新内容是否符合已建立的世界观：
        1. 是否违反了世界设定？
        2. 是否与已有的地点/时间线矛盾？
        3. 是否符合社会结构和文化习俗？
        4. 特殊系统（如武功体系）的使用是否正确？
        
        如有问题，请指出并建议改进。
        """
        
        check_result = self.think(prompt, temperature=0.5)
        
        is_consistent = "一致" in check_result or "符合" in check_result
        return {
            "consistent": is_consistent,
            "feedback": check_result
        }
    
    def explain_world_rule(self, rule_name: str) -> str:
        """解释世界规则"""
        prompt = f"""
        世界设定：{str(self.world_settings)}
        
        规则名称：{rule_name}
        
        请详细解释这个世界中的"{rule_name}"规则。包括：
        1. 规则的定义
        2. 规则的应用范围
        3. 规则的例外情况
        4. 对故事的影响
        """
        
        explanation = self.think(prompt, temperature=0.7)
        return explanation
    
    def get_location_description(self, location: str) -> str:
        """获取地点描写"""
        if location in self.locations:
            return self.locations[location]["description"]
        
        prompt = f"""
        世界设定：{str(self.world_settings)}
        
        地点：{location}
        
        请为这个地点生成一段详细的描写（100-150字）。
        """
        
        description = self.think(prompt, temperature=0.7)
        self.add_location(location, description, "自动生成")
        return description
    
    def get_timeline(self) -> List[Dict[str, Any]]:
        """获取时间线"""
        return self.timeline
