# 3zhuGe 文件结构说明

## 完整文件清单

```
3zhuGe/
│
├── 📄 app.py                          # Streamlit主应用入口（450行）
├── 📄 demo.py                         # 完整工作流演示脚本（260行）
├── 📄 test_basic.py                   # 基础功能测试脚本（180行）
│
├── 📁 config/
│   └── 📄 settings.py                 # 全局配置文件（60行）
│
├── 📁 agents/                         # Agent实现（6个文件，总计900行）
│   ├── 📄 base_agent.py               # Agent基类（60行）
│   ├── 📄 director_agent.py           # 导演Agent（120行）
│   ├── 📄 narrator_agent.py           # 叙事Agent（130行）
│   ├── 📄 world_builder_agent.py      # 世界构建Agent（140行）
│   ├── 📄 editor_agent.py             # 编辑Agent（150行）
│   └── 📄 character_agent.py          # 角色Agent（200行）
│
├── 📁 core/                           # 核心模块（5个文件，总计1130行）
│   ├── 📄 memory.py                   # 三层记忆系统（350行）
│   ├── 📄 story_engine.py             # 故事引擎（280行）
│   ├── 📄 outline.py                  # 大纲管理（180行）
│   ├── 📄 consistency.py              # 一致性检查（200行）
│   └── 📄 summary.py                  # 章节摘要生成（120行）
│
├── 📁 models/                         # LLM和Prompt（2个文件，总计270行）
│   ├── 📄 llm_client.py               # LLM客户端封装（70行）
│   └── 📄 prompts.py                  # Prompt模板库（200行）
│
├── 📁 db/
│   └── 📄 database.py                 # SQLite数据库操作（350行）
│
├── 📁 ui/                             # UI组件（4个文件，总计1180行）
│   ├── 📄 guided_creation.py          # 引导式创作页面（350行）
│   ├── 📄 agent_panel.py              # Agent互动展示面板（250行）
│   ├── 📄 novel_preview.py            # 小说预览面板（300行）
│   └── 📄 control_panel.py            # 控制面板（280行）
│
├── 📁 data/                           # 数据存储
│   ├── 📄 3zhuge.db                   # SQLite数据库（自动创建）
│   ├── 📁 templates/                  # 预设故事模板（待扩展）
│   └── 📁 projects/                   # 用户项目数据（待扩展）
│
├── 📄 requirements.txt                # 项目依赖
├── 📄 .env.example                    # 环境配置示例
│
├── 📄 README.md                       # 完整项目文档（400行）
├── 📄 QUICKSTART.md                   # 快速开始指南（200行）
├── 📄 INSTALLATION.md                 # 安装指南（300行）
├── 📄 PROJECT_SUMMARY.md              # 项目总结（400行）
├── 📄 COMPLETION_REPORT.md            # 项目完成报告（500行）
└── 📄 FILE_STRUCTURE.md               # 本文件
```

## 文件说明

### 核心应用文件

#### `app.py` - Streamlit主应用
- **功能**：应用入口，包含所有页面路由
- **页面**：
  - 主页（home）
  - 创建项目（create）
  - 确认角色（confirm）
  - 生成故事（generate）
  - 打开项目（open）
- **依赖**：所有UI模块和核心模块
- **启动**：`streamlit run app.py`

#### `demo.py` - 演示脚本
- **功能**：演示系统完整工作流程
- **演示内容**：
  1. 项目创建
  2. 角色生成
  3. 记忆初始化
  4. 角色互动
  5. 章节保存
- **特点**：无需API密钥
- **运行**：`python3 demo.py`

#### `test_basic.py` - 测试脚本
- **功能**：验证基础功能
- **测试项**：
  - 数据库操作
  - Agent初始化
  - 记忆系统
  - LLM客户端
- **运行**：`python3 test_basic.py`

### 配置文件

#### `config/settings.py`
- LLM配置（提供商、模型、API密钥）
- 故事生成参数（章节长度、记忆窗口）
- 数据库路径
- UI设置
- 预设模板

