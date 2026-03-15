#!/usr/bin/env python3
"""3zhuGe 演示脚本 - 展示系统工作流程"""

import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from db.database import Database
from core.memory import Memory
from core.outline import OutlineManager
from agents.character_agent import CharacterAgent


def demo_workflow():
    """演示完整工作流程"""
    print("\n" + "="*60)
    print("3zhuGe 多Agent小说创作工具 - 演示")
    print("="*60)
    
    # 1. 初始化数据库
    print("\n[1] 初始化项目...")
    db = Database()
    
    project_id = db.create_project(
        name="武侠复仇记",
        genre="武侠",
        tone="热血激昂",
        protagonist_type="废柴逆袭",
        core_conflict="江湖恩怨",
        story_scale="中篇（10-20万字）",
        outline=json.dumps({
            "act1": {
                "name": "起",
                "goal": "主角踏入江湖",
                "must_events": ["师父被杀", "获得遗物", "立下复仇誓言"],
                "forbidden_events": ["主角死亡", "反派被杀"]
            },
            "act2": {
                "name": "承",
                "goal": "主角成长，揭开真相",
                "must_events": ["遇到关键盟友", "发现阴谋", "遭遇重大挫折"],
                "forbidden_events": ["主角放弃复仇"]
            }
        }, ensure_ascii=False)
    )
    print(f"✅ 项目创建成功，ID: {project_id}")
    
    # 2. 创建角色
    print("\n[2] 创建主要角色...")
    characters_data = [
        {
            "name": "李逍遥",
            "gender": "男",
            "age": 20,
            "personality": "正义感强，热血，有点冲动",
            "background": "普通出身，师父被杀",
            "goal": "复仇，成为强者",
            "motivation": "为师父报仇",
            "relationships": {"林月如": "同门", "黑袍人": "仇敌"}
        },
        {
            "name": "林月如",
            "gender": "女",
            "age": 18,
            "personality": "聪慧，温柔，武艺高强",
            "background": "名门之女",
            "goal": "帮助李逍遥",
            "motivation": "同情和爱慕",
            "relationships": {"李逍遥": "同门", "黑袍人": "敌人"}
        },
        {
            "name": "黑袍人",
            "gender": "男",
            "age": 40,
            "personality": "阴谋诡谲，冷酷无情",
            "background": "隐藏身份的反派",
            "goal": "统治江湖",
            "motivation": "权力欲望",
            "relationships": {"李逍遥": "仇敌", "林月如": "对手"}
        }
    ]
    
    for char_data in characters_data:
        char_id = db.create_character(
            project_id=project_id,
            name=char_data["name"],
            gender=char_data["gender"],
            age=char_data["age"],
            personality=char_data["personality"],
            background=char_data["background"],
            goal=char_data["goal"],
            motivation=char_data["motivation"],
            relationships=json.dumps(char_data["relationships"], ensure_ascii=False)
        )
        print(f"  ✅ {char_data['name']} (ID: {char_id})")
    
    # 3. 初始化记忆系统
    print("\n[3] 初始化记忆系统...")
    memory = Memory()
    
    for char_data in characters_data:
        memory.initialize_character_memory(char_data["name"])
    
    # 初始化关系记忆
    memory.initialize_relationship("李逍遥", "林月如")
    memory.initialize_relationship("李逍遥", "黑袍人")
    memory.initialize_relationship("林月如", "黑袍人")
    
    print("✅ 三层记忆系统初始化完成")
    
    # 4. 添加初始事件
    print("\n[4] 记录初始事件...")
    memory.add_world_event("李逍遥的师父被神秘人杀害", chapter=1)
    memory.add_world_event("李逍遥发现师父的遗物", chapter=1)
    memory.add_world_event("李逍遥立下复仇誓言", chapter=1)
    
    memory.add_private_thought("李逍遥", "我一定要找到杀害师父的凶手，为他报仇！")
    memory.add_emotion("李逍遥", "愤怒", 9)
    memory.add_emotion("李逍遥", "悲伤", 8)
    
    print("✅ 初始事件记录完成")
    
    # 5. 初始化大纲
    print("\n[5] 初始化故事大纲...")
    try:
        outline_manager = OutlineManager()
        project = db.get_project(project_id)
        outline = json.loads(project.get("outline", "{}"))
        outline_manager.set_outline(outline)
        
        print("✅ 大纲初始化完成")
        print("\n大纲摘要：")
        print(outline_manager.get_outline_summary())
    except Exception as e:
        print(f"⚠️ 大纲初始化失败: {str(e)}")
        outline_manager = None
    
    # 6. 创建角色Agent
    print("\n[6] 创建角色Agent...")
    character_agents = {}
    for char_data in characters_data:
        agent = CharacterAgent(
            name=char_data["name"],
            personality=char_data["personality"],
            background=char_data["background"],
            goal=char_data["goal"],
            motivation=char_data["motivation"],
            relationships=char_data["relationships"]
        )
        character_agents[char_data["name"]] = agent
        print(f"  ✅ {char_data['name']} Agent 创建成功")
    
    # 7. 演示角色互动
    print("\n[7] 演示角色互动...")
    
    # 李逍遥思考
    print("\n--- 李逍遥的思考 ---")
    li_agent = character_agents["李逍遥"]
    li_agent.set_status("悲痛中")
    li_agent.set_emotion("愤怒")
    li_agent.set_location("破庙")
    
    thought = li_agent.think_about_situation(
        "师父被杀，我在破庙中发现了他的遗物",
        ["林月如", "黑袍人"]
    )
    print(f"李逍遥的想法：{thought[:200]}...")
    
    # 李逍遥决定行动
    print("\n--- 李逍遥的行动 ---")
    action = li_agent.decide_action("我该如何应对这个局面？")
    print(f"行动类型：{action['type']}")
    print(f"行动描述：{action['description'][:200]}...")
    
    # 林月如回应
    print("\n--- 林月如的回应 ---")
    lin_agent = character_agents["林月如"]
    response = lin_agent.respond_to_character("李逍遥", action["description"])
    print(f"林月如的回应：{response[:200]}...")
    
    # 更新关系记忆
    memory.record_interaction("李逍遥", "林月如", f"李逍遥向林月如倾诉了心事")
    memory.update_emotional_temperature("李逍遥", "林月如", 15)
    
    # 8. 显示记忆状态
    print("\n[8] 记忆系统状态...")
    
    world_context = memory.get_world_context()
    print(f"\n世界事件（最近）：")
    for event in world_context["recent_events"][-3:]:
        print(f"  - {event['event']} (第{event['chapter']}章)")
    
    li_memory = memory.get_character_private_memory("李逍遥")
    print(f"\n李逍遥的情感状态：")
    for emotion in li_memory["emotions"][-2:]:
        print(f"  - {emotion['emotion']} (强度: {emotion['intensity']}/10)")
    
    relationship = memory.get_relationship_memory("李逍遥", "林月如")
    print(f"\n李逍遥与林月如的关系：")
    print(f"  情感温度：{relationship['emotional_temperature']}/100")
    print(f"  互动次数：{len(relationship['interaction_history'])}")
    
    # 9. 大纲进度
    print("\n[9] 故事进度...")
    progress = outline_manager.get_outline_progress(current_chapter=1, total_chapters=50)
    print(f"  当前章节：{progress['current_chapter']}")
    print(f"  当前幕：{progress['current_act']}")
    print(f"  幕进度：{progress['act_progress']:.1f}%")
    print(f"  总进度：{progress['overall_progress']:.1f}%")
    
    # 10. 保存章节
    print("\n[10] 保存章节...")
    chapter_content = """
第一章 师父之死

月光如水，洒在破庙的残垣断壁上。李逍遥跪在师父的遗体前，泪水模糊了双眼。

"师父...你为什么要离开我？"

他的声音在空荡荡的庙宇中回荡，却没有人回答。突然，一阵冷风吹过，李逍遥的目光落在了师父身旁的一个布娃娃上——那是师父一直珍藏的遗物。

他颤抖着伸出手，握住了那个布娃娃。在这一刻，一股强大的力量在他心中苏醒。

"我发誓，无论付出什么代价，我都要找到杀害你的凶手，为你报仇！"

李逍遥的声音充满了决心和愤怒。
    """
    
    chapter_id = db.create_chapter(
        project_id=project_id,
        chapter_num=1,
        title="师父之死",
        content=chapter_content,
        word_count=len(chapter_content)
    )
    print(f"✅ 章节保存成功，ID: {chapter_id}")
    
    print("\n" + "="*60)
    print("✅ 演示完成！")
    print("="*60)
    print("\n系统已成功演示以下功能：")
    print("  ✓ 项目和角色管理")
    print("  ✓ 三层记忆系统")
    print("  ✓ 角色Agent互动")
    print("  ✓ 故事大纲管理")
    print("  ✓ 章节保存")
    print("\n下一步：")
    print("  1. 配置 .env 文件中的API密钥")
    print("  2. 运行 streamlit run app.py")
    print("  3. 在Web界面中创建和管理你的小说")


if __name__ == "__main__":
    demo_workflow()
