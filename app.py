import streamlit as st
import json
from typing import Dict, Any
from ui.guided_creation import GuidedCreation
from ui.agent_panel import AgentPanel
from ui.novel_preview import NovelPreview
from ui.control_panel import ControlPanel
from core.story_engine import StoryEngine
from db.database import Database
from config.settings import STREAMLIT_PAGE_TITLE, STREAMLIT_PAGE_ICON

# 页面配置
st.set_page_config(
    page_title=STREAMLIT_PAGE_TITLE,
    page_icon=STREAMLIT_PAGE_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# 初始化session state
if "project_id" not in st.session_state:
    st.session_state.project_id = None
if "story_engine" not in st.session_state:
    st.session_state.story_engine = None
if "current_page" not in st.session_state:
    st.session_state.current_page = "home"
if "view_mode" not in st.session_state:
    st.session_state.view_mode = "read"

# 初始化UI组件
guided_creation = GuidedCreation()
agent_panel = AgentPanel()
novel_preview = NovelPreview()
control_panel = ControlPanel()
db = Database()


def show_home_page():
    """显示主页"""
    st.title("📖 3zhuGe - 多Agent小说创作工具")
    st.write("用AI Agent模拟角色互动，自动生成精彩小说")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🚀 快速开始")
        if st.button("创建新项目", use_container_width=True, key="new_project"):
            st.session_state.current_page = "create"
            st.rerun()
    
    with col2:
        st.subheader("📂 打开项目")
        if st.button("打开现有项目", use_container_width=True, key="open_project"):
            st.session_state.current_page = "open"
            st.rerun()
    
    st.divider()
    
    # 显示功能介绍
    st.subheader("✨ 核心功能")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("**🤖 多Agent协作**")
        st.write("导演、叙事者、世界构建者、编辑和角色Agent协同工作")
    
    with col2:
        st.write("**📖 智能生成**")
        st.write("基于用户选择自动生成大纲、角色和故事内容")
    
    with col3:
        st.write("**🎯 精准控制**")
        st.write("三层控制系统确保故事精彩但不失控")


def show_create_page():
    """显示创建项目页面"""
    st.title("🎬 创建新项目")
    
    # 选择模式
    mode = guided_creation.show_mode_selection()
    
    if mode is None:
        return
    
    st.divider()
    
    # 获取用户输入
    if mode == "beginner":
        responses = guided_creation.show_beginner_questions()
        responses["story_name"] = f"{responses.get('genre', '')}故事"
    else:
        responses = guided_creation.show_expert_questions()
    
    # 显示模板选择
    template = guided_creation.show_template_selection()
    if template:
        responses.update(template)
    
    st.divider()
    
    # 生成大纲和角色
    if st.button("🚀 生成故事框架", use_container_width=True):
        with st.spinner("正在生成..."):
            # 生成大纲
            outline = guided_creation.generate_outline(responses)
            
            # 生成角色
            characters = guided_creation.generate_characters(responses, num_characters=5)
            
            # 保存项目
            project_id = db.create_project(
                name=responses.get("story_name", "新故事"),
                genre=responses.get("genre", ""),
                tone=responses.get("tone", ""),
                protagonist_type=responses.get("protagonist_type", ""),
                core_conflict=responses.get("core_conflict", ""),
                story_scale=responses.get("story_scale", ""),
                outline=json.dumps(outline, ensure_ascii=False)
            )
            
            # 保存角色
            for char in characters:
                db.create_character(
                    project_id=project_id,
                    name=char.get("name", ""),
                    gender=char.get("gender", ""),
                    age=char.get("age", 0),
                    personality=char.get("personality", ""),
                    background=char.get("background", ""),
                    goal=char.get("goal", ""),
                    motivation=char.get("motivation", ""),
                    relationships=json.dumps(char.get("relationships", {}), ensure_ascii=False)
                )
            
            st.session_state.project_id = project_id
            st.session_state.current_page = "confirm"
            st.rerun()


def show_confirm_page():
    """显示确认页面"""
    st.title("👥 确认角色设定")
    
    if st.session_state.project_id is None:
        st.error("项目ID不存在")
        return
    
    # 获取项目和角色信息
    project = db.get_project(st.session_state.project_id)
    characters = db.get_characters(st.session_state.project_id)
    
    st.write(f"**项目:** {project.get('name')}")
    st.write(f"**题材:** {project.get('genre')} | **基调:** {project.get('tone')}")
    
    st.divider()
    
    # 显示角色确认
    char_list = [{"name": c["name"], "gender": c["gender"], "age": c["age"],
                  "personality": c["personality"], "background": c["background"],
                  "goal": c["goal"], "motivation": c["motivation"],
                  "relationships": json.loads(c.get("relationships", "{}")) if isinstance(c.get("relationships"), str) else c.get("relationships", {})}
                 for c in characters]
    
    confirmed_chars = guided_creation.show_character_confirmation(char_list)
    
    st.divider()
    
    # 显示关系图
    guided_creation.show_relationship_graph(confirmed_chars)
    
    st.divider()
    
    # 开始生成
    if st.button("✅ 确认并开始生成", use_container_width=True):
        # 初始化故事引擎
        story_engine = StoryEngine(st.session_state.project_id)
        
        outline = json.loads(project.get("outline", "{}"))
        story_engine.initialize_story(outline, confirmed_chars)
        
        st.session_state.story_engine = story_engine
        st.session_state.current_page = "generate"
        st.rerun()


def show_generate_page():
    """显示生成页面"""
    st.title("📝 故事生成")
    
    if st.session_state.story_engine is None:
        st.error("故事引擎未初始化")
        return
    
    story_engine = st.session_state.story_engine
    
    # 左右分屏
    col_left, col_right = st.columns([1, 1])
    
    with col_left:
        st.subheader("🤖 Agent互动")
        
        # 显示Agent状态
        agents_status = {
            "导演": "监控中",
            "叙事者": "待命",
            "世界构建": "待命",
            "编辑": "待命"
        }
        agent_panel.display_agent_status(agents_status)
        
        st.divider()
        
        # 生成按钮
        if st.button("📝 生成下一章", use_container_width=True):
            with st.spinner("正在生成章节..."):
                chapter_num = story_engine.current_chapter + 1
                result = story_engine.generate_chapter(chapter_num)
                
                # 添加到预览
                novel_preview.add_chapter(
                    chapter_num,
                    f"第{chapter_num}章",
                    result.get("content", "")
                )
                
                # 显示互动
                for interaction in result.get("interactions", []):
                    agent_panel.add_message(
                        interaction.get("character", ""),
                        "character",
                        interaction.get("content", ""),
                        interaction.get("type", "thought")
                    )
                
                st.success("✅ 章节生成完成！")
                st.rerun()
        
        # 显示互动消息
        agent_panel.display_messages()
    
    with col_right:
        st.subheader("📖 小说预览")
        
        if novel_preview.chapters:
            novel_preview.display_chapter_navigation()
            novel_preview.display_current_chapter()
        else:
            st.info("暂无章节内容，点击左侧按钮生成")
    
    st.divider()
    
    # 控制面板
    st.subheader("⚙️ 控制面板")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        control_panel.show_playback_controls()
    
    with col2:
        control_panel.show_checkpoint_controls()
    
    with col3:
        control_panel.show_quick_actions()
    
    st.divider()
    
    # 显示统计
    if novel_preview.chapters:
        novel_preview.display_chapter_stats()
        novel_preview.show_export_options()


def show_open_page():
    """显示打开项目页面"""
    st.title("📂 打开项目")
    
    # 获取所有项目
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, genre, tone, created_at FROM projects ORDER BY created_at DESC")
    projects = cursor.fetchall()
    conn.close()
    
    if not projects:
        st.info("暂无项目")
        return
    
    st.write(f"找到 {len(projects)} 个项目")
    
    for project in projects:
        col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
        
        with col1:
            st.write(f"**{project['name']}**")
            st.caption(f"{project['genre']} | {project['tone']}")
        
        with col2:
            st.caption(project['created_at'][:10])
        
        with col3:
            chapters = db.get_chapters(project['id'])
            st.metric("章节", len(chapters))
        
        with col4:
            if st.button("打开", key=f"open_{project['id']}", use_container_width=True):
                st.session_state.project_id = project['id']
                st.session_state.story_engine = StoryEngine(project['id'])
                st.session_state.current_page = "generate"
                st.rerun()


# 侧边栏
with st.sidebar:
    st.title("🎬 3zhuGe")
    
    if st.session_state.project_id:
        project = db.get_project(st.session_state.project_id)
        st.write(f"**当前项目:** {project.get('name')}")
        st.divider()
    
    page = st.radio(
        "导航",
        ["主页", "创建项目", "打开项目", "生成故事"],
        index=0 if st.session_state.current_page == "home" else 
              1 if st.session_state.current_page == "create" else
              2 if st.session_state.current_page == "open" else 3
    )
    
    if page == "主页":
        st.session_state.current_page = "home"
    elif page == "创建项目":
        st.session_state.current_page = "create"
    elif page == "打开项目":
        st.session_state.current_page = "open"
    elif page == "生成故事":
        st.session_state.current_page = "generate"
    
    st.divider()
    
    # 帮助
    control_panel.show_help_panel()


# 主页面路由
if st.session_state.current_page == "home":
    show_home_page()
elif st.session_state.current_page == "create":
    show_create_page()
elif st.session_state.current_page == "confirm":
    show_confirm_page()
elif st.session_state.current_page == "generate":
    show_generate_page()
elif st.session_state.current_page == "open":
    show_open_page()
else:
    show_home_page()