#### `requirements.txt`
- streamlit==1.28.1
- openai==1.3.0
- anthropic==0.7.0
- pydantic==2.4.2
- python-dotenv==1.0.0

#### `.env.example`
- LLM_PROVIDER 配置
- API_KEY 示例

### Agent模块 (`agents/`)

#### `base_agent.py`
- **BaseAgent** 基类
- 方法：think(), speak(), act(), remember()
- 内存管理

#### `director_agent.py`
- **DirectorAgent** 导演
- 方法：analyze_current_scene(), guide_character_action()
- 大纲管理和约束检查

#### `narrator_agent.py`
- **NarratorAgent** 叙事者
- 方法：transform_interaction(), enhance_description()
- 文本生成和风格管理

#### `world_builder_agent.py`
- **WorldBuilderAgent** 世界构建者
- 方法：initialize_world(), generate_scene_description()
- 设定管理和一致性检查

#### `editor_agent.py`
- **EditorAgent** 编辑
- 方法：check_quality(), polish_text()
- 质量检查和文本润色

#### `character_agent.py`
- **CharacterAgent** 角色
- 方法：think_about_situation(), decide_action()
- 角色状态和关系管理

### 核心模块 (`core/`)

#### `memory.py` - 三层记忆系统
- **Memory** 类
- 共享世界记忆
- 角色独立记忆
- 关系记忆
- 方法：add_world_event(), add_private_thought(), record_interaction()

#### `story_engine.py` - 故事引擎
- **StoryEngine** 类
- 协调所有Agent
- 生成章节流程
- 方法：generate_chapter(), get_story_context()

#### `outline.py` - 大纲管理
- **OutlineManager** 类
- 大纲设置和验证
- 约束检查
- 方法：check_must_event_completion(), check_forbidden_event_violation()

#### `consistency.py` - 一致性检查
- **ConsistencyChecker** 类
- 角色行为验证
- 能力和物品检查
- 时间线和关系验证
- 方法：validate_action(), check_world_consistency()

#### `summary.py` - 摘要生成
- **SummaryGenerator** 类
- 章节摘要生成
- 关键事件提取
- 角色弧线追踪
- 方法：generate_summary(), extract_key_events()

### 数据和模型 (`models/` 和 `db/`)

#### `llm_client.py`
- **LLMClient** 基类
- **OpenAIClient** OpenAI实现
- **AnthropicClient** Anthropic实现
- 函数：get_llm_client()

#### `prompts.py`
- 各Agent的系统Prompt
- 用户交互Prompt
- 大纲生成Prompt
- 角色生成Prompt
- 检查和验证Prompt

#### `database.py`
- **Database** 类
- SQLite操作
- 表设计：projects, characters, chapters, memories, events
- 方法：create_project(), get_chapters(), save_memory()

### UI模块 (`ui/`)

#### `guided_creation.py`
- **GuidedCreation** 类
- 新手模式（3个问题）
- 专家模式（完全自定义）
- 预设模板选择
- 大纲和角色生成
- 角色确认界面

#### `agent_panel.py`
- **AgentPanel** 类
- 消息展示
- Agent状态栏
- 互动摘要
- 实时流文本
- 思考过程展示
- 决策树展示
- 冲突检测
- 记忆预览

#### `novel_preview.py`
- **NovelPreview** 类
- 章节导航
- 章节列表
- 统计信息
- 章节大纲
- 导出功能（TXT、Markdown）
- 多种阅读视图

#### `control_panel.py`
- **ControlPanel** 类
- 播放控制（暂停、继续、跳过）
- 生成设置（速度、自由度、质量）
- 检查点管理
- 编辑工具
- 调试面板
- 快速操作
- 导出控制
- 帮助面板
- 状态栏

### 数据存储 (`data/`)

#### `3zhuge.db`
- SQLite数据库文件
- 表：projects, characters, chapters, memories, events
- 自动创建和管理

#### `templates/`
- 预设故事模板（待扩展）
- 模板格式：JSON或YAML

