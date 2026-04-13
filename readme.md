# VoiceClone - 语音克隆与合成系统

一个基于 FastAPI + Vue 3 的语音克隆与语音合成系统，支持多种 TTS 引擎。

[English](README_en.md) | 中文

## 功能特性

- 🎤 **语音录制** - 浏览器直接录制参考音频
- 🔊 **语音克隆** - 使用参考音频克隆音色
- 🌐 **多引擎支持** - Pocket-TTS, Coqui TTS, pyttsx3
- ⚡ **实时合成** - 支持实时语音合成输出
- 🎨 **现代化界面** - Vue 3 + Tailwind CSS

## 项目结构

```
voice-clone/
├── main.py                      # FastAPI 后端主入口
├── requirements.txt              # Python 依赖
├── services/                     # 服务模块
│   └── voice_clone/             # 语音克隆服务
├── modules/                      # 核心模块
│   ├── speech_processor.py      # 语音处理
│   └── speech_synthesizer.py   # 语音合成
├── voice-input-frontend/        # Vue 前端
│   ├── src/
│   │   ├── components/         # 组件
│   │   └── views/              # 视图
│   └── package.json
└── lib/                         # 本地依赖库
```

## 快速开始

### 环境要求

- Python 3.10+
- Node.js 18+
- FFmpeg (用于音频处理)

### 1. 克隆项目

```bash
git clone <your-repo-url>
cd voice-clone
```

### 2. 安装后端依赖

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境 (Windows)
venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

### 3. 安装前端依赖

```bash
cd voice-input-frontend
npm install
```

### 4. 配置 FFmpeg

下载并安装 FFmpeg: https://ffmpeg.org/download.html

或使用 winget (Windows):
```bash
winget install ffmpeg
```

### 5. 启动服务

启动后端:
```bash
# 在项目根目录
uvicorn main:app --host 0.0.0.0 --port 8080
```

启动前端 (新窗口):
```bash
cd voice-input-frontend
npm run dev
```

### 6. 访问应用

- 前端: http://localhost:3000
- 后端 API: http://localhost:8080
- API 文档: http://localhost:8080/docs

## 使用方法

### 语音克隆

1. 打开前端界面
2. 上传或录制参考音频（5-30秒，清晰无噪音）
3. 输入要合成的文本
4. 选择 TTS 模型
5. 点击合成按钮

### 可用模型

| 模型 | 说明 | 特点 |
|------|------|------|
| Pocket-TTS | Kyutai 轻量级模型 | 推荐，高质量 |
| pyttsx3 | 系统语音 | 无需网络，基础效果 |

## API 接口

### 健康检查
```
GET /health
```

### 语音克隆合成
```
POST /api/voice-clone/synthesize
Content-Type: multipart/form-data

参数:
- audio: 参考音频文件 (wav, mp3, webm)
- text: 要合成的文本
- speed: 语速 (0.5-2.0)
- model: 模型选择 (pockettts, pyttsx3)

响应:
{
  "audio_url": "/output/xxx.wav",
  "duration": 3.5
}
```

### 模型状态
```
GET /api/voice-clone/status
```

## 配置说明

### 环境变量

可在 `.env` 文件中配置:
```env
AZURE_SPEECH_KEY=your_key
AZURE_SPEECH_REGION=eastus
```

### 模型下载

Pocket-TTS 模型约 500MB，首次使用时会自动下载。

如需手动下载:
```bash
# 设置 HuggingFace 镜像
export HF_ENDPOINT=https://hf-mirror.com

# 下载模型
huggingface-cli download kyutai/pocket-tts-without-voice-cloning
```

## 开发指南

### 添加新的 TTS 引擎

1. 在 `services/voice_clone/` 目录创建新的引擎类
2. 实现 `initialize()` 和 `synthesize()` 方法
3. 在 `voice_clone_service.py` 中注册引擎
4. 更新 API 端点支持新引擎

示例:
```python
class MyTTSEngine:
    def initialize(self) -> bool:
        # 初始化模型
        pass

    def synthesize(self, text: str, reference_audio: str) -> str:
        # 合成语音
        pass
```

## 常见问题

### Q: 端口被占用
```bash
# 查找占用端口的进程
netstat -ano | findstr :8080

# 终止进程
taskkill /PID <PID> /F
```

### Q: 音频格式不支持
确保安装 FFmpeg 并将其添加到系统 PATH

### Q: 麦克风权限被拒绝
在浏览器设置中允许麦克风权限

## 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 开源协议

本项目基于 MIT 协议开源 - 详见 [LICENSE](LICENSE) 文件

## 致谢

- [Pocket-TTS](https://github.com/kyutai-labs/pocket-tts) - Kyutai Labs
- [FastAPI](https://fastapi.tiangolo.com/) - 现代 Python Web 框架
- [Vue.js](https://vuejs.org/) - 渐进式 JavaScript 框架
