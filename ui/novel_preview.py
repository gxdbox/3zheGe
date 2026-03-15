import streamlit as st
from typing import List, Dict, Any


class NovelPreview:
    """小说预览面板"""
    
    def __init__(self):
        self.chapters = []
        self.current_chapter = 0
    
    def add_chapter(self, chapter_num: int, title: str, content: str):
        """添加章节"""
        self.chapters.append({
            "num": chapter_num,
            "title": title,
            "content": content
        })
    
    def display_current_chapter(self, chapter_num: int = None):
        """显示当前章节"""
        if chapter_num is None:
            chapter_num = self.current_chapter
        
        # 找到对应章节
        chapter = None
        for ch in self.chapters:
            if ch["num"] == chapter_num:
                chapter = ch
                break
        
        if not chapter:
            st.info("暂无章节内容")
            return
        
        # 显示章节标题
        st.title(f"📖 {chapter['title']}")
        
        # 显示章节信息
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("章节", f"第{chapter['num']}章")
        with col2:
            st.metric("字数", len(chapter['content']))
        with col3:
            st.metric("阅读时间", f"{len(chapter['content']) // 300}分钟")
        
        st.divider()
        
        # 显示内容
        st.write(chapter['content'])
    
    def display_chapter_navigation(self):
        """显示章节导航"""
        st.subheader("📚 章节导航")
        
        if not self.chapters:
            st.info("暂无章节")
            return
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("⬅️ 上一章"):
                if self.current_chapter > 0:
                    self.current_chapter -= 1
                    st.rerun()
        
        with col2:
            chapter_options = [f"第{ch['num']}章: {ch['title']}" for ch in self.chapters]
            selected = st.selectbox(
                "选择章节",
                range(len(self.chapters)),
                format_func=lambda i: chapter_options[i],
                label_visibility="collapsed"
            )
            self.current_chapter = selected
        
        with col3:
            if st.button("下一章 ➡️"):
                if self.current_chapter < len(self.chapters) - 1:
                    self.current_chapter += 1
                    st.rerun()
        
        # 显示进度
        progress = (self.current_chapter + 1) / len(self.chapters)
        st.progress(progress)
    
    def display_chapter_list(self):
        """显示章节列表"""
        st.subheader("📖 已生成章节")
        
        if not self.chapters:
            st.info("暂无章节")
            return
        
        for chapter in self.chapters:
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.write(f"**第{chapter['num']}章: {chapter['title']}**")
            
            with col2:
                st.caption(f"{len(chapter['content'])}字")
            
            with col3:
                if st.button("查看", key=f"view_{chapter['num']}"):
                    self.current_chapter = chapter['num'] - 1
                    st.rerun()
    
    def display_chapter_stats(self):
        """显示章节统计"""
        st.subheader("📊 统计信息")
        
        if not self.chapters:
            st.info("暂无数据")
            return
        
        total_words = sum(len(ch['content']) for ch in self.chapters)
        avg_words = total_words // len(self.chapters) if self.chapters else 0
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("总章数", len(self.chapters))
        
        with col2:
            st.metric("总字数", total_words)
        
        with col3:
            st.metric("平均字数", avg_words)
        
        with col4:
            st.metric("预计阅读时间", f"{total_words // 300}小时")
    
    def display_chapter_outline(self):
        """显示章节大纲"""
        st.subheader("📋 章节大纲")
        
        if not self.chapters:
            st.info("暂无章节")
            return
        
        outline_text = ""
        for chapter in self.chapters:
            outline_text += f"第{chapter['num']}章 {chapter['title']}\n"
        
        st.text(outline_text)
    
    def export_chapter(self, chapter_num: int, format: str = "txt") -> str:
        """导出章节"""
        chapter = None
        for ch in self.chapters:
            if ch["num"] == chapter_num:
                chapter = ch
                break
        
        if not chapter:
            return ""
        
        if format == "txt":
            return self._export_as_txt(chapter)
        elif format == "markdown":
            return self._export_as_markdown(chapter)
        
        return ""
    
    def _export_as_txt(self, chapter: Dict[str, Any]) -> str:
        """导出为TXT格式"""
        return f"{chapter['title']}\n\n{chapter['content']}"
    
    def _export_as_markdown(self, chapter: Dict[str, Any]) -> str:
        """导出为Markdown格式"""
        return f"# {chapter['title']}\n\n{chapter['content']}"
    
    def export_all_chapters(self, format: str = "txt") -> str:
        """导出所有章节"""
        if format == "txt":
            content = ""
            for chapter in self.chapters:
                content += f"\n{'='*50}\n"
                content += f"{chapter['title']}\n"
                content += f"{'='*50}\n\n"
                content += chapter['content']
                content += "\n\n"
            return content
        
        elif format == "markdown":
            content = "# 小说全文\n\n"
            for chapter in self.chapters:
                content += f"## {chapter['title']}\n\n"
                content += chapter['content']
                content += "\n\n"
            return content
        
        return ""
    
    def show_reading_mode(self):
        """显示阅读模式"""
        st.subheader("📖 阅读模式")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📄 列表视图", use_container_width=True):
                st.session_state.view_mode = "list"
        
        with col2:
            if st.button("📖 阅读视图", use_container_width=True):
                st.session_state.view_mode = "read"
        
        with col3:
            if st.button("📊 统计视图", use_container_width=True):
                st.session_state.view_mode = "stats"
        
        # 根据模式显示内容
        if st.session_state.get("view_mode") == "list":
            self.display_chapter_list()
        elif st.session_state.get("view_mode") == "read":
            self.display_chapter_navigation()
            self.display_current_chapter()
        elif st.session_state.get("view_mode") == "stats":
            self.display_chapter_stats()
            self.display_chapter_outline()
    
    def show_export_options(self):
        """显示导出选项"""
        st.subheader("💾 导出选项")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📥 导出为TXT", use_container_width=True):
                content = self.export_all_chapters("txt")
                st.download_button(
                    label="下载TXT文件",
                    data=content,
                    file_name="novel.txt",
                    mime="text/plain"
                )
        
        with col2:
            if st.button("📥 导出为Markdown", use_container_width=True):
                content = self.export_all_chapters("markdown")
                st.download_button(
                    label="下载Markdown文件",
                    data=content,
                    file_name="novel.md",
                    mime="text/markdown"
                )
