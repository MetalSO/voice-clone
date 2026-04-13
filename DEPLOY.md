# 语音处理服务部署说明

## 系统要求

- Python 3.7 或更高版本
- pip 包管理工具
- 互联网连接（用于语音识别和gTTS语音合成）

## 环境配置

### 1. 克隆项目

```bash
git clone <项目地址>
cd <项目目录>
```

### 2. 安装依赖

使用pip安装项目依赖：

```bash
pip install -r requirements.txt
```

依赖说明：
- `fastapi`: 用于构建RESTful API
- `uvicorn`: ASGI服务器，用于运行FastAPI应用
- `pydantic`: 数据验证库
- `python-multipart`: 处理文件上传
- `speechrecognition`: 语音识别库
- `pyttsx3`: 离线语音合成库
- `gTTS`: Google Text-to-Speech，在线语音合成库
- `python-dotenv`: 环境变量管理

### 3. 环境变量配置

创建 `.env` 文件（可选），用于配置环境变量：

```dotenv
# 服务配置
HOST=0.0.0.0
PORT=8000

# 其他配置...
```

## 启动服务

### 开发环境启动

使用Python直接运行主文件：

```bash
python main.py
```

或使用uvicorn启动：

```bash
uvicorn main:app --reload
```

### 生产环境启动

使用uvicorn启动，指定主机和端口：

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## 服务验证

服务启动后，可以通过以下方式验证服务是否正常运行：

1. 访问健康检查端点：
   ```
   http://localhost:8000/health
   ```
   应返回：
   ```json
   {"status": "ok", "message": "服务运行正常"}
   ```

2. 访问API文档：
   ```
   http://localhost:8000/docs
   ```
   这将打开FastAPI自动生成的交互式API文档，可以在浏览器中测试API端点。

## 目录结构

```
├── main.py              # 主应用文件
├── requirements.txt     # 依赖配置文件
├── modules/             # 模块目录
│   ├── speech_processor.py  # 语音处理模块
│   └── speech_synthesizer.py # 语音合成模块
├── output/              # 生成的语音文件目录
├── API.md               # API接口文档
└── DEPLOY.md            # 部署说明文档
```

## 常见问题

### 1. 语音识别失败

- 确保语音文件格式正确（建议使用wav格式）
- 确保网络连接正常（Google Web Speech API需要互联网连接）
- 确保语音清晰，无背景噪音

### 2. 语音合成失败

- 对于gTTS模型，确保网络连接正常
- 对于pyttsx3模型，确保系统已安装相应的语音引擎

### 3. 服务启动失败

- 检查端口是否被占用
- 检查依赖是否安装完整
- 查看控制台错误信息

## 性能优化

1. **语音文件处理**：对于大型语音文件，可以考虑使用流式处理或异步处理
2. **缓存机制**：对于重复的文本合成，可以考虑缓存结果
3. **并发处理**：使用uvicorn的多进程模式提高并发处理能力

## 安全建议

1. **文件上传**：限制上传文件大小和类型，防止恶意文件上传
2. **API访问**：在生产环境中添加认证机制
3. **CORS配置**：在生产环境中设置具体的前端域名，而不是使用通配符
4. **临时文件**：确保临时文件被正确删除，防止磁盘空间耗尽
