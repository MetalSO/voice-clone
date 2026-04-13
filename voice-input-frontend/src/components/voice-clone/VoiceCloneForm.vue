<template>
  <div class="voice-clone-container">
    <div class="clone-header">
      <h2 class="title">
        <i class="fa fa-clone"></i>
        语音克隆
      </h2>
      <p class="subtitle">上传或录制参考声音，生成克隆语音</p>
    </div>

    <div class="clone-body">
      <div class="section reference-section">
        <h3 class="section-title">
          <span class="step-number">1</span>
          参考声音
        </h3>
        
        <div class="audio-input-area" :class="{ 'has-audio': hasReferenceAudio }">
          <div v-if="!hasReferenceAudio" class="upload-area" @click="triggerFileInput" @dragover.prevent @drop.prevent="handleFileDrop">
            <input
              ref="fileInput"
              type="file"
              accept="audio/*,.wav,.mp3"
              @change="handleFileSelect"
              style="display: none"
            />
            <i class="fa fa-microphone upload-icon"></i>
            <p class="upload-text">点击上传或拖拽音频文件</p>
            <p class="upload-hint">支持 WAV、MP3 格式，建议时长 5-30 秒</p>
          </div>

          <div v-else class="audio-preview">
            <AudioPlayer :src="referenceAudioUrl" :show-download="true" />
            <button @click="clearReferenceAudio" class="btn-clear">
              <i class="fa fa-trash"></i> 重新选择
            </button>
          </div>

          <div class="record-section">
            <button 
              :class="['btn-record', { 'recording': isRecording }]"
              @click="toggleRecording"
              :disabled="isProcessing"
            >
              <i :class="isRecording ? 'fa fa-stop' : 'fa fa-circle'"></i>
              {{ isRecording ? '停止录制' : '开始录制' }}
            </button>
            <span v-if="isRecording" class="recording-time">{{ formatTime(recordingTime) }}</span>
          </div>
        </div>
      </div>

      <div class="section text-section">
        <h3 class="section-title">
          <span class="step-number">2</span>
          输入文本
        </h3>
        <textarea
          v-model="inputText"
          class="text-input"
          placeholder="输入要合成的文本内容..."
          rows="4"
          maxlength="500"
        ></textarea>
        <div class="char-count">{{ inputText.length }}/500</div>
      </div>

      <div class="section params-section">
        <h3 class="section-title">
          <span class="step-number">3</span>
          合成参数
        </h3>
        <div class="params-grid">
          <div class="param-item">
            <label>语速</label>
            <div class="slider-wrapper">
              <input type="range" v-model.number="params.speed" min="0.5" max="2" step="0.1" />
              <span class="param-value">{{ params.speed }}x</span>
            </div>
          </div>
          <div class="param-item">
            <label>音调</label>
            <div class="slider-wrapper">
              <input type="range" v-model.number="params.pitch" min="-12" max="12" step="1" />
              <span class="param-value">{{ params.pitch > 0 ? '+' : '' }}{{ params.pitch }}</span>
            </div>
          </div>
          <div class="param-item">
            <label>音量</label>
            <div class="slider-wrapper">
              <input type="range" v-model.number="params.volume" min="0" max="1" step="0.05" />
              <span class="param-value">{{ Math.round(params.volume * 100) }}%</span>
            </div>
          </div>
          <div class="param-item">
            <label>模型</label>
            <select v-model="params.model" class="model-select">
              <option value="pockettts">Pocket-TTS (推荐)</option>
              <option value="kittentts">KittenTTS</option>
              <option value="pyttsx3">pyttsx3 (基础)</option>
            </select>
          </div>
        </div>
      </div>

      <div class="action-section">
        <button 
          class="btn-generate"
          @click="generateClonedVoice"
          :disabled="!canGenerate || isProcessing"
        >
          <i v-if="!isProcessing" class="fa fa-magic"></i>
          <i v-else class="fa fa-spinner fa-spin"></i>
          {{ isProcessing ? '合成中...' : '生成克隆语音' }}
        </button>
      </div>

      <div v-if="resultAudioUrl || errorMessage" class="result-section">
        <h3 class="section-title">
          <span class="step-number">4</span>
          合成结果
        </h3>
        
        <div v-if="errorMessage" class="error-message">
          <i class="fa fa-exclamation-triangle"></i>
          {{ errorMessage }}
        </div>

        <div v-if="resultAudioUrl" class="result-audio">
          <AudioPlayer :src="resultAudioUrl" :show-download="true" />
          <div class="result-actions">
            <button @click="downloadResult" class="btn-download">
              <i class="fa fa-download"></i> 下载音频
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onUnmounted } from 'vue'
import AudioPlayer from './AudioPlayer.vue'
import { voiceCloneService } from '../../services/voiceCloneService'

const emit = defineEmits(['status-change', 'error', 'success'])

const fileInput = ref(null)
const inputText = ref('')
const hasReferenceAudio = ref(false)
const referenceAudioBlob = ref(null)
const referenceAudioUrl = ref('')
const resultAudioUrl = ref('')
const errorMessage = ref('')

