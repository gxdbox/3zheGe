from abc import ABC, abstractmethod
from typing import Optional, Dict, Any


class BaseAgent(ABC):
    """Agent基类"""
    
    def __init__(self, name: str, role: str, system_prompt: str):
        self.name = name
        self.role = role
        self.system_prompt = system_prompt
        self.llm = None
        try:
            from models.llm_client import get_llm_client
            self.llm = get_llm_client()
        except ValueError:
            # API密钥未设置，继续使用基础功能
            pass
        self.memory = []
    
    def think(self, context: str, temperature: float = 0.7) -> str:
        """思考"""
        if self.llm:
            response = self.llm.generate(
                prompt=context,
                system=self.system_prompt,
                temperature=temperature
            )
        else:
            # 演示模式：返回模拟响应
            response = f"[演示模式] {self.name}在思考：{context[:100]}..."
        
        self.memory.append({
            "type": "thought",
            "content": response
        })
        return response
    
    def speak(self, message: str) -> str:
        """发言"""
        self.memory.append({
            "type": "speech",
            "content": message
        })
        return message
    
    def act(self, action: str) -> str:
        """行动"""
        self.memory.append({
            "type": "action",
            "content": action
        })
        return action
    
    def remember(self, event: str, event_type: str = "event"):
        """记忆"""
        self.memory.append({
            "type": event_type,
            "content": event
        })
    
    def get_memory(self, limit: int = 10) -> list:
        """获取最近的记忆"""
        return self.memory[-limit:]
    
    def clear_memory(self):
        """清空记忆"""
        self.memory = []
    
    def __repr__(self) -> str:
        return f"{self.role}({self.name})"