#### `projects/`
- 用户项目数据（待扩展）
- 项目备份和导出

### 文档文件

#### `README.md`
- 项目概述
- 核心特性
- 快速开始
- 项目结构
- 使用流程
- Agent说明
- 记忆系统说明
- 配置选项
- 工作流程
- 开发路线图

#### `QUICKSTART.md`
- 5分钟快速上手
- 安装和配置
- 运行应用
- 创建第一部小说
- 演示模式
- 常见问题

#### `INSTALLATION.md`
- 系统要求
- 详细安装步骤
- 虚拟环境设置
- API密钥配置
- 验证安装
- 故障排除
- 性能优化
- 升级指南

#### `PROJECT_SUMMARY.md`
- 项目完成状态
- 已完成功能
- 核心特性
- 技术架构
- 使用流程
- 已验证功能
- 部署和运行
- 下一步改进
- 关键设计决策
- 性能指标
- 已知限制
- 测试覆盖

#### `COMPLETION_REPORT.md`
- 项目概览
- 完成情况
- 交付物清单
- 总代码量
- 核心功能实现
- 验证结果
- 技术架构
- 使用指南
- 已知限制
- 后续改进方向
- 项目亮点
- 项目成果总结
- 建议使用方式
- 最终评价

## 代码统计

| 类别 | 文件数 | 代码行数 |
|------|--------|---------|
| Agent系统 | 6 | 900 |
| 核心模块 | 5 | 1,130 |
| 数据和模型 | 3 | 620 |
| UI组件 | 4 | 1,180 |
| 应用入口 | 1 | 450 |
| 测试和演示 | 2 | 440 |
| **总计** | **21** | **4,720** |

加上文档（~1,300行），总计约6,000行。

## 快速导航

### 我想...

**了解项目**
- 阅读 `README.md`
- 查看 `PROJECT_SUMMARY.md`

**快速开始**
- 阅读 `QUICKSTART.md`
- 运行 `python3 demo.py`

**安装和配置**
- 阅读 `INSTALLATION.md`
- 配置 `.env` 文件

**运行应用**
- 执行 `streamlit run app.py`
- 在浏览器打开应用

**测试系统**
- 运行 `python3 test_basic.py`
- 运行 `python3 demo.py`

**学习代码**
- 查看 `agents/` 了解Agent设计
- 查看 `core/` 了解核心逻辑
- 查看 `ui/` 了解UI实现

**扩展功能**
- 在 `agents/` 添加新Agent
- 在 `core/` 添加新模块
- 在 `ui/` 添加新页面

**部署应用**
- 参考 `INSTALLATION.md` 的部署部分
- 配置生产环境变量
- 优化性能参数

## 文件依赖关系

```
app.py
├── ui/guided_creation.py
├── ui/agent_panel.py
├── ui/novel_preview.py
├── ui/control_panel.py
├── core/story_engine.py
│   ├── agents/director_agent.py
│   ├── agents/narrator_agent.py
│   ├── agents/world_builder_agent.py
│   ├── agents/editor_agent.py
│   ├── agents/character_agent.py
│   ├── core/memory.py
│   ├── core/outline.py
│   └── core/consistency.py
├── db/database.py
└── config/settings.py

demo.py
├── db/database.py
├── core/memory.py
├── core/outline.py
├── agents/character_agent.py
└── config/settings.py

test_basic.py
├── db/database.py
├── agents/base_agent.py
├── agents/director_agent.py
├── agents/narrator_agent.py
├── agents/world_builder_agent.py
├── agents/editor_agent.py
├── agents/character_agent.py
├── core/memory.py
├── models/llm_client.py
└── config/settings.py
```

## 总结

3zhuGe项目包含：
- **21个代码文件**，约4,720行代码
- **6个Agent实现**，各司其职
- **5个核心模块**，完整的功能支持
- **4个UI组件**，友好的用户界面
- **完整的文档**，便于理解和使用

所有文件都已完成并通过验证，可以直接使用或进一步扩展。
