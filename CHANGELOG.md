# 更新日志

所有重要的项目更新都会在此文件中记录。

## [1.0.0] - 2024-01-XX

### Added

- 语音克隆功能
  - 支持 Pocket-TTS 引擎
  - 支持 pyttsx3 引擎
  - 支持参考音频上传和录制
- 语音合成功能
  - 多引擎支持
  - 语速、音调、音量调节
- Web 界面
  - Vue 3 前端
  - 响应式设计
  - 实时录音功能
- API 接口
  - RESTful API 设计
  - Swagger 文档

### Features

- `POST /api/voice-clone/synthesize` - 语音克隆合成
- `GET /api/voice-clone/status` - 模型状态查询
- `GET /health` - 健康检查

### Dependencies

- FastAPI - Web 框架
- Vue 3 - 前端框架
- Pocket-TTS - 语音克隆引擎
- pydub - 音频处理
- FFmpeg - 音频格式转换
