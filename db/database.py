import sqlite3
import json
from datetime import datetime
from typing import Optional, List, Dict, Any
from pathlib import Path
from config.settings import DATABASE_PATH


class Database:
    """SQLite数据库管理"""
    
    def __init__(self, db_path: str = DATABASE_PATH):
        self.db_path = db_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self.init_db()
    
    def get_connection(self):
        """获取数据库连接"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_db(self):
        """初始化数据库表"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # 项目表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                genre TEXT,
                tone TEXT,
                protagonist_type TEXT,
                core_conflict TEXT,
                story_scale TEXT,
                outline TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 角色表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS characters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                gender TEXT,
                age INTEGER,
                personality TEXT,
                background TEXT,
                goal TEXT,
                motivation TEXT,
                relationships TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (project_id) REFERENCES projects(id)
            )
        ''')
        
        # 章节表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chapters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER NOT NULL,
                chapter_num INTEGER,
                title TEXT,
                content TEXT,
                summary TEXT,
                word_count INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (project_id) REFERENCES projects(id)
            )
        ''')
        
        # 记忆表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER NOT NULL,
                memory_type TEXT,
                character_id INTEGER,
                content TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (project_id) REFERENCES projects(id),
                FOREIGN KEY (character_id) REFERENCES characters(id)
            )
        ''')
        
        # 事件表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER NOT NULL,
                chapter_id INTEGER,
                event_type TEXT,
                description TEXT,
                timestamp TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (project_id) REFERENCES projects(id),
                FOREIGN KEY (chapter_id) REFERENCES chapters(id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    # Project operations
    def create_project(self, name: str, genre: str, tone: str, 
                      protagonist_type: str, core_conflict: str, 
                      story_scale: str, outline: str) -> int:
        """创建新项目"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO projects 
            (name, genre, tone, protagonist_type, core_conflict, story_scale, outline)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (name, genre, tone, protagonist_type, core_conflict, story_scale, outline))
        conn.commit()
        project_id = cursor.lastrowid
        conn.close()
        return project_id
    
    def get_project(self, project_id: int) -> Optional[Dict]:
        """获取项目"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM projects WHERE id = ?', (project_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None
    
    # Character operations
    def create_character(self, project_id: int, name: str, gender: str, age: int,
                        personality: str, background: str, goal: str, 
                        motivation: str, relationships: str) -> int:
        """创建角色"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO characters 
            (project_id, name, gender, age, personality, background, goal, motivation, relationships)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (project_id, name, gender, age, personality, background, goal, motivation, relationships))
        conn.commit()
        character_id = cursor.lastrowid
        conn.close()
        return character_id
    
    def get_characters(self, project_id: int) -> List[Dict]:
        """获取项目的所有角色"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM characters WHERE project_id = ?', (project_id,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    
    # Chapter operations
    def create_chapter(self, project_id: int, chapter_num: int, title: str, 
                      content: str, summary: str = "", word_count: int = 0) -> int:
        """创建章节"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO chapters 
            (project_id, chapter_num, title, content, summary, word_count)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (project_id, chapter_num, title, content, summary, word_count))
        conn.commit()
        chapter_id = cursor.lastrowid
        conn.close()
        return chapter_id
    
    def get_chapter(self, chapter_id: int) -> Optional[Dict]:
        """获取章节"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM chapters WHERE id = ?', (chapter_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None
    
    def get_chapters(self, project_id: int, limit: int = 100) -> List[Dict]:
        """获取项目的章节"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM chapters WHERE project_id = ? 
            ORDER BY chapter_num DESC LIMIT ?
        ''', (project_id, limit))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    
    def update_chapter(self, chapter_id: int, content: str = None, 
                      summary: str = None, word_count: int = None):
        """更新章节"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        updates = []
        params = []
        
        if content is not None:
            updates.append("content = ?")
            params.append(content)
        if summary is not None:
            updates.append("summary = ?")
            params.append(summary)
        if word_count is not None:
            updates.append("word_count = ?")
            params.append(word_count)
        
        updates.append("updated_at = CURRENT_TIMESTAMP")
        params.append(chapter_id)
        
        cursor.execute(f"UPDATE chapters SET {', '.join(updates)} WHERE id = ?", params)
        conn.commit()
        conn.close()
    
    # Memory operations
    def save_memory(self, project_id: int, memory_type: str, 
                   content: str, character_id: Optional[int] = None) -> int:
        """保存记忆"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO memories (project_id, memory_type, character_id, content)
            VALUES (?, ?, ?, ?)
        ''', (project_id, memory_type, character_id, content))
        conn.commit()
        memory_id = cursor.lastrowid
        conn.close()
        return memory_id
    
    def get_memories(self, project_id: int, memory_type: str = None, 
                    character_id: int = None) -> List[Dict]:
        """获取记忆"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = 'SELECT * FROM memories WHERE project_id = ?'
        params = [project_id]
        
        if memory_type:
            query += ' AND memory_type = ?'
            params.append(memory_type)
        if character_id:
            query += ' AND character_id = ?'
            params.append(character_id)
        
        query += ' ORDER BY created_at DESC'
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    
    # Event operations
    def log_event(self, project_id: int, event_type: str, description: str, 
                 chapter_id: Optional[int] = None, timestamp: str = None) -> int:
        """记录事件"""
        conn = self.get_connection()
        cursor = conn.cursor()
        if timestamp is None:
            timestamp = datetime.now().isoformat()
        
        cursor.execute('''
            INSERT INTO events (project_id, chapter_id, event_type, description, timestamp)
            VALUES (?, ?, ?, ?, ?)
        ''', (project_id, chapter_id, event_type, description, timestamp))
        conn.commit()
        event_id = cursor.lastrowid
        conn.close()
        return event_id
    
    def get_events(self, project_id: int, limit: int = 100) -> List[Dict]:
        """获取事件"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM events WHERE project_id = ? 
            ORDER BY timestamp DESC LIMIT ?
        ''', (project_id, limit))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
