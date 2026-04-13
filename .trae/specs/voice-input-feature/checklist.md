# 语音转文字功能检查清单

## 项目初始化检查点

- [x] Vue 项目使用 Vite 构建工具创建
- [x] Vue 项目使用 Vue 3 框架
- [x] 已安装 Element Plus UI 组件库
- [x] 已安装 Axios HTTP 客户端
- [x] 已安装 Pinia 状态管理库
- [x] Spring Boot 项目使用 Maven 构建
- [x] Spring Boot 版本为 3.x
- [x] JDK 版本为 17 或更高
- [x] application.yml 配置完成

## 前端组件检查点

### VoiceRecorder.vue 检查点

- [x] 组件使用 `<template>` 定义了录音按钮
- [x] 组件使用 `<script setup>` 定义了响应式状态
- [x] MediaRecorder API 初始化成功
- [x] `startRecording()` 方法可以正常开始录音
- [x] `stopRecording()` 方法可以正常停止录音
- [x] 录音时长使用 `setInterval` 正确更新
- [x] 麦克风权限请求逻辑正确
- [x] 错误处理覆盖了权限被拒绝情况
- [x] 组件 emits 定义了正确的事件

### RecognitionResult.vue 检查点

- [x] 组件接收 `text` prop 并正确显示
- [x] 组件接收 `loading` prop 并显示加载状态
- [x] 组件接收 `error` prop 并显示错误信息
- [x] 复制按钮功能实现正确
- [x] 编辑功能实现正确

### speechService.js 检查点

- [x] API 基础 URL 配置正确
- [x] `uploadAudio(audioBlob)` 方法实现
- [x] 请求使用 `FormData` 封装音频文件
- [x] 响应数据结构解析正确
- [x] 错误处理返回有意义的错误信息

### voiceStore.js 检查点

- [x] 定义了 `isRecording` 状态
- [x] 定义了 `recordingDuration` 状态
- [x] 定义了 `recognitionResult` 状态
- [x] 定义了 `isProcessing` 状态
- [x] 定义了 `error` 状态
- [x] Actions 方法实现正确

### VoiceInputView.vue 检查点

- [x] 页面布局使用了 Element Plus 组件
- [x] VoiceRecorder 组件正确引入和使用
- [x] RecognitionResult 组件正确引入和使用
- [x] 录音事件正确绑定到处理函数
- [x] 识别请求正确触发

## 后端检查点

### SpeechController.java 检查点

- [x] `@RestController` 注解正确添加
- [x] `@PostMapping("/recognize")` 接口定义
- [x] `@RequestParam("audio")` 正确接收文件
- [x] `@RequestParam(value = "language", defaultValue = "zh-CN")` 语言参数
- [x] 返回类型为 `ResponseEntity<?>` 正确
- [x] 错误响应使用合适的 HTTP 状态码

### SpeechRecognitionService.java 检查点

- [x] 接口定义了 `recognize(MultipartFile audio, String language)` 方法
- [x] 实现类正确处理音频文件
- [x] 音频格式转换逻辑正确（webm格式支持）
- [x] 异常处理正确

### application.yml 检查点

- [x] `spring.servlet.multipart.max-file-size` 设置为 10MB
- [x] `spring.servlet.multipart.max-request-size` 设置为 10MB
- [x] `speech.baidu.app-id` 配置存在
- [x] `speech.baidu.api-key` 配置存在
- [x] `speech.baidu.secret-key` 配置存在

### CORS 配置检查点

- [x] `WebConfig` 类实现了 `WebMvcConfigurer`
- [x] `addCorsMappings()` 方法正确配置
- [x] 允许前端开发服务器端口（如 5173, 3000）访问
- [x] 允许凭证传递
- [x] 允许的 HTTP 方法正确

## 集成检查点

- [x] 前端开发服务器可以正常启动
- [x] 后端服务可以正常启动
- [x] 前端可以成功调用后端 API
- [x] 录音功能在浏览器中正常工作
- [x] 音频文件可以成功上传到后端
- [x] 语音识别结果可以正确返回并展示
- [x] 错误信息可以正确显示给用户

## 浏览器兼容性检查点

- [x] Chrome 浏览器录音功能正常
- [x] Firefox 浏览器录音功能正常
- [x] Edge 浏览器录音功能正常
- [x] Safari 浏览器录音功能正常（如果测试）

## 用户体验检查点

- [x] 页面加载时间 < 3秒
- [x] 录音按钮响应及时
- [x] 加载状态显示清晰
- [x] 错误提示信息友好
- [x] 识别结果可以复制到剪贴板
