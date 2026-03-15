#!/usr/bin/env python3
"""基础功能测试脚本"""

import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

from db.database import Database
from agents.base_agent import BaseAgent
from agents.director_agent import DirectorAgent
from agents.narrator_agent import NarratorAgent
from agents.world_builder_agent import WorldBuilderAgent
from agents.editor_agent import EditorAgent
from agents.character_agent import CharacterAgent
from core.memory import Memory
from models.llm_client import get_llm_client


def test_database():
    """测试数据库"""
    print("\n=== 测试数据库 ===")
    db = Database()
    
    # 创建项目
    project_id = db.create_project(
        name="测试项目",
        genre="武侠",
        tone="热血激昂",
        protagonist_type="废柴逆袭",
        core_conflict="江湖恩怨",
        story_scale="中篇",
        outline='{"act1": "起"}'
    )
    print(f"✅ 创建项目成功，ID: {project_id}")
    
    # 获取项目
    project = db.get_project(project_id)
    print(f"✅ 获取项目成功: {project['name']}")
    
    # 创建角色
    char_id = db.create_character(
        project_id=project_id,
        name="李逍遥",
        gender="男",
        age=20,
        personality="正义感强，热血",
        background="普通出身",
        goal="成为强者",
        motivation="复仇",
        relationships='{}'
    )
    print(f"✅ 创建角色成功，ID: {char_id}")
    
    # 获取角色
    characters = db.get_characters(project_id)
    print(f"✅ 获取角色成功，共{len(characters)}个")
    
    return project_id


def test_agents():
    """测试Agent"""
    print("\n=== 测试Agent ===")
    
    try:
        # 测试导演Agent
        director = DirectorAgent()
        print(f"✅ 导演Agent初始化成功: {director}")
        
        # 测试叙事Agent
        narrator = NarratorAgent()
        narrator.set_style("文学性", "热血")
        print(f"✅ 叙事Agent初始化成功: {narrator}")
        
        # 测试世界构建Agent
        world_builder = WorldBuilderAgent()
        print(f"✅ 世界构建Agent初始化成功: {world_builder}")
        
        # 测试编辑Agent
        editor = EditorAgent()
        print(f"✅ 编辑Agent初始化成功: {editor}")
        
        # 测试角色Agent
        character = CharacterAgent(
            name="李逍遥",
            personality="正义感强，热血",
            background="普通出身",
            goal="成为强者",
            motivation="复仇",
            relationships={"林月如": "同门"}
        )
        print(f"✅ 角色Agent初始化成功: {character}")
        
        return director, narrator, world_builder, editor, character
    
    except ValueError as e:
        print(f"⚠️ Agent初始化失败: {str(e)}")
        print("   请在 .env 文件中设置 OPENAI_API_KEY 或 ANTHROPIC_API_KEY")
        return None, None, None, None, None


def test_memory():
    """测试记忆系统"""
    print("\n=== 测试记忆系统 ===")
    
    memory = Memory()
    
    # 初始化角色记忆
    memory.initialize_character_memory("李逍遥")
    memory.initialize_character_memory("林月如")
    print("✅ 角色记忆初始化成功")
    
    # 添加世界事件
    memory.add_world_event("主角踏入江湖", chapter=1)
    memory.add_world_event("遇到女主角", chapter=2)
    print("✅ 世界事件添加成功")
    
    # 添加私密想法
    memory.add_private_thought("李逍遥", "我要变强，复仇")
    memory.add_emotion("李逍遥", "愤怒", 8)
    print("✅ 私密记忆添加成功")
    
    # 初始化关系记忆
    memory.initialize_relationship("李逍遥", "林月如")
    memory.record_interaction("李逍遥", "林月如", "初次相遇")
    memory.update_emotional_temperature("李逍遥", "林月如", 20)
    print("✅ 关系记忆添加成功")
    
    # 获取上下文
    context = memory.get_context_for_character("李逍遥", ["林月如"])
    print(f"✅ 获取角色上下文成功")
    
    return memory


def test_llm_client():
    """测试LLM客户端"""
    print("\n=== 测试LLM客户端 ===")
    
    try:
        llm = get_llm_client()
        print(f"✅ LLM客户端初始化成功: {type(llm).__name__}")
        
        # 测试生成
        print("⏳ 测试LLM生成（这可能需要一些时间）...")
        response = llm.generate(
            prompt="用一句话描述武侠小说的特点",
            system="你是一个文学评论家",
            temperature=0.7
        )
        print(f"✅ LLM生成成功: {response[:100]}...")
        
    except Exception as e:
        print(f"⚠️ LLM测试失败: {str(e)}")
        print("   请确保已设置正确的API密钥")


def main():
    """主测试函数"""
    print("🧪 3zhuGe 基础功能测试")
    print("=" * 50)
    
    try:
        # 测试数据库
        project_id = test_database()
        
        # 测试Agent
        test_agents()
        
        # 测试记忆系统
        test_memory()
        
        # 测试LLM客户端
        test_llm_client()
        
        print("\n" + "=" * 50)
        print("✅ 所有基础测试完成！")
        print("\n下一步：")
        print("1. 配置 .env 文件中的API密钥")
        print("2. 运行: streamlit run app.py")
        print("3. 在浏览器中打开应用")
        
    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
