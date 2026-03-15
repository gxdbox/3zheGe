from abc import ABC, abstractmethod
from typing import Optional
import openai
import anthropic
from config.settings import (
    LLM_PROVIDER, OPENAI_API_KEY, ANTHROPIC_API_KEY, LLM_MODEL, LLM_BASE_URL
)


class LLMClient(ABC):
    """LLM客户端基类"""
    
    @abstractmethod
    def generate(self, prompt: str, system: Optional[str] = None, temperature: float = 0.7) -> str:
        """生成文本"""
        pass


class OpenAIClient(LLMClient):
    """OpenAI API客户端（支持OpenAI兼容的API）"""
    
    def __init__(self, api_key: str = OPENAI_API_KEY, model: str = LLM_MODEL, base_url: str = None):
        if not api_key:
            raise ValueError("OPENAI_API_KEY not set")
        
        # 支持自定义base_url（用于兼容其他OpenAI格式的API）
        if base_url:
            self.client = openai.OpenAI(api_key=api_key, base_url=base_url, timeout=30.0)
        else:
            self.client = openai.OpenAI(api_key=api_key, timeout=30.0)
        
        self.model = model
    
    def generate(self, prompt: str, system: Optional[str] = None, temperature: float = 0.7) -> str:
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=2000
        )
        return response.choices[0].message.content


class AnthropicClient(LLMClient):
    """Anthropic API客户端"""
    
    def __init__(self, api_key: str = ANTHROPIC_API_KEY, model: str = "claude-3-opus-20240229"):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model
    
    def generate(self, prompt: str, system: Optional[str] = None, temperature: float = 0.7) -> str:
        response = self.client.messages.create(
            model=self.model,
            max_tokens=2000,
            system=system or "",
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature
        )
        return response.content[0].text


def get_llm_client() -> LLMClient:
    """获取LLM客户端"""
    if LLM_PROVIDER == "anthropic":
        return AnthropicClient()
    else:
        return OpenAIClient(base_url=LLM_BASE_URL)
