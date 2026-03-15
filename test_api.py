#!/usr/bin/env python3
"""测试GLM-5 API连接"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from models.llm_client import get_llm_client
from config.settings import LLM_MODEL, LLM_BASE_URL, OPENAI_API_KEY

print("="*60)
print("GLM-5 API 连接测试")
print("="*60)

print(f"\n配置信息：")
print(f"  模型: {LLM_MODEL}")
print(f"  Base URL: {LLM_BASE_URL}")
print(f"  API Key: {OPENAI_API_KEY[:20]}...{OPENAI_API_KEY[-10:]}")

print("\n正在初始化LLM客户端...")
try:
    llm = get_llm_client()
    print("✅ LLM客户端初始化成功")
except Exception as e:
    print(f"❌ LLM客户端初始化失败: {str(e)}")
    sys.exit(1)

print("\n正在测试API调用...")
print("发送测试问题: '你好，请用一句话介绍你自己'")

try:
    response = llm.generate(
        prompt="你好，请用一句话介绍你自己",
        system="你是一个友好的AI助手",
        temperature=0.7
    )
    
    print("\n✅ API调用成功！")
    print(f"\n模型回复：")
    print("-" * 60)
    print(response)
    print("-" * 60)
    
    print(f"\n回复长度: {len(response)} 字符")
    
except Exception as e:
    print(f"\n❌ API调用失败: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "="*60)
print("✅ GLM-5 API 测试通过！")
print("="*60)
print("\n你现在可以正常使用3zhuGe应用了。")
print("运行: python3 -m streamlit run app.py")
