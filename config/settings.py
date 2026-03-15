import os
from dotenv import load_dotenv

load_dotenv()

# LLM Configuration
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")  # "openai" or "anthropic"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4-turbo-preview")
LLM_BASE_URL = os.getenv("LLM_BASE_URL", None)  # Custom base URL for OpenAI-compatible APIs

# Story Generation Settings
DEFAULT_CHAPTER_LENGTH = 3000  # words
MAX_CHAPTER_LENGTH = 5000
MIN_CHAPTER_LENGTH = 1500

# Memory Settings
WORKING_MEMORY_WINDOW = 3  # Keep last N chapters in full
SUMMARY_LENGTH = 200  # words per chapter summary
MAX_RELATIONSHIP_HISTORY = 20  # Keep last N interactions

# Agent Settings
AGENT_THINK_TIMEOUT = 30  # seconds
AGENT_ACT_TIMEOUT = 30

# Database
DATABASE_PATH = "data/3zhuge.db"

# UI Settings
STREAMLIT_PAGE_TITLE = "3zhuGe - 多Agent小说创作工具"
STREAMLIT_PAGE_ICON = "📖"

# Story Templates
STORY_TEMPLATES = {
    "武侠复仇": {
        "genre": "武侠",
        "tone": "热血激昂",
        "protagonist_type": "废柴逆袭",
        "core_conflict": "江湖恩怨",
        "description": "经典武侠复仇故事框架"
    },
    "仙侠修行": {
        "genre": "仙侠",
        "tone": "热血激昂",
        "protagonist_type": "天才陨落",
        "core_conflict": "门派争斗",
        "description": "仙侠修行成长故事框架"
    },
    "都市爱情": {
        "genre": "都市",
        "tone": "轻松幽默",
        "protagonist_type": "平凡英雄",
        "core_conflict": "正邪对立",
        "description": "都市爱情故事框架"
    }
}
