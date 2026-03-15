from typing import Dict, List, Any
from models.llm_client import get_llm_client


class ConsistencyChecker:
    """一致性检查器"""
    
    def __init__(self):
        self.llm = get_llm_client()
        self.violations = []
    
    def check_character_consistency(self, character_profile: Dict[str, Any], 
                                   action: str) -> Dict[str, Any]:
        """检查角色行为是否符合性格"""
        prompt = f"""
角色设定：
- 名字：{character_profile.get('name')}
- 性格：{character_profile.get('personality')}
- 背景：{character_profile.get('background')}
- 目标：{character_profile.get('goal')}
- 动机：{character_profile.get('motivation')}

拟议行动：{action}

这个行动是否符合角色的性格和设定？
请回答：符合/不符合，并说明原因。
"""
        
        response = self.llm.generate(prompt, temperature=0.5)
        
        is_consistent = "符合" in response
        return {
            "consistent": is_consistent,
            "feedback": response
        }
    
    def check_ability_consistency(self, character_profile: Dict[str, Any], 
                                 action: str) -> Dict[str, Any]:
        """检查角色能力是否足以完成行动"""
        abilities = character_profile.get("abilities", [])
        status = character_profile.get("status", "正常")
        
        prompt = f"""
角色能力：{abilities}
角色状态：{status}

拟议行动：{action}

角色是否有能力完成这个行动？考虑当前状态。
请回答：可以/不可以，并说明原因。
"""
        
        response = self.llm.generate(prompt, temperature=0.5)
        
        is_capable = "可以" in response
        return {
            "capable": is_capable,
            "feedback": response
        }
    
    def check_item_consistency(self, character_items: List[str], 
                              action: str) -> Dict[str, Any]:
        """检查角色是否拥有所需物品"""
        prompt = f"""
角色持有物品：{character_items}

拟议行动：{action}

这个行动是否需要特定的物品？如果需要，角色是否拥有？
请列出所有的物品需求和是否满足。
"""
        
        response = self.llm.generate(prompt, temperature=0.5)
        
        has_items = "满足" in response or "拥有" in response
        return {
            "has_items": has_items,
            "feedback": response
        }
    
    def check_timeline_consistency(self, timeline: List[Dict[str, Any]], 
                                  new_event: str, chapter_num: int) -> Dict[str, Any]:
        """检查时间线一致性"""
        timeline_str = "\n".join([
            f"第{e['chapter']}章：{e['event']}"
            for e in timeline[-10:]  # 最近10个事件
        ])
        
        prompt = f"""
时间线（最近事件）：
{timeline_str}

新事件（第{chapter_num}章）：{new_event}

这个新事件是否与时间线一致？是否违反了已建立的事实？
请检查并说明。
"""
        
        response = self.llm.generate(prompt, temperature=0.5)
        
        is_consistent = "一致" in response
        return {
            "consistent": is_consistent,
            "feedback": response
        }
    
    def check_relationship_consistency(self, relationship_history: List[Dict[str, Any]], 
                                      new_interaction: str) -> Dict[str, Any]:
        """检查关系一致性"""
        history_str = "\n".join([
            f"{e.get('timestamp', '')}: {e.get('interaction', '')}"
            for e in relationship_history[-5:]  # 最近5个互动
        ])
        
        prompt = f"""
互动历史：
{history_str}

新互动：{new_interaction}

这个新互动是否与历史互动一致？是否符合两个角色之间的关系发展？
请检查并说明。
"""
        
        response = self.llm.generate(prompt, temperature=0.5)
        
        is_consistent = "一致" in response
        return {
            "consistent": is_consistent,
            "feedback": response
        }
    
    def check_world_consistency(self, world_settings: Dict[str, Any], 
                               content: str) -> Dict[str, Any]:
        """检查世界观一致性"""
        prompt = f"""
世界设定：{world_settings}

内容：{content}

这段内容是否符合已建立的世界观？
请检查：
1. 是否违反了世界规则？
2. 是否与已有的地点/时间线矛盾？
3. 是否符合社会结构？
"""
        
        response = self.llm.generate(prompt, temperature=0.5)
        
        is_consistent = "符合" in response or "一致" in response
        return {
            "consistent": is_consistent,
            "feedback": response
        }
    
    def validate_action(self, character_profile: Dict[str, Any], 
                       action: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """综合验证行动"""
        checks = {
            "character": self.check_character_consistency(character_profile, action),
            "ability": self.check_ability_consistency(character_profile, action),
            "items": self.check_item_consistency(character_profile.get("items", []), action),
            "timeline": self.check_timeline_consistency(
                context.get("timeline", []), action, context.get("chapter", 0)
            )
        }
        
        all_valid = all(check.get("consistent", check.get("capable", check.get("has_items", False))) 
                       for check in checks.values())
        
        return {
            "valid": all_valid,
            "checks": checks
        }
