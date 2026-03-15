import streamlit as st
from typing import Callable, Dict, Any


class ControlPanel:
    """控制面板"""
    
    def __init__(self):
        self.is_paused = False
        self.generation_speed = 1.0
    
    def show_playback_controls(self) -> Dict[str, Any]:
        """显示播放控制"""
        st.subheader("⏯️ 播放控制")
        
        col1, col2, col3, col4 = st.columns(4)
        
        actions = {}
        
        with col1:
            if st.button("⏸️ 暂停", use_container_width=True):
                actions["pause"] = True
                self.is_paused = True
        
        with col2:
            if st.button("▶️ 继续", use_container_width=True):
                actions["resume"] = True
                self.is_paused = False
        
        with col3:
            if st.button("⏭️ 跳过当前", use_container_width=True):
                actions["skip"] = True
        
        with col4:
            if st.button("🔄 重新生成", use_container_width=True):
                actions["regenerate"] = True
        
        return actions
    
    def show_generation_settings(self) -> Dict[str, Any]:
        """显示生成设置"""
        st.subheader("⚙️ 生成设置")
        
        settings = {}
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**生成速度**")
            speed = st.slider(
                "调整生成速度",
                min_value=0.5,
                max_value=2.0,
                value=1.0,
                step=0.1,
                label_visibility="collapsed"
            )
            settings["speed"] = speed
            self.generation_speed = speed
        
        with col2:
            st.write("**自由度**")
            freedom = st.slider(
                "调整Agent的自由度（0=严格，100=完全自由）",
                min_value=0,
                max_value=100,
                value=50,
                label_visibility="collapsed"
            )
            settings["freedom"] = freedom
        
        st.write("**质量阈值**")
        quality = st.slider(
            "设置最低质量要求（低于此值将重新生成）",
            min_value=0,
            max_value=100,
            value=70,
            label_visibility="collapsed"
        )
        settings["quality_threshold"] = quality
        
        return settings
    
    def show_checkpoint_controls(self) -> Dict[str, Any]:
        """显示检查点控制"""
        st.subheader("💾 检查点管理")
        
        actions = {}
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("💾 保存检查点", use_container_width=True):
                actions["save_checkpoint"] = True
        
        with col2:
            if st.button("📂 加载检查点", use_container_width=True):
                actions["load_checkpoint"] = True
        
        with col3:
            if st.button("🗑️ 删除检查点", use_container_width=True):
                actions["delete_checkpoint"] = True
        
        return actions
    
    def show_editing_tools(self) -> Dict[str, Any]:
        """显示编辑工具"""
        st.subheader("✏️ 编辑工具")
        
        actions = {}
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("✏️ 编辑当前章节", use_container_width=True):
                actions["edit_chapter"] = True
        
        with col2:
            if st.button("🔄 替换当前章节", use_container_width=True):
                actions["replace_chapter"] = True
        
        st.write("**手动编辑内容**")
        manual_edit = st.text_area(
            "在此输入要添加或修改的内容",
            label_visibility="collapsed",
            height=100
        )
        
        if manual_edit:
            actions["manual_edit"] = manual_edit
        
        return actions
    
    def show_debug_panel(self) -> Dict[str, Any]:
        """显示调试面板"""
        with st.expander("🐛 调试面板"):
            st.write("**日志级别**")
            log_level = st.selectbox(
                "选择日志级别",
                ["DEBUG", "INFO", "WARNING", "ERROR"],
                label_visibility="collapsed"
            )
            
            st.write("**显示详细信息**")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                show_prompts = st.checkbox("显示Prompts")
            
            with col2:
                show_tokens = st.checkbox("显示Token使用")
            
            with col3:
                show_timing = st.checkbox("显示执行时间")
            
            return {
                "log_level": log_level,
                "show_prompts": show_prompts,
                "show_tokens": show_tokens,
                "show_timing": show_timing
            }
        
        return {}
    
    def show_quick_actions(self) -> Dict[str, Any]:
        """显示快速操作"""
        st.subheader("⚡ 快速操作")
        
        col1, col2, col3 = st.columns(3)
        
        actions = {}
        
        with col1:
            if st.button("📊 查看统计", use_container_width=True):
                actions["show_stats"] = True
        
        with col2:
            if st.button("🎯 调整大纲", use_container_width=True):
                actions["adjust_outline"] = True
        
        with col3:
            if st.button("👥 管理角色", use_container_width=True):
                actions["manage_characters"] = True
        
        return actions
    
    def show_export_controls(self) -> Dict[str, Any]:
        """显示导出控制"""
        st.subheader("💾 导出选项")
        
        col1, col2, col3 = st.columns(3)
        
        actions = {}
        
        with col1:
            if st.button("📥 导出为TXT", use_container_width=True):
                actions["export_txt"] = True
        
        with col2:
            if st.button("📥 导出为Markdown", use_container_width=True):
                actions["export_markdown"] = True
        
        with col3:
            if st.button("📥 导出为EPUB", use_container_width=True):
                actions["export_epub"] = True
        
        return actions
    
    def show_help_panel(self):
        """显示帮助面板"""
        with st.expander("❓ 帮助"):
            st.write("""
            ### 快速开始
            1. **创建项目** - 选择题材和基调
            2. **确认角色** - 修改自动生成的角色设定
            3. **生成章节** - 点击"生成章节"开始创作
            4. **审阅编辑** - 查看生成的内容，可以编辑或重新生成
            
            ### 常见问题
            - **如何调整故事方向？** - 使用"调整大纲"功能修改情节框架
            - **如何修改角色？** - 在"管理角色"中编辑角色设定
            - **如何导出小说？** - 使用导出选项将内容保存为文件
            
            ### 快捷键
            - `Ctrl+S` - 保存检查点
            - `Ctrl+Z` - 撤销上一步
            - `Ctrl+E` - 导出当前章节
            """)
    
    def show_status_bar(self, status_info: Dict[str, Any]):
        """显示状态栏"""
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("当前章节", status_info.get("current_chapter", 0))
        
        with col2:
            st.metric("总字数", status_info.get("total_words", 0))
        
        with col3:
            st.metric("生成进度", f"{status_info.get('progress', 0)}%")
        
        with col4:
            status = status_info.get("status", "就绪")
            if status == "生成中":
                st.metric("状态", "🔄 " + status)
            elif status == "暂停":
                st.metric("状态", "⏸️ " + status)
            else:
                st.metric("状态", "✅ " + status)
