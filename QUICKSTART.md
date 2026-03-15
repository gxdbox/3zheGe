# 3zhuGe 快速开始指南

## 5分钟快速上手

### 1. 安装和配置

```bash
# 进入项目目录
cd /Users/pony/Documents/code/ai/3zhuGe

# 安装依赖
pip3 install -r requirements.txt

# 复制环境配置模板
cp .env.example .env

# 编辑 .env 文件，添加你的API密钥
# 使用OpenAI:
# OPENAI_API_KEY=sk-...

# 或使用Anthropic:
# LLM_PROVIDER=anthropic
# ANTHROPIC_API_KEY=sk-ant-...
```

### 2. 运行应用

```bash
streamlit run app.py
```

应用会自动在浏览器中打开：`http://localhost:8501`

### 3. 创建你的第一部小说

#### 步骤1：选择模式
- **新手模式**：只需回答3个问题，快速生成故事框架
- **专家模式**：完全自定义所有设置

#### 步骤2：回答问题
新手模式示例：
- 题材：武侠
- 基调：热血激昂
- 主角类型：废柴逆袭

#### 步骤3：确认角色
系统会自动生成5个主要角色，你可以：
- 修改角色名字、性格、背景
- 删除不需要的角色
- 查看角色关系

#### 步骤4：生成故事
点击"生成下一章"按钮，系统会：
- 左侧显示Agent的思考和互动过程
- 右侧实时显示生成的小说文本

#### 步骤5：审阅和编辑
- 阅读生成的内容
- 如果满意，点击"生成下一章"继续
- 如果不满意，点击"重新生成"重试

#### 步骤6：导出
完成后可以导出为TXT或Markdown格式

## 演示模式（无需API密钥）

如果你还没有API密钥，可以先运行演示脚本了解系统工作原理：

```bash
python3 demo.py
```

这会演示：
- 项目和角色创建
- 三层记忆系统
- 角色Agent互动
- 故事大纲管理
- 章节保存

## 常见问题

### Q: 我没有API密钥怎么办？
A: 
1. 获取OpenAI API密钥：https://platform.openai.com/api-keys
2. 或获取Anthropic API密钥：https://console.anthropic.com/
3. 将密钥添加到 `.env` 文件

### Q: 生成速度太慢？
A: 
- 在控制面板中调整"生成速度"滑块
- 使用更快的模型（如GPT-3.5而不是GPT-4）
- 减少章节长度

### Q: 如何修改已生成的章节？
A:
- 在预览区域点击"编辑当前章节"
- 手动修改内容
- 或点击"重新生成"让AI重新生成

### Q: 如何调整故事方向？
A:
- 使用"调整大纲"功能修改情节框架
- 或在"管理角色"中修改角色设定
- 导演Agent会根据新设定调整故事

### Q: 支持哪些格式导出？
A: 目前支持：
- TXT（纯文本）
- Markdown（带格式）
- 计划支持：EPUB、PDF

## 项目结构速览

```
3zhuGe/
├── app.py                 # 主应用入口
├── demo.py               # 演示脚本
├── test_basic.py         # 基础测试
├── config/               # 配置文件
├── agents/               # Agent实现
├── core/                 # 核心模块
├── models/               # LLM和Prompt
├── db/                   # 数据库
├── ui/                   # UI组件
└── data/                 # 数据存储
```

## 下一步

- 📖 阅读 [README.md](README.md) 了解详细信息
- 🔧 查看 [config/settings.py](config/settings.py) 自定义配置
- 🧪 运行 `python3 test_basic.py` 验证安装
- 🎬 运行 `python3 demo.py` 查看演示

## 获取帮助

- 查看应用内的"❓ 帮助"面板
- 阅读代码注释了解实现细节
- 检查日志输出排查问题

祝你创作愉快！🎉
