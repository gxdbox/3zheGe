from typing import Dict, Any, List
from models.llm_client import get_llm_client
from models.prompts import CHAPTER_SUMMARY_PROMPT
import json


class SummaryGenerator:
    """章节摘要生成器"""
    
    def __init__(self):
        self.llm = get_llm_client()
    
    def generate_summary(self, chapter_content: str, chapter_num: int = 0) -> Dict[str, Any]:
        """生成章节摘要"""
        prompt = CHAPTER_SUMMARY_PROMPT.format(chapter_content=chapter_content)
        
        response = self.llm.generate(prompt, temperature=0.6)
        
        try:
            summary = json.loads(response)
        except:
            summary = {
                "core_events": [chapter_content[:100]],
                "character_changes": [],
                "plot_progress": chapter_content[:200],
                "foreshadowing": [],
                "key_dialogue": []
            }
        
        return summary
    
    def compress_chapters(self, chapters: List[Dict[str, Any]], 
                         window_size: int = 3) -> Dict[str, Any]:
        """压缩章节为摘要"""
        compressed = {
            "full_chapters": chapters[-window_size:],
            "summarized_chapters": []
        }
        
        for chapter in chapters[:-window_size]:
            summary = self.generate_summary(
                chapter.get("content", ""),
                chapter.get("chapter_num", 0)
            )
            compressed["summarized_chapters"].append({
                "chapter_num": chapter.get("chapter_num"),
                "summary": summary
            })
        
        return compressed
    
    def extract_key_events(self, chapters: List[Dict[str, Any]]) -> List[str]:
        """提取关键事件"""
        key_events = []
        
        for chapter in chapters:
            summary = chapter.get("summary", {})
            if isinstance(summary, dict):
                events = summary.get("core_events", [])
                key_events.extend(events)
        
        return key_events
    
    def extract_character_arcs(self, chapters: List[Dict[str, Any]]) -> Dict[str, List[str]]:
        """提取角色弧线"""
        character_arcs = {}
        
        for chapter in chapters:
            summary = chapter.get("summary", {})
            if isinstance(summary, dict):
                changes = summary.get("character_changes", {})
                for char, change in changes.items():
                    if char not in character_arcs:
                        character_arcs[char] = []
                    character_arcs[char].append(change)
        
        return character_arcs
    
    def create_reading_guide(self, chapters: List[Dict[str, Any]]) -> str:
        """创建阅读指南"""
        key_events = self.extract_key_events(chapters)
        character_arcs = self.extract_character_arcs(chapters)
        
        guide = "## 故事阅读指南\n\n"
        
        guide += "### 关键事件\n"
        for event in key_events[:10]:
            guide += f"- {event}\n"
        
        guide += "\n### 角色发展\n"
        for char, arc in character_arcs.items():
            guide += f"**{char}**: {' → '.join(arc[:3])}\n"
        
        return guide
