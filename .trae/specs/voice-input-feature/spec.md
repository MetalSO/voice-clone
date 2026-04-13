# 语音转文字功能规格说明书

## 一、需求概述

### 1.1 项目背景

当前项目已具备语音合成功能（文字转语音），现需要新增语音转文字功能（语音输入），实现用户通过麦克风录音并实时转换为文字的功能。这是一个完整的语音交互系统。

### 1.2 核心需求

* 实现网页端语音录音功能

* 将录制的音频实时转换为文字

* 采用前后端分离架构

* 前端使用 Vue 框架

* 后端使用 Java Spring Boot 框架

## 二、技术架构

### 2.1 架构设计

```
┌─────────────────┐         ┌─────────────────┐
│   Vue 前端      │   HTTP  │  Spring Boot   │
│  (Port 5173)   │◄───────►│  后端服务       │
│                 │   REST  │  (Port 8080)   │
└─────────────────┘         └─────────────────┘
       │                           │
       │                     ┌─────┴─────┐
       │                     │  语音识别  │
       │                     │  服务层    │
       │                     └───────────┘
```

### 2.2 技术栈

#### 前端技术栈

* **框架**：Vue 3

* **构建工具**：Vite

* **HTTP客户端**：Axios

* **录音组件**：Web Speech API / MediaRecorder API

* **状态管理**：Pinia

* **UI组件**：Element Plus

#### 后端技术栈

* **框架**：Spring Boot 3.x

* **语音识别**：百度语音识别 API / 讯飞语音识别 API

* **构建工具**：Maven

* **Java版本**：JDK 17

## 三、功能需求

### 3.1 核心功能

#### F1: 语音录制功能

* 用户点击录音按钮开始录音

* 实时显示录音时长

* 支持中断录音

* 录音文件临时存储

#### F2: 语音转文字功能

* 将录制的音频上传至后端

* 后端调用语音识别API进行转换

* 返回识别结果并展示

* 支持中英文识别

#### F3: 实时显示功能

* 识别过程中显示加载状态

* 识别完成后实时更新文本内容

* 识别失败时显示错误信息

### 3.2 用户交互流程

1. 用户进入语音输入页面
2. 用户点击"开始录音"按钮
3. 系统请求麦克风权限
4. 权限通过后开始录音，显示录音时长
5. 用户点击"停止录音"按钮
6. 系统上传音频文件至后端
7. 后端调用语音识别服务
8. 识别结果返回前端并展示
9. 用户可对识别结果进行编辑或复制

## 四、接口设计

### 4.1 REST API 接口

#### 4.1.1 语音识别接口

**请求**

```
POST /api/speech/recognize
Content-Type: multipart/form-data

参数：
- audio: 音频文件 (WAV/MP3/PCM)
- language: 语言类型 (zh-CN / en-US)
```

**响应**

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "text": "识别出的文字内容",
    "duration": 5.2,
    "language": "zh-CN"
  }
}
```

#### 4.1.2 语音识别（实时流式）接口

**请求**

```
POST /api/speech/recognize-stream
Content-Type: audio/*

音频流数据
```

**响应**

```
SSE (Server-Sent Events) 流式返回识别结果
```

### 4.2 错误码定义

| 错误码  | 说明        |
| ---- | --------- |
| 200  | 成功        |
| 400  | 请求参数错误    |
| 401  | 认证失败      |
| 403  | 无权限访问     |
| 500  | 服务器内部错误   |
| 1001 | 音频格式不支持   |
| 1002 | 音频文件过大    |
| 1003 | 语音识别服务不可用 |

## 五、前端实现需求

### 5.1 页面结构

```
voice-input/
├── src/
│   ├── components/
│   │   ├── VoiceRecorder.vue      # 录音组件
│   │   ├── RecognitionResult.vue  # 识别结果展示组件
│   │   └── AudioWaveform.vue      # 音频波形展示组件
│   ├── views/
│   │   └── VoiceInputView.vue      # 语音输入主页面
│   ├── services/
│   │   └── speechService.js       # 语音服务API调用
│   ├── stores/
│   │   └── voiceStore.js           # 状态管理
│   └── App.vue
```

### 5.2 组件规格

#### VoiceRecorder 组件

* 属性：

  * `language`: 语言类型，默认 "zh-CN"

  * `maxDuration`: 最大录音时长，默认 60 秒

* 事件：

  * `@start`: 开始录音时触发

  * `@stop`: 停止录音时触发，携带音频 blob

  * `@error`: 录音出错时触发

* 方法：

  * `startRecording()`: 开始录音

  * `stopRecording()`: 停止录音

  * `cancelRecording()`: 取消录音

#### RecognitionResult 组件

* 属性：

  * `text`: 识别结果文本

  * `loading`: 是否正在识别

  * `error`: 错误信息

* 事件：

  * `@copy`: 复制文本时触发

  * `@edit`: 编辑文本时触发

## 六、后端实现需求

### 6.1 项目结构

```
speech-backend/
├── src/main/java/com/speech/
│   ├── SpeechApplication.java
│   ├── controller/
│   │   └── SpeechController.java
│   ├── service/
│   │   ├── SpeechRecognitionService.java
│   │   └── impl/
│   │       └── SpeechRecognitionServiceImpl.java
│   ├── config/
│   │   └── WebConfig.java
│   ├── dto/
│   │   ├── RecognitionRequest.java
│   │   └── RecognitionResponse.java
│   └── exception/
│       ├── SpeechException.java
│       └── GlobalExceptionHandler.java
├── src/main/resources/
│   └── application.yml
└── pom.xml
```

### 6.2 配置项

```yaml
spring:
  servlet:
    multipart:
      max-file-size: 10MB
      max-request-size: 10MB

speech:
  baidu:
    app-id: ${BAIDU_APP_ID}
    api-key: ${BAIDU_API_KEY}
    secret-key: ${BAIDU_SECRET_KEY}
```

## 七、验收标准

### 7.1 功能验收

* [ ] 用户可以成功进行语音录音

* [ ] 录音时长正确显示

* [ ] 录音可以正常停止

* [ ] 音频文件可以成功上传

* [ ] 语音识别结果正确返回

* [ ] 识别结果可以正常展示

* [ ] 错误信息可以正确处理

### 7.2 性能验收

* [ ] 页面加载时间 < 3秒

* [ ] 录音启动时间 < 1秒

* [ ] 识别响应时间 < 5秒（60秒音频）

### 7.3 兼容性验收

* [ ] Chrome 浏览器支持

* [ ] Firefox 浏览器支持

* [ ] Edge 浏览器支持

* [ ] 移动端 Safari 支持

## 八、已知限制

1. **浏览器兼容性**：需要浏览器支持 MediaRecorder API
2. **麦克风权限**：需要用户授权麦克风访问权限
3. **网络要求**：需要稳定的网络连接进行音频上传
4. **音频格式**：仅支持 WAV、MP3、PCM 格式

## 九、后续扩展

* 实时语音转文字（流式识别）

* 多语言混合识别

* 标点符号自动添加

* 说话人分离

* 关键词提取

