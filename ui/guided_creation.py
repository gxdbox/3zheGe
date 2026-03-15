import streamlit as st
from typing import Dict, Any, List
from models.llm_client import get_llm_client
from models.prompts import OUTLINE_GENERATION_PROMPT, CHARACTER_GENERATION_PROMPT
import json


class GuidedCreation:
    """引导式创作"""
    
    def __init__(self):
        self.llm = get_llm_client()
    
    def show_mode_selection(self) -> str:
        """显示模式选择"""
        st.subheader("👋 欢迎使用 3zhuGe")
        st.write("选择你的创作模式")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🚀 新手模式（快速开始）", use_container_width=True):
                return "beginner"
        
        with col2:
            if st.button("⚙️ 专家模式（完全自定义）", use_container_width=True):
                return "expert"
        
        return None
    
    def show_beginner_questions(self) -> Dict[str, str]:
        """显示新手模式问题"""
        st.subheader("📝 请回答以下问题")
        st.write("只需3个简单问题，我们就能为你生成故事框架")
        
        responses = {}
        
        # 问题1：题材
        st.write("**1. 你想创作什么题材的小说？**")
        genre = st.radio(
            "选择题材",
            ["武侠", "仙侠", "都市", "科幻", "悬疑", "言情"],
            label_visibility="collapsed"
        )
        responses["genre"] = genre
        
        # 问题2：基调
        st.write("**2. 故事的基调是什么？**")
        tone = st.radio(
            "选择基调",
            ["热血激昂", "阴谋诡谲", "轻松幽默", "悲情沉重"],
            label_visibility="collapsed"
        )
        responses["tone"] = tone
        
        # 问题3：主角类型
        st.write("**3. 主角的成长路线？**")
        protagonist = st.radio(
            "选择主角类型",
            ["废柴逆袭", "天才陨落", "平凡英雄"],
            label_visibility="collapsed"
        )
        responses["protagonist_type"] = protagonist
        
        return responses
    
    def show_expert_questions(self) -> Dict[str, str]:
        """显示专家模式问题"""
        st.subheader("📝 详细创作设置")
        st.write("完整自定义你的故事框架")
        
        responses = {}
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**题材**")
            responses["genre"] = st.selectbox(
                "选择题材",
                ["武侠", "仙侠", "都市", "科幻", "悬疑", "言情", "其他"],
                label_visibility="collapsed"
            )
            
            st.write("**基调**")
            responses["tone"] = st.selectbox(
                "选择基调",
                ["热血激昂", "阴谋诡谲", "轻松幽默", "悲情沉重", "平衡型"],
                label_visibility="collapsed"
            )
        
        with col2:
            st.write("**主角类型**")
            responses["protagonist_type"] = st.selectbox(
                "选择主角类型",
                ["废柴逆袭", "天才陨落", "平凡英雄", "反英雄"],
                label_visibility="collapsed"
            )
            
            st.write("**故事规模**")
            responses["story_scale"] = st.selectbox(
                "选择故事规模",
                ["短篇（3-5万字）", "中篇（10-20万字）", "长篇（50万+）"],
                label_visibility="collapsed"
            )
        
        st.write("**核心冲突**")
        responses["core_conflict"] = st.selectbox(
            "选择核心冲突",
            ["江湖恩怨", "家族复仇", "门派争斗", "正邪对立", "爱恨纠葛"],
            label_visibility="collapsed"
        )
        
        st.write("**故事名称**")
        responses["story_name"] = st.text_input(
            "输入故事名称",
            label_visibility="collapsed"
        )
        
        return responses
    
    def show_template_selection(self) -> Dict[str, Any]:
        """显示预设模板选择"""
        st.subheader("📚 或选择预设模板")
        
        templates = {
            "武侠复仇": {
                "genre": "武侠",
                "tone": "热血激昂",
                "protagonist_type": "废柴逆袭",
                "core_conflict": "江湖恩怨",
                "story_scale": "中篇（10-20万字）"
            },
            "仙侠修行": {
                "genre": "仙侠",
                "tone": "热血激昂",
                "protagonist_type": "天才陨落",
                "core_conflict": "门派争斗",
                "story_scale": "长篇（50万+）"
            },
            "都市爱情": {
                "genre": "都市",
                "tone": "轻松幽默",
                "protagonist_type": "平凡英雄",
                "core_conflict": "爱恨纠葛",
                "story_scale": "中篇（10-20万字）"
            }
        }
        
        col1, col2, col3 = st.columns(3)
        
        selected = None
        with col1:
            if st.button("⚔️ 武侠复仇", use_container_width=True):
                selected = "武侠复仇"
        
        with col2:
            if st.button("✨ 仙侠修行", use_container_width=True):
                selected = "仙侠修行"
        
        with col3:
            if st.button("💕 都市爱情", use_container_width=True):
                selected = "都市爱情"
        
        if selected:
            return templates[selected]
        
        return None
    
    def generate_outline(self, responses: Dict[str, str]) -> Dict[str, Any]:
        """生成大纲"""
        st.info("🤖 正在生成故事大纲...")
        
        prompt = OUTLINE_GENERATION_PROMPT.format(
            genre=responses.get("genre", ""),
            tone=responses.get("tone", ""),
            protagonist_type=responses.get("protagonist_type", ""),
            core_conflict=responses.get("core_conflict", "")
        )
        
        response = self.llm.generate(prompt, temperature=0.7)
        
        try:
            outline = json.loads(response)
        except:
            outline = {
                "act1": {
                    "name": "起",
                    "goal": "故事开端",
                    "must_events": ["主角出场"],
                    "forbidden_events": ["主角死亡"]
                }
            }
        
        st.success("✅ 大纲生成完成！")
        return outline
    
    def generate_characters(self, responses: Dict[str, str], 
                           num_characters: int = 5) -> List[Dict[str, Any]]:
        """生成角色"""
        st.info(f"🤖 正在生成{num_characters}个主要角色...")
        
        prompt = CHARACTER_GENERATION_PROMPT.format(
            genre=responses.get("genre", ""),
            tone=responses.get("tone", ""),
            core_conflict=responses.get("core_conflict", ""),
            story_scale=responses.get("story_scale", ""),
            num_characters=num_characters
        )
        
        response = self.llm.generate(prompt, temperature=0.8)
        
        try:
            characters = json.loads(response)
        except:
            characters = [
                {
                    "name": "主角",
                    "gender": "男",
                    "age": 20,
                    "personality": "正义感强",
                    "background": "普通出身",
                    "goal": "成为强者",
                    "motivation": "复仇",
                    "relationships": {}
                }
            ]
        
        st.success(f"✅ 生成了{len(characters)}个角色！")
        return characters
    
    def show_character_confirmation(self, characters: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """显示角色确认界面"""
        st.subheader("👥 确认角色设定")
        st.write("以下是自动生成的主要角色，你可以修改或删除")
        
        confirmed_characters = []
        
        for i, char in enumerate(characters):
            with st.expander(f"👤 {char.get('name', '角色')} - {char.get('personality', '')}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    name = st.text_input("名字", value=char.get("name", ""), key=f"name_{i}")
                    gender = st.selectbox("性别", ["男", "女"], 
                                         index=0 if char.get("gender") == "男" else 1,
                                         key=f"gender_{i}")
                    age = st.number_input("年龄", value=char.get("age", 20), key=f"age_{i}")
                
                with col2:
                    personality = st.text_area("性格", value=char.get("personality", ""), 
                                              key=f"personality_{i}")
                    background = st.text_area("背景", value=char.get("background", ""), 
                                             key=f"background_{i}")
                
                goal = st.text_input("目标", value=char.get("goal", ""), key=f"goal_{i}")
                motivation = st.text_input("动机", value=char.get("motivation", ""), key=f"motivation_{i}")
                
                keep = st.checkbox("保留此角色", value=True, key=f"keep_{i}")
                
                if keep:
                    confirmed_characters.append({
                        "name": name,
                        "gender": gender,
                        "age": age,
                        "personality": personality,
                        "background": background,
                        "goal": goal,
                        "motivation": motivation,
                        "relationships": char.get("relationships", {})
                    })
        
        return confirmed_characters
    
    def show_relationship_graph(self, characters: List[Dict[str, Any]]):
        """显示角色关系图"""
        st.subheader("🔗 角色关系图")
        
        relationship_text = "角色关系：\n"
        for char in characters:
            relationship_text += f"- {char.get('name')}: {char.get('personality')}\n"
        
        st.text(relationship_text)
        st.info("💡 提示：角色关系将在故事生成过程中动态发展")
