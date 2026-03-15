from typing import Dict, List, Any, Optional
from datetime import datetime
import json


class Memory:
    """三层记忆系统"""
    
    def __init__(self):
        # 第一层：共享世界记忆
        self.world_memory = {
            "timeline": [],
            "current_state": {},
            "events": []
        }
        
        # 第二层：角色独立记忆
        self.private_memories = {}
        
        # 第三层：关系记忆
        self.relationship_memories = {}
    
    def initialize_character_memory(self, character_name: str):
        """初始化角色的私密记忆"""
        self.private_memories[character_name] = {
            "thoughts": [],
            "secrets": [],
            "emotions": [],
            "goals": [],
            "fears": []
        }
    
    def initialize_relationship(self, char1: str, char2: str):
        """初始化两个角色之间的关系记忆"""
        key = tuple(sorted([char1, char2]))
        self.relationship_memories[key] = {
            "interaction_history": [],
            "emotional_temperature": 50,  # 0-100
            "shared_secrets": [],
            "conflicts": [],
            "bonds": []
        }
    
    # 世界记忆操作
    def add_world_event(self, event: str, timestamp: str = None, chapter: int = 0):
        """添加世界事件"""
        if timestamp is None:
            timestamp = datetime.now().isoformat()
        
        event_entry = {
            "event": event,
            "timestamp": timestamp,
            "chapter": chapter
        }
        self.world_memory["events"].append(event_entry)
    
    def update_world_state(self, key: str, value: Any):
        """更新世界状态"""
        self.world_memory["current_state"][key] = value
    
    def get_world_state(self) -> Dict[str, Any]:
        """获取当前世界状态"""
        return self.world_memory["current_state"]
    
    def get_recent_events(self, limit: int = 10) -> List[Dict[str, Any]]:
        """获取最近的事件"""
        return self.world_memory["events"][-limit:]
    
    def get_timeline(self) -> List[Dict[str, Any]]:
        """获取完整时间线"""
        return self.world_memory["timeline"]
    
    # 私密记忆操作
    def add_private_thought(self, character_name: str, thought: str):
        """添加角色的私密想法"""
        if character_name not in self.private_memories:
            self.initialize_character_memory(character_name)
        
        self.private_memories[character_name]["thoughts"].append({
            "content": thought,
            "timestamp": datetime.now().isoformat()
        })
    
    def add_secret(self, character_name: str, secret: str):
        """添加角色的秘密"""
        if character_name not in self.private_memories:
            self.initialize_character_memory(character_name)
        
        self.private_memories[character_name]["secrets"].append({
            "content": secret,
            "timestamp": datetime.now().isoformat(),
            "revealed": False
        })
    
    def add_emotion(self, character_name: str, emotion: str, intensity: int = 5):
        """添加角色的情感"""
        if character_name not in self.private_memories:
            self.initialize_character_memory(character_name)
        
        self.private_memories[character_name]["emotions"].append({
            "emotion": emotion,
            "intensity": intensity,  # 1-10
            "timestamp": datetime.now().isoformat()
        })
    
    def get_character_private_memory(self, character_name: str) -> Dict[str, Any]:
        """获取角色的私密记忆"""
        if character_name not in self.private_memories:
            self.initialize_character_memory(character_name)
        return self.private_memories[character_name]
    
    def get_character_thoughts(self, character_name: str, limit: int = 5) -> List[Dict[str, Any]]:
        """获取角色最近的想法"""
        if character_name not in self.private_memories:
            return []
        return self.private_memories[character_name]["thoughts"][-limit:]
    
    def get_character_secrets(self, character_name: str) -> List[Dict[str, Any]]:
        """获取角色的秘密"""
        if character_name not in self.private_memories:
            return []
        return self.private_memories[character_name]["secrets"]
    
    # 关系记忆操作
    def record_interaction(self, char1: str, char2: str, interaction: str):
        """记录两个角色之间的互动"""
        key = tuple(sorted([char1, char2]))
        if key not in self.relationship_memories:
            self.initialize_relationship(char1, char2)
        
        self.relationship_memories[key]["interaction_history"].append({
            "interaction": interaction,
            "timestamp": datetime.now().isoformat(),
            "initiator": char1
        })
    
    def update_emotional_temperature(self, char1: str, char2: str, change: int):
        """更新两个角色之间的情感温度"""
        key = tuple(sorted([char1, char2]))
        if key not in self.relationship_memories:
            self.initialize_relationship(char1, char2)
        
        current = self.relationship_memories[key]["emotional_temperature"]
        new_temp = max(0, min(100, current + change))
        self.relationship_memories[key]["emotional_temperature"] = new_temp
    
    def get_emotional_temperature(self, char1: str, char2: str) -> int:
        """获取两个角色之间的情感温度"""
        key = tuple(sorted([char1, char2]))
        if key not in self.relationship_memories:
            return 50
        return self.relationship_memories[key]["emotional_temperature"]
    
    def add_shared_secret(self, char1: str, char2: str, secret: str):
        """添加两个角色之间的共享秘密"""
        key = tuple(sorted([char1, char2]))
        if key not in self.relationship_memories:
            self.initialize_relationship(char1, char2)
        
        self.relationship_memories[key]["shared_secrets"].append({
            "secret": secret,
            "timestamp": datetime.now().isoformat()
        })
    
    def get_relationship_memory(self, char1: str, char2: str) -> Dict[str, Any]:
        """获取两个角色之间的关系记忆"""
        key = tuple(sorted([char1, char2]))
        if key not in self.relationship_memories:
            self.initialize_relationship(char1, char2)
        return self.relationship_memories[key]
    
    def get_interaction_history(self, char1: str, char2: str, limit: int = 10) -> List[Dict[str, Any]]:
        """获取两个角色之间的互动历史"""
        key = tuple(sorted([char1, char2]))
        if key not in self.relationship_memories:
            return []
        return self.relationship_memories[key]["interaction_history"][-limit:]
    
    # 上下文组装
    def get_context_for_character(self, character_name: str, 
                                  other_characters: List[str] = None) -> Dict[str, Any]:
        """为特定角色组装上下文"""
        context = {
            "world": self.world_memory,
            "private": self.get_character_private_memory(character_name),
            "relationships": {}
        }
        
        if other_characters:
            for other_char in other_characters:
                context["relationships"][other_char] = self.get_relationship_memory(
                    character_name, other_char
                )
        
        return context
    
    def get_world_context(self) -> Dict[str, Any]:
        """获取世界上下文"""
        return {
            "current_state": self.world_memory["current_state"],
            "recent_events": self.get_recent_events(10),
            "timeline": self.world_memory["timeline"]
        }
    
    # 序列化和持久化
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "world_memory": self.world_memory,
            "private_memories": self.private_memories,
            "relationship_memories": {
                str(k): v for k, v in self.relationship_memories.items()
            }
        }
    
    def to_json(self) -> str:
        """转换为JSON"""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)
    
    def from_dict(self, data: Dict[str, Any]):
        """从字典加载"""
        self.world_memory = data.get("world_memory", self.world_memory)
        self.private_memories = data.get("private_memories", self.private_memories)
        
        # 转换关系记忆的键
        rel_mem = data.get("relationship_memories", {})
        self.relationship_memories = {
            eval(k): v for k, v in rel_mem.items()
        }
    
    def from_json(self, json_str: str):
        """从JSON加载"""
        data = json.loads(json_str)
        self.from_dict(data)
