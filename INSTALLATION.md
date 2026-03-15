# 3zhuGe 安装指南

## 系统要求

- Python 3.9 或更高版本
- macOS / Linux / Windows
- 至少 2GB 磁盘空间
- 网络连接（用于LLM API调用）

## 安装步骤

### 1. 克隆或下载项目

```bash
# 如果已有项目目录，进入该目录
cd /Users/pony/Documents/code/ai/3zhuGe
```

### 2. 创建虚拟环境（推荐）

```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
# macOS/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate
```

### 3. 安装依赖

```bash
pip3 install -r requirements.txt
```

### 4. 配置API密钥

#### 方式1：使用OpenAI

```bash
# 复制环境配置模板
cp .env.example .env

# 编辑 .env 文件
nano .env
```

添加以下内容：
```
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your-api-key-here
```

获取OpenAI API密钥：
1. 访问 https://platform.openai.com/api-keys
2. 创建新的API密钥
3. 复制密钥到 .env 文件

#### 方式2：使用Anthropic

```bash
# 编辑 .env 文件
nano .env
```

添加以下内容：
```
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-your-api-key-here
```

获取Anthropic API密钥：
1. 访问 https://console.anthropic.com/
2. 创建新的API密钥
3. 复制密钥到 .env 文件

### 5. 验证安装

```bash
# 运行基础测试
python3 test_basic.py
```

预期输出：
```
🧪 3zhuGe 基础功能测试
==================================================

=== 测试数据库 ===
✅ 创建项目成功，ID: X
✅ 获取项目成功: 测试项目
✅ 创建角色成功，ID: X
✅ 获取角色成功，共1个

=== 测试Agent ===
✅ Agent初始化成功...

=== 测试记忆系统 ===
✅ 角色记忆初始化成功
✅ 世界事件添加成功
✅ 私密记忆添加成功
✅ 关系记忆添加成功
✅ 获取角色上下文成功

=== 测试LLM客户端 ===
✅ LLM生成成功...

==================================================
✅ 所有基础测试完成！
```

## 运行应用

### 方式1：启动Streamlit应用

```bash
streamlit run app.py
```

应用会自动在浏览器中打开：http://localhost:8501

### 方式2：运行演示脚本

```bash
python3 demo.py
```

这会演示系统的完整工作流程，不需要API密钥。

## 故障排除

### 问题1：ModuleNotFoundError

**症状**：`ModuleNotFoundError: No module named 'streamlit'`

**解决方案**：
```bash
# 重新安装依赖
pip3 install -r requirements.txt

# 或单独安装缺失的包
pip3 install streamlit openai anthropic pydantic python-dotenv
```

### 问题2：API密钥错误

**症状**：`ValueError: OPENAI_API_KEY not set`

**解决方案**：
```bash
# 检查 .env 文件是否存在
ls -la .env

# 检查 .env 文件内容
cat .env

# 确保密钥格式正确（不要有引号）
# 正确：OPENAI_API_KEY=sk-...
# 错误：OPENAI_API_KEY="sk-..."
```

### 问题3：Streamlit端口被占用

**症状**：`Address already in use`

**解决方案**：
```bash
# 使用不同的端口
streamlit run app.py --server.port 8502

# 或杀死占用端口的进程
lsof -i :8501
kill -9 <PID>
```

### 问题4：数据库错误

**症状**：`sqlite3.OperationalError`

**解决方案**：
```bash
# 删除损坏的数据库
rm data/3zhuge.db

# 重新启动应用，会自动创建新数据库
streamlit run app.py
```

### 问题5：Python版本不兼容

**症状**：`SyntaxError` 或其他版本相关错误

**解决方案**：
```bash
# 检查Python版本
python3 --version

# 需要Python 3.9+
# 如果版本过低，升级Python或使用虚拟环境
```

## 性能优化

### 1. 使用更快的模型

编辑 `config/settings.py`：
```python
LLM_MODEL = "gpt-3.5-turbo"  # 比GPT-4快且便宜
```

### 2. 减少章节长度

编辑 `config/settings.py`：
```python
DEFAULT_CHAPTER_LENGTH = 2000  # 从3000减少到2000
```

### 3. 增加记忆窗口

编辑 `config/settings.py`：
```python
WORKING_MEMORY_WINDOW = 5  # 保留最近5章完整内容
```

## 升级指南

### 从旧版本升级

```bash
# 备份数据
cp data/3zhuge.db data/3zhuge.db.backup

# 更新依赖
pip3 install -r requirements.txt --upgrade

# 运行迁移脚本（如果有）
python3 migrate.py

# 重启应用
streamlit run app.py
```

## 卸载

```bash
# 删除虚拟环境
rm -rf venv

# 删除项目目录
rm -rf /Users/pony/Documents/code/ai/3zhuGe

# 或只删除数据
rm -rf data/3zhuge.db
```

## 获取帮助

- 查看 [README.md](README.md) 了解功能详情
- 查看 [QUICKSTART.md](QUICKSTART.md) 快速开始
- 查看 [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) 项目总结
- 运行 `python3 test_basic.py` 验证安装
- 运行 `python3 demo.py` 查看演示

## 下一步

1. ✅ 安装完成
2. ⏭️ 阅读 [QUICKSTART.md](QUICKSTART.md)
3. ⏭️ 运行 `streamlit run app.py`
4. ⏭️ 创建你的第一部小说！

祝你使用愉快！🎉
