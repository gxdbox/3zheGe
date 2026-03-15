from typing import Dict, List, Any, Optional
from agents.director_agent import DirectorAgent
from agents.narrator_agent import NarratorAgent
from agents.world_builder_agent import WorldBuilderAgent
from agents.editor_agent import EditorAgent
from agents.character_agent import CharacterAgent
from core.memory import Memory
from db.database import Database
import json


class StoryEngine:
    """故事引擎 - 协调各Agent生成故事"""
    
    def __init__(self, project_id: int):
        self.project_id = project_id
        self.db = Database()
        self.memory = Memory()
        
        # 初始化固定Agent
        self.director = DirectorAgent()
        self.narrator = NarratorAgent()
        self.world_builder = WorldBuilderAgent()
        self.editor = EditorAgent()
        
        # 动态角色Agent
        self.characters: Dict[str, CharacterAgent] = {}
        
        # 故事状态
        self.current_chapter = 0
        self.outline = None
        self.project_info = None
        
        self._load_project()
    
    def _load_project(self):
        """加载项目信息"""
        self.project_info = self.db.get_project(self.project_id)
        if self.project_info and self.project_info.get("outline"):
            try:
                self.outline = json.loads(self.project_info["outline"])
            except:
                self.outline = None
    
    def initialize_story(self, outline: Dict[str, Any], characters: List[Dict[str, Any]]):
        """初始化故事"""
        self.outline = outline
        self.director.set_outline(outline)
        
        # 初始化世界
        genre = self.project_info.get("genre", "")
        setting = self.project_info.get("core_conflict", "")
        self.world_builder.initialize_world(genre, setting)
        
        # 创建角色Agent
        for char_info in characters:
            self.create_character_agent(char_info)
        
        # 初始化记忆
        for char_name in self.characters.keys():
            self.memory.initialize_character_memory(char_name)
        
        for char1 in self.characters.keys():
            for char2 in self.characters.keys():
                if char1 < char2:
                    self.memory.initialize_relationship(char1, char2)
    
    def create_character_agent(self, char_info: Dict[str, Any]) -> CharacterAgent:
        """创建角色Agent"""
        name = char_info.get("name", "")
        personality = char_info.get("personality", "")
        background = char_info.get("background", "")
        goal = char_info.get("goal", "")
        motivation = char_info.get("motivation", "")
        relationships = char_info.get("relationships", {})
        
        agent = CharacterAgent(
            name=name,
            personality=personality,
            background=background,
            goal=goal,
            motivation=motivation,
            relationships=relationships
        )
        
        self.characters[name] = agent
        return agent
    
    def generate_chapter(self, chapter_num: int) -> Dict[str, Any]:
        """生成章节"""
        self.current_chapter = chapter_num
        
        # 1. 导演设计章节大纲
        chapter_outline = self._director_plan_chapter(chapter_num)
        
        # 2. 世界构建者设置场景
        scene_description = self._world_builder_setup_scene(chapter_outline)
        
        # 3. 角色互动
        interactions = self._simulate_character_interactions(chapter_outline)
        
        # 4. 导演审核和引导
        self._director_review_and_guide(interactions)
        
        # 5. 叙事者转化为小说文本
        narrative_text = self._narrator_transform(interactions, scene_description)
        
        # 6. 编辑润色和检查
        final_text = self._editor_polish(narrative_text, chapter_num)
        
        # 7. 保存章节
        chapter_id = self.db.create_chapter(
            self.project_id,
            chapter_num,
            f"第{chapter_num}章",
            final_text,
            word_count=len(final_text)
        )
        
        return {
            "chapter_id": chapter_id,
            "chapter_num": chapter_num,
            "content": final_text,
            "interactions": interactions,
            "scene": scene_description
        }
    
    def _director_plan_chapter(self, chapter_num: int) -> Dict[str, Any]:
        """导演规划章节"""
        context = f"""
        当前章节：{chapter_num}
        故事大纲：{json.dumps(self.outline, ensure_ascii=False)}
        """
        
        analysis = self.director.analyze_current_scene(context)
        
        return {
            "chapter_num": chapter_num,
            "analysis": analysis
        }
    
    def _world_builder_setup_scene(self, chapter_outline: Dict[str, Any]) -> str:
        """世界构建者设置场景"""
        location = "未知地点"
        time_of_day = "白天"
        weather = "晴朗"
        mood = "平静"
        
        scene = self.world_builder.generate_scene_description(
            location, time_of_day, weather, mood
        )
        
        return scene
    
    def _simulate_character_interactions(self, chapter_outline: Dict[str, Any]) -> List[Dict[str, Any]]:
        """模拟角色互动"""
        interactions = []
        
        # 简化版：让主要角色进行互动
        if len(self.characters) > 0:
            char_names = list(self.characters.keys())
            
            # 第一个角色思考
            first_char = self.characters[char_names[0]]
            scene_context = f"第{self.current_chapter}章的场景"
            thought = first_char.think_about_situation(scene_context, char_names[1:])
            
            interactions.append({
                "character": first_char.name,
                "type": "thought",
                "content": thought
            })
            
            # 第一个角色行动
            action = first_char.decide_action(scene_context)
            interactions.append({
                "character": first_char.name,
                "type": "action",
                "content": action["description"]
            })
            
            # 如果有第二个角色，让其回应
            if len(char_names) > 1:
                second_char = self.characters[char_names[1]]
                response = second_char.respond_to_character(
                    first_char.name,
                    action["description"]
                )
                interactions.append({
                    "character": second_char.name,
                    "type": "response",
                    "content": response
                })
                
                # 更新关系记忆
                self.memory.record_interaction(
                    first_char.name,
                    second_char.name,
                    f"{first_char.name}的行动和{second_char.name}的回应"
                )
        
        return interactions
    
    def _director_review_and_guide(self, interactions: List[Dict[str, Any]]):
        """导演审核和引导"""
        # 简化版：记录互动
        for interaction in interactions:
            self.memory.add_world_event(
                f"{interaction['character']}的{interaction['type']}",
                chapter=self.current_chapter
            )
    
    def _narrator_transform(self, interactions: List[Dict[str, Any]], 
                           scene_description: str) -> str:
        """叙事者转化为小说文本"""
        narrative = self.narrator.transform_interaction(interactions, scene_description)
        return narrative
    
    def _editor_polish(self, text: str, chapter_num: int) -> str:
        """编辑润色"""
        polished = self.editor.polish_text(text, ["可读性", "文学性"])
        return polished
    
    def get_chapter_summary(self, chapter_id: int) -> str:
        """获取章节摘要"""
        chapter = self.db.get_chapter(chapter_id)
        if not chapter:
            return ""
        
        content = chapter.get("content", "")
        
        # 简化版：直接使用前500字作为摘要
        summary = content[:500] if len(content) > 500 else content
        
        return summary
    
    def get_story_context(self) -> Dict[str, Any]:
        """获取故事上下文"""
        return {
            "project": self.project_info,
            "outline": self.outline,
            "current_chapter": self.current_chapter,
            "characters": {
                name: agent.get_profile()
                for name, agent in self.characters.items()
            },
            "world_context": self.memory.get_world_context()
        }
