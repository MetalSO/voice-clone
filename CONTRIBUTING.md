# 贡献指南

感谢您对 VoiceClone 项目的关注！我们欢迎各种形式的贡献，包括但不限于：

- 🐛 报告 Bug
- 💡 提出新功能建议
- 📖 完善文档
- 🔧 提交代码改进
- 🌐 翻译文档

## 开发环境设置

### 1. Fork 项目

点击 GitHub 页面的 Fork 按钮创建您自己的副本。

### 2. 克隆您的 Fork

```bash
git clone https://github.com/YOUR_USERNAME/voice-clone.git
cd voice-clone
```

### 3. 添加上游仓库

```bash
git remote add upstream https://github.com/ORIGINAL_REPO/voice-clone.git
```

### 4. 创建开发分支

```bash
git checkout -b feature/your-feature-name
# 或
git checkout -b fix/your-bug-fix
```

## 代码规范

### Python

- 遵循 PEP 8 规范
- 使用有意义的变量和函数命名
- 添加适当的文档字符串

```python
def synthesize_speech(text: str, voice_id: str) -> str:
    """
    合成语音

    Args:
        text: 要合成的文本
        voice_id: 语音ID

    Returns:
        生成的音频文件路径
    """
    pass
```

### JavaScript/Vue

- 遵循 ESLint 配置
- 使用 Vue 3 Composition API
- 添加适当的注释

## 提交规范

### 提交信息格式

```
<type>: <subject>

<body>

<footer>
```

### Type 类型

- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更改
- `style`: 代码格式（不影响功能）
- `refactor`: 重构
- `test`: 测试相关
- `chore`: 构建/工具相关

### 示例

```
feat: 添加语音克隆参数配置

- 支持语速调节
- 支持音调调节
- 支持音量调节

Closes #123
```

## Pull Request 流程

1. **保持同步**：在开发前确保与上游同步

```bash
git fetch upstream
git checkout main
git merge upstream/main
```

2. **推送分支**

```bash
git push origin feature/your-feature-name
```

3. **创建 Pull Request**

- 清晰地描述更改内容和动机
- 关联相关 Issue
- 确保所有 CI 检查通过

## 测试

### 运行测试

```bash
# Python 后端测试
pytest

# 前端测试
cd voice-input-frontend
npm run test
```

### 编写测试

- 为新功能添加单元测试
- 确保测试覆盖核心逻辑
- 测试应独立、可重复执行

## 报告 Bug

请在提交 Bug 报告时包含：

1. **问题简述**
2. **复现步骤**
3. **预期行为**
4. **实际行为**
5. **环境信息**（操作系统、Python 版本等）

## 提出新功能

请在提交功能请求时包含：

1. **功能描述**
2. **使用场景**
3. **可能的实现方案**
4. **是否有替代方案**

## 许可证

通过贡献代码，您同意将您的作品按照 [MIT 许可证](../LICENSE) 发布。

---

再次感谢您的贡献！ 🎉