const isRecording = ref(false)
const recordingTime = ref(0)
const mediaRecorder = ref(null)
const recordingInterval = ref(null)

const isProcessing = ref(false)

const params = ref({
  speed: 1.0,
  pitch: 0,
  volume: 1.0,
  model: 'kittentts'
})

let audioChunks = []

const canGenerate = computed(() => {
  return hasReferenceAudio.value && inputText.value.trim().length > 0
})

const triggerFileInput = () => {
  fileInput.value?.click()
}

const handleFileSelect = async (event) => {
  const file = event.target.files[0]
  if (file) {
    await processAudioFile(file)
  }
}

const handleFileDrop = async (event) => {
  const file = event.dataTransfer.files[0]
  if (file && file.type.startsWith('audio/')) {
    await processAudioFile(file)
  }
}

const createWavBlob = (audioChunks, sampleRate) => {
  const wavHeaderSize = 44
  const totalDataLen = audioChunks.reduce((acc, chunk) => acc + chunk.length, 0) * 2
  const buffer = new ArrayBuffer(wavHeaderSize + totalDataLen)
  const view = new DataView(buffer)

  // RIFF header
  writeString(view, 0, 'RIFF')
  view.setUint32(4, 36 + totalDataLen, true)
  writeString(view, 8, 'WAVE')
  // fmt chunk
  writeString(view, 12, 'fmt ')
  view.setUint32(16, 16, true)
  view.setUint16(20, 1, true) // PCM
  view.setUint16(22, 1, true) // Mono
  view.setUint32(24, sampleRate, true)
  view.setUint32(28, sampleRate * 2, true) // Byte rate
  view.setUint16(32, 2, true) // Block align
  view.setUint16(34, 16, true) // Bits per sample
  // data chunk
  writeString(view, 36, 'data')
  view.setUint32(40, totalDataLen, true)

  let offset = 44
  for (const chunk of audioChunks) {
    for (let i = 0; i < chunk.length; i++) {
      const sample = Math.max(-1, Math.min(1, chunk[i]))
      view.setInt16(offset, sample < 0 ? sample * 0x8000 : sample * 0x7FFF, true)
      offset += 2
    }
  }

  return new Blob([buffer], { type: 'audio/wav' })
}

const writeString = (view, offset, str) => {
  for (let i = 0; i < str.length; i++) {
    view.setUint8(offset + i, str.charCodeAt(i))
  }
}

const processAudioFile = async (file) => {
  try {
    const url = URL.createObjectURL(file)
    referenceAudioBlob.value = file
    referenceAudioUrl.value = url
    hasReferenceAudio.value = true
    errorMessage.value = ''
  } catch (err) {
    errorMessage.value = '文件处理失败: ' + err.message
  }
}

const clearReferenceAudio = () => {
  if (referenceAudioUrl.value) {
    URL.revokeObjectURL(referenceAudioUrl.value)
  }
  referenceAudioBlob.value = null
  referenceAudioUrl.value = ''
  hasReferenceAudio.value = false
  if (fileInput.value) {
    fileInput.value.value = ''
  }
}

const toggleRecording = async () => {
  if (isRecording.value) {
    stopRecording()
  } else {
    await startRecording()
  }
}

const startRecording = async () => {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true })

    mediaRecorder.value = new MediaRecorder(stream, { mimeType: 'audio/webm' })
    audioChunks = []

    mediaRecorder.value.ondataavailable = (event) => {
      if (event.data.size > 0) {
        audioChunks.push(event.data)
      }
    }

    mediaRecorder.value.onstop = () => {
      const blob = new Blob(audioChunks, { type: 'audio/webm' })
      processAudioFile(blob)
      stream.getTracks().forEach(track => track.stop())
    }

    mediaRecorder.value.start()
    isRecording.value = true
    recordingTime.value = 0

    recordingInterval.value = setInterval(() => {
      recordingTime.value++
    }, 1000)

  } catch (err) {
    errorMessage.value = '无法访问麦克风: ' + err.message
  }
}

const stopRecording = () => {
  if (mediaRecorder.value && mediaRecorder.value.state !== 'inactive') {
    mediaRecorder.value.stop()
  }

  isRecording.value = false

  if (recordingInterval.value) {
    clearInterval(recordingInterval.value)
    recordingInterval.value = null
  }
}

const formatTime = (seconds) => {
  const mins = Math.floor(seconds / 60)
  const secs = seconds % 60
  return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
}

const generateClonedVoice = async () => {
  if (!canGenerate.value) return

  isProcessing.value = true
  errorMessage.value = ''
  resultAudioUrl.value = ''
  
  emit('status-change', 'processing')

  try {
    const formData = new FormData()
    formData.append('audio', referenceAudioBlob.value, 'reference_audio.webm')
    formData.append('text', inputText.value)
    formData.append('speed', params.value.speed.toString())
    formData.append('pitch', params.value.pitch.toString())
    formData.append('volume', params.value.volume.toString())
    formData.append('model', params.value.model)

    const response = await voiceCloneService.cloneVoice(formData)

    if (response.status === 'success' && response.audio_path) {
      resultAudioUrl.value = `http://localhost:8080/${response.audio_path}`
      emit('success', '语音克隆成功')
    } else {
      throw new Error(response.message || '合成失败')
    }

  } catch (err) {
    errorMessage.value = err.message || '语音克隆失败，请重试'
    emit('error', err.message)
  } finally {
    isProcessing.value = false
    emit('status-change', 'idle')
  }
}

