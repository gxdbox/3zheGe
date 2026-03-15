import streamlit as st
from typing import List, Dict, Any
from datetime import datetime


class AgentPanel:
    """Agent互动展示面板"""
    
    def __init__(self):
        self.messages = []
    
    def add_message(self, agent_name: str, agent_role: str, message: str, 
                   message_type: str = "thought", avatar: str = "🤖"):
        """添加消息"""
        self.messages.append({
            "agent_name": agent_name,
            "agent_role": agent_role,
            "message": message,
            "type": message_type,
            "avatar": avatar,
            "timestamp": datetime.now().isoformat()
        })
    
    def display_messages(self, container=None):
        """显示消息"""
        if container is None:
            container = st.container()
        
        with container:
            for msg in self.messages:
                self._display_single_message(msg)
    
    def _display_single_message(self, msg: Dict[str, Any]):
        """显示单条消息"""
        avatar_map = {
            "director": "🎬",
            "narrator": "📖",
            "world_builder": "🌍",
            "editor": "✏️",
            "character": "👤"
        }
        
        avatar = avatar_map.get(msg.get("agent_role", "character"), msg.get("avatar", "🤖"))
        
        # 根据消息类型选择颜色和图标
        type_icons = {
            "thought": "💭",
            "action": "⚡",
            "speech": "💬",
            "decision": "🎯",
            "analysis": "🔍",
            "guidance": "👉"
        }
        
        type_icon = type_icons.get(msg.get("type", "thought"), "💭")
        
        with st.chat_message(msg.get("agent_name", "Agent"), avatar=avatar):
            # 消息头
            col1, col2 = st.columns([3, 1])
            with col1:
                st.caption(f"{type_icon} {msg.get('type', '思考')}")
            with col2:
                st.caption(msg.get("timestamp", "")[-8:])
            
            # 消息内容
            st.write(msg.get("message", ""))
    
    def display_agent_status(self, agents_status: Dict[str, str]):
        """显示Agent状态栏"""
        st.divider()
        st.subheader("🤖 Agent状态")
        
        cols = st.columns(len(agents_status))
        for i, (agent_name, status) in enumerate(agents_status.items()):
            with cols[i]:
                # 状态颜色
                if "思考中" in status:
                    status_color = "🟡"
                elif "行动中" in status:
                    status_color = "🔴"
                elif "监控中" in status:
                    status_color = "🟢"
                else:
                    status_color = "⚪"
                
                st.metric(agent_name, status_color, status)
    
    def display_interaction_summary(self, interactions: List[Dict[str, Any]]):
        """显示互动摘要"""
        st.subheader("📊 互动摘要")
        
        if not interactions:
            st.info("暂无互动")
            return
        
        # 统计互动类型
        type_counts = {}
        for interaction in interactions:
            itype = interaction.get("type", "unknown")
            type_counts[itype] = type_counts.get(itype, 0) + 1
        
        # 显示统计
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("总互动数", len(interactions))
        with col2:
            st.metric("涉及角色数", len(set(i.get("character") for i in interactions)))
        with col3:
            st.metric("互动类型", len(type_counts))
        
        # 显示互动列表
        st.write("**互动详情：**")
        for i, interaction in enumerate(interactions[-5:], 1):  # 显示最近5个
            st.write(f"{i}. **{interaction.get('character')}** ({interaction.get('type')})")
            st.caption(interaction.get('content', '')[:100] + "...")
    
    def display_real_time_stream(self, text_stream: str):
        """显示实时流文本"""
        placeholder = st.empty()
        
        with placeholder.container():
            st.write("**实时生成中...**")
            st.code(text_stream, language="text")
    
    def show_agent_thoughts(self, agent_name: str, thoughts: List[str]):
        """显示Agent的思考过程"""
        with st.expander(f"💭 {agent_name}的思考过程"):
            for i, thought in enumerate(thoughts, 1):
                st.write(f"**步骤{i}:**")
                st.write(thought)
                st.divider()
    
    def show_decision_tree(self, decisions: Dict[str, Any]):
        """显示决策树"""
        st.subheader("🎯 决策树")
        
        for agent, decision in decisions.items():
            with st.expander(f"{agent}的决策"):
                st.write(f"**情况分析:**")
                st.write(decision.get("analysis", ""))
                
                st.write(f"**可选方案:**")
                for i, option in enumerate(decision.get("options", []), 1):
                    st.write(f"{i}. {option}")
                
                st.write(f"**最终选择:**")
                st.success(decision.get("choice", ""))
    
    def show_conflict_detection(self, conflicts: List[Dict[str, Any]]):
        """显示冲突检测"""
        if not conflicts:
            st.success("✅ 无冲突检测")
            return
        
        st.warning(f"⚠️ 检测到{len(conflicts)}个潜在冲突")
        
        for conflict in conflicts:
            with st.expander(f"冲突：{conflict.get('type', 'unknown')}"):
                st.write(f"**描述:** {conflict.get('description', '')}")
                st.write(f"**涉及角色:** {', '.join(conflict.get('characters', []))}")
                st.write(f"**建议:** {conflict.get('suggestion', '')}")
    
    def show_agent_memory_preview(self, agent_name: str, memory: Dict[str, Any]):
        """显示Agent记忆预览"""
        with st.expander(f"🧠 {agent_name}的记忆"):
            if "thoughts" in memory:
                st.write("**最近想法:**")
                for thought in memory.get("thoughts", [])[-3:]:
                    st.caption(thought.get("content", "")[:100] + "...")
            
            if "emotions" in memory:
                st.write("**情感状态:**")
                for emotion in memory.get("emotions", [])[-3:]:
                    st.write(f"- {emotion.get('emotion', '')}")
            
            if "secrets" in memory:
                st.write("**秘密:**")
                for secret in memory.get("secrets", []):
                    st.caption(f"🔒 {secret.get('content', '')[:80]}...")
