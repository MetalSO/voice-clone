# 语音处理服务 API 文档

## 概述

本API提供语音输入处理和语音合成功能，支持从手机端接收语音数据并进行处理，以及将文本转换为语音。

## 基础信息

- **服务地址**: `http://localhost:8000`
- **API版本**: 1.0.0
- **内容类型**: `application/json` (除了语音文件上传)

## 端点列表

| 端点 | 方法 | 描述 |
|------|------|------|
| `/health` | GET | 健康检查 |
| `/api/speech/process` | POST | 处理语音输入文件 |
| `/api/speech/synthesize` | POST | 文本转语音 |

## 详细说明

### 1. 健康检查

**端点**: `/health`
**方法**: `GET`
**描述**: 检查服务是否正常运行

**响应示例**:

```json
{
  "status": "ok",
  "message": "服务运行正常"
}
```

### 2. 语音输入处理

**端点**: `/api/speech/process`
**方法**: `POST`
**描述**: 上传语音文件并返回识别结果

**请求参数**:
- `file`: 语音文件 (支持常见音频格式如wav, mp3等)

**响应示例**:

成功:
```json
{
  "status": "success",
  "text": "你好，这是一段测试语音"
}
```

失败:
```json
{
  "detail": "处理语音文件失败: 无法识别语音"
}
```

### 3. 语音合成

**端点**: `/api/speech/synthesize`
**方法**: `POST`
**描述**: 将文本转换为语音

**请求体**:

```json
{
  "text": "这是一段测试文本",
  "model": "gtts", // 可选，默认gtts，可选值: gtts, pyttsx3
  "language": "zh-CN" // 可选，默认zh-CN
}
```

**响应示例**:

成功:
```json
{
  "status": "success",
  "audio_path": "output/123e4567-e89b-12d3-a456-426614174000.mp3"
}
```

失败:
```json
{
  "detail": "语音合成失败: 不支持的语音模型: unknown"
}
```

## 错误处理

API使用标准HTTP状态码来表示请求结果:

- `200 OK`: 请求成功
- `400 Bad Request`: 请求参数错误
- `500 Internal Server Error`: 服务器内部错误

错误响应格式:

```json
{
  "detail": "错误描述"
}
```

## 使用示例

### 1. 上传语音文件

**使用curl**:

```bash
curl -X POST "http://localhost:8000/api/speech/process" -F "file=@test.wav"
```

**使用Python requests**:

```python
import requests

url = "http://localhost:8000/api/speech/process"
files = {"file": open("test.wav", "rb")}
response = requests.post(url, files=files)
print(response.json())
```

### 2. 文本转语音

**使用curl**:

```bash
curl -X POST "http://localhost:8000/api/speech/synthesize" \
  -H "Content-Type: application/json" \
  -d '{"text": "这是一段测试文本", "model": "gtts", "language": "zh-CN"}'
```

**使用Python requests**:

```python
import requests

url = "http://localhost:8000/api/speech/synthesize"
data = {
    "text": "这是一段测试文本",
    "model": "gtts",
    "language": "zh-CN"
}
response = requests.post(url, json=data)
print(response.json())
```
