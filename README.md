# 3zhuGe - 多Agent小说创作工具

用AI Agent模拟角色互动，自动生成精彩小说的创意工具。

## 🎯 核心特性

- **多Agent协作**：导演、叙事者、世界构建者、编辑和角色Agent协同工作
- **智能生成**：基于用户选择自动生成大纲、角色和故事内容
- **精准控制**：三层控制系统（硬约束、软引导、自由发挥）确保故事精彩但不失控
- **三层记忆**：共享世界记忆、角色独立记忆、关系记忆系统
- **长文管理**：滑动窗口+摘要压缩+向量检索处理长篇小说
- **实时展示**：分屏UI展示Agent互动和小说生成过程

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置API密钥

创建 `.env` 文件：

```
LLM_PROVIDER=openai
OPENAI_API_KEY=your_api_key_here
```

或使用Anthropic：

```
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=your_api_key_here
```

### 3. 运行应用

```bash
streamlit run app.py
```

应用将在 `http://localhost:8501` 打开。

## 📁 项目结构

```
3zhuGe/
├── app.py                    # Streamlit主应用
├── requirements.txt          # 依赖管理
├── config/
│   └── settings.py           # 全局配置
├── agents/
│   ├── base_agent.py         # Agent基类
│   ├── director_agent.py     # 导演Agent
│   ├── narrator_agent.py     # 叙事Agent
│   ├── world_builder_agent.py# 世界构建Agent
│   ├── editor_agent.py       # 编辑Agent
│   └── character_agent.py    # 角色Agent
├── core/
│   ├── memory.py             # 三层记忆系统
│   ├── story_engine.py       # 故事引擎
│   ├── consistency.py        # 一致性检查器
│   └── summary.py            # 章节摘要生成
├── models/
│   ├── llm_client.py         # LLM调用封装
│   └── prompts.py            # Prompt模板库
├── db/
│   └── database.py           # SQLite数据库
├── ui/
│   ├── guided_creation.py    # 引导式创作
│   ├── agent_panel.py        # Agent互动展示
│   ├── novel_preview.py      # 小说预览
│   └── control_panel.py      # 控制面板
└── data/
    ├── templates/            # 预设故事模板
    └── projects/             # 用户项目数据
```

## 💡 使用流程

### 1. 创建项目

选择新手模式或专家模式，回答几个问题：
- 题材（武侠、仙侠、都市等）
- 基调（热血、阴谋、轻松等）
- 主角类型（废柴逆袭、天才陨落等）

或选择预设模板快速开始。

### 2. 确认角色

系统自动生成5个主要角色，你可以：
- 修改角色名字、性格、背景
- 删除不需要的角色
- 查看角色关系图

### 3. 生成故事

点击"生成下一章"，系统会：
1. 导演规划章节
2. 世界构建者设置场景
3. 角色Agent进行互动
4. 叙事者转化为小说文本
5. 编辑润色和检查

### 4. 审阅和编辑

- 左侧查看Agent互动过程
- 右侧预览生成的小说文本
- 可以编辑、重新生成或继续下一章

### 5. 导出

支持导出为TXT、Markdown等格式。

## 🤖 Agent说明

### 导演Agent (Director)
- 把控整体情节走向
- 设计冲突和高潮
- 确保故事符合大纲框架
- 引导其他Agent的行动

### 叙事Agent (Narrator)
- 将角色互动转化为小说文本
- 保持文风一致
- 添加环境描写和心理描写
- 营造沉浸感

### 世界构建Agent (WorldBuilder)
- 管理世界设定
- 确保世界观一致性
- 生成场景描写
- 维护时间线

### 编辑Agent (Editor)
- 检查文本质量
- 检查逻辑漏洞
- 润色文本
- 最终审核

### 角色Agent (Character)
- 模拟角色思考和行动
- 与其他角色互动
- 维护角色一致性
- 记录角色成长

## 🧠 记忆系统

### 共享世界记忆
所有Agent都能访问的客观事实：
- 时间线
- 已发生事件
- 世界状态

### 角色独立记忆
每个角色Agent独有的私密信息：
- 内心想法
- 秘密
- 动机
- 情感状态

### 关系记忆
两个角色之间的互动记录：
- 互动历史
- 情感温度
- 共享秘密
- 冲突和联系

## ⚙️ 配置选项

在 `config/settings.py` 中可以配置：

- `LLM_PROVIDER`: 使用的LLM提供商（openai/anthropic）
- `LLM_MODEL`: 使用的模型
- `DEFAULT_CHAPTER_LENGTH`: 默认章节长度
- `WORKING_MEMORY_WINDOW`: 工作记忆窗口大小
- `AGENT_THINK_TIMEOUT`: Agent思考超时时间

## 📊 数据库

使用SQLite存储：
- 项目信息
- 角色设定
- 章节内容
- 记忆数据
- 事件日志

数据库文件位置：`data/3zhuge.db`

## 🔄 工作流程

```
用户输入
  ↓
引导式创作（5-8个选择题）
  ↓
自动生成大纲和角色
  ↓
用户确认角色设定
  ↓
故事引擎开始生成
  ├─ 导演规划章节
  ├─ 世界构建者设置场景
  ├─ 角色Agent互动
  ├─ 导演审核和引导
  ├─ 叙事者转化文本
  └─ 编辑润色检查
  ↓
用户审阅和编辑
  ↓
继续下一章或导出
```

## 🎨 UI特性

- **分屏展示**：左侧Agent互动，右侧小说预览
- **实时更新**：生成过程实时显示
- **多种视图**：列表视图、阅读视图、统计视图
- **交互控制**：暂停、继续、重新生成、编辑等
- **导出功能**：支持多种格式导出

## 🚧 开发路线图

### Phase 1 ✅ 基础框架
- [x] 项目结构
- [x] Agent基类和固定Agent
- [x] 数据库设计
- [x] 基础UI

### Phase 2 🔄 核心功能
- [ ] 完整的故事生成流程
- [ ] 三层记忆系统优化
- [ ] 一致性检查完善
- [ ] UI交互完善

### Phase 3 📋 增强功能
- [ ] 向量检索集成
- [ ] 长文记忆管理
- [ ] 预设模板库
- [ ] 角色关系图谱可视化

### Phase 4 🎯 优化和扩展
- [ ] 性能优化
- [ ] 多语言支持
- [ ] 云端保存
- [ ] 协同创作

## 📝 许可证

MIT License

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📧 联系方式

如有问题或建议，请联系开发者。