const downloadResult = () => {
  if (resultAudioUrl.value) {
    const link = document.createElement('a')
    link.href = resultAudioUrl.value
    link.download = `cloned_voice_${Date.now()}.wav`
    link.click()
  }
}

onUnmounted(() => {
  stopRecording()
  clearReferenceAudio()
})
</script>

<style scoped>
.voice-clone-container {
  background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
  border-radius: 24px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
  padding: 24px;
}

.clone-header {
  margin-bottom: 24px;
}

.title {
  font-size: 20px;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 6px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.title i {
  color: #6366f1;
}

.subtitle {
  font-size: 14px;
  color: #64748b;
  margin: 0;
}

.clone-body {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.section {
  background: #f8fafc;
  border-radius: 16px;
  padding: 20px;
}

.section-title {
  font-size: 16px;
  font-weight: 600;
  color: #334155;
  margin: 0 0 16px 0;
  display: flex;
  align-items: center;
  gap: 10px;
}

.step-number {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  color: white;
  font-size: 13px;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
}

.audio-input-area {
  border: 2px dashed #cbd5e1;
  border-radius: 12px;
  padding: 20px;
  transition: all 0.3s ease;
}

.audio-input-area.has-audio {
  border-style: solid;
  border-color: #6366f1;
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.05), rgba(139, 92, 246, 0.05));
}

.upload-area {
  cursor: pointer;
  text-align: center;
  padding: 30px;
}

.upload-icon {
  font-size: 40px;
  color: #94a3b8;
  margin-bottom: 12px;
}

.upload-text {
  font-size: 15px;
  color: #475569;
  margin: 0 0 6px 0;
}

.upload-hint {
  font-size: 13px;
  color: #94a3b8;
  margin: 0;
}

.audio-preview {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.btn-clear {
  padding: 8px 16px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  background: white;
  color: #64748b;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s ease;
  align-self: flex-start;
}

.btn-clear:hover {
  background: #fef2f2;
  border-color: #fecaca;
  color: #ef4444;
}

.record-section {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid #e2e8f0;
}

.btn-record {
  padding: 10px 20px;
  border: none;
  border-radius: 10px;
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  color: white;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
}

.btn-record:hover:not(:disabled) {
  transform: scale(1.02);
  box-shadow: 0 4px 20px rgba(99, 102, 241, 0.4);
}

.btn-record.recording {
  background: linear-gradient(135deg, #ef4444 0%, #f97316 100%);
  animation: pulse 1.5s infinite;
}

@keyframes pulse {
  0%, 100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.4); }
  50% { box-shadow: 0 0 0 10px rgba(239, 68, 68, 0); }
}

.recording-time {
  font-family: monospace;
  font-size: 14px;
  font-weight: 600;
  color: #ef4444;
}

.text-input {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  font-size: 14px;
  resize: vertical;
  transition: border-color 0.2s ease;
}

.text-input:focus {
  outline: none;
  border-color: #6366f1;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

.char-count {
  text-align: right;
  font-size: 12px;
  color: #94a3b8;
  margin-top: 6px;
}

.params-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.param-item label {
  display: block;
  font-size: 13px;
  font-weight: 500;
  color: #475569;
  margin-bottom: 8px;
}

.slider-wrapper {
  display: flex;
  align-items: center;
  gap: 10px;
}

.slider-wrapper input[type="range"] {
  flex: 1;
  height: 6px;
  -webkit-appearance: none;
  appearance: none;
  background: #e2e8f0;
  border-radius: 3px;
  outline: none;
}

.slider-wrapper input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  cursor: pointer;
}

.param-value {
  font-size: 13px;
  font-weight: 600;
  color: #6366f1;
  min-width: 45px;
  text-align: right;
}

.model-select {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 14px;
  background: white;
  cursor: pointer;
}

.action-section {
  padding: 0 4px;
}

.btn-generate {
  width: 100%;
  padding: 14px 24px;
  border: none;
  border-radius: 12px;
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  color: white;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}

.btn-generate:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(99, 102, 241, 0.35);
}

.btn-generate:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.error-message {
  padding: 12px 16px;
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 10px;
  color: #dc2626;
  font-size: 14px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.result-audio {
  padding: 16px;
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.05), rgba(139, 92, 246, 0.05));
  border-radius: 12px;
}

.result-actions {
  display: flex;
  gap: 10px;
  margin-top: 12px;
}

.btn-download {
  padding: 8px 16px;
  border: 1px solid #6366f1;
  border-radius: 8px;
  background: white;
  color: #6366f1;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 6px;
}

.btn-download:hover {
  background: #6366f1;
  color: white;
}

@media (max-width: 768px) {
  .params-grid {
    grid-template-columns: 1fr;
  }
}
</style>
