<template>
  <div class="voice-input-panel">
    <div class="flex items-center justify-between mb-6">
      <h2 class="text-xl font-semibold text-gray-800">语音输入</h2>
      <div class="flex space-x-2">
        <button
          id="btn-mic-toggle"
          class="voice-btn flex items-center justify-center"
          :class="{ 'listening': isListening }"
          @click="toggleVoiceInput"
        >
          <div class="wave-animation" v-for="n in 3" :key="n" :class="{ 'hidden': !isListening }"></div>
          <i class="fa fa-microphone mic-icon text-white text-xl relative z-10"></i>
        </button>
      </div>
    </div>

    <div id="voice-status" class="mb-4 p-4 rounded-xl" :class="statusClass">
      <div class="flex items-center">
        <i :class="statusIcon" class="mr-3"></i>
        <p :class="statusTextClass">{{ statusMessage }}</p>
      </div>
      <div v-if="isListening && interimTranscript" class="mt-2 p-2 rounded-lg bg-white/50 text-sm">
        {{ interimTranscript }}<span class="animate-pulse">|</span>
      </div>
    </div>

    <div v-show="transcriptText" id="transcript-result" class="mb-4">
      <label class="block text-sm font-medium text-gray-700 mb-2">识别结果</label>
      <div class="p-4 rounded-xl bg-gradient-to-r from-indigo-50 to-purple-50 border border-indigo-100">
        <p class="transcript-text text-gray-800 leading-relaxed">{{ transcriptText }}</p>
      </div>
    </div>

    <div class="mb-4">
      <label class="block text-sm font-medium text-gray-700 mb-2">文本输入</label>
      <textarea
        v-model="inputText"
        class="w-full px-4 py-3 rounded-xl border border-gray-200 focus:border-primary focus:ring-2 focus:ring-indigo-100 transition-all outline-none"
        rows="4"
        placeholder="输入要转换的文本..."
      ></textarea>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">语音模型</label>
        <select
          v-model="synthesizeModel"
          class="w-full px-4 py-3 rounded-xl border border-gray-200 focus:border-primary focus:ring-2 focus:ring-indigo-100 transition-all outline-none"
        >
          <option v-for="(model, key) in availableModels" :key="key" :value="key" :disabled="!model.available">
            {{ model.name }} ({{ model.description }}){{ !model.available ? ' [不可用]' : '' }}
          </option>
        </select>
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">语言</label>
        <select
          v-model="synthesizeLanguage"
          class="w-full px-4 py-3 rounded-xl border border-gray-200 focus:border-primary focus:ring-2 focus:ring-indigo-100 transition-all outline-none"
        >
          <option value="zh-CN">中文</option>
          <option value="en-US">英文</option>
        </select>
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">语音</label>
        <select
          v-model="synthesizeGender"
          class="w-full px-4 py-3 rounded-xl border border-gray-200 focus:border-primary focus:ring-2 focus:ring-indigo-100 transition-all outline-none"
        >
          <option value="female">女声</option>
          <option value="male">男声</option>
        </select>
      </div>
    </div>

    <div class="flex flex-wrap gap-3">
      <button
        @click="synthesizeSpeech"
        :disabled="isSynthesizing || !inputText.trim()"
        class="flex-1 min-w-[140px] px-6 py-3 bg-gradient-to-r from-primary to-secondary text-white rounded-xl font-medium hover:shadow-lg hover:shadow-indigo-200 transition-all flex items-center justify-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        <i class="fa fa-volume-up"></i>
        <span>{{ isSynthesizing ? '合成中...' : '语音合成' }}</span>
      </button>
      <button
        @click="clearAll"
        class="px-6 py-3 bg-gray-100 text-gray-700 rounded-xl font-medium hover:bg-gray-200 transition-all flex items-center justify-center space-x-2"
      >
        <i class="fa fa-refresh"></i>
        <span>清空</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { speechService } from '../services/speechService'

const inputText = ref('')
const transcriptText = ref('')
const interimTranscript = ref('')
const isListening = ref(false)
const isSynthesizing = ref(false)
const synthesizeModel = ref('pyttsx3')
const synthesizeLanguage = ref('zh-CN')
const synthesizeGender = ref('female')
const availableModels = ref({
  pyttsx3: { available: true, name: 'pyttsx3', description: '本地语音合成' },
  gtts: { available: true, name: 'gTTS', description: 'Google Text-to-Speech' },
  coqui: { available: false, name: 'Coqui TTS', description: '开源高质量语音合成' },
  azure: { available: false, name: 'Azure Speech Service', description: '高质量云服务语音合成' }
})

let recognition = null
let recordingInterval = null

const statusMessage = ref('点击麦克风按钮开始语音输入')
const statusType = ref('info')

const statusClass = computed(() => {
  if (statusType.value === 'error') return 'bg-red-50 border border-red-100'
  if (statusType.value === 'listening') return 'bg-green-50 border border-green-100'
  return 'bg-indigo-50 border border-indigo-100'
})

const statusIcon = computed(() => {
  if (statusType.value === 'error') return 'fa fa-exclamation-circle text-red-500'
  if (statusType.value === 'listening') return 'fa fa-microphone text-green-500 animate-pulse'
  return 'fa fa-info-circle text-indigo-500'
})

const statusTextClass = computed(() => {
  if (statusType.value === 'error') return 'text-red-700'
  if (statusType.value === 'listening') return 'text-green-700'
  return 'text-indigo-700'
})

const toggleVoiceInput = () => {
  if (isListening.value) {
    stopListening()
  } else {
    startListening()
  }
}

const startListening = () => {
  if (!recognition) {
    statusMessage.value = '浏览器不支持语音识别'
    statusType.value = 'error'
    return
  }

  isListening.value = true
  statusMessage.value = '正在聆听...'
  statusType.value = 'listening'
  interimTranscript.value = ''
  emit('listening-change', true)

  try {
    recognition.start()
  } catch (e) {
    console.error('Recognition start error:', e)
    stopListening()
  }
}

const stopListening = () => {
  isListening.value = false
  statusMessage.value = '点击麦克风按钮开始语音输入'
  statusType.value = 'info'
  interimTranscript.value = ''
  emit('listening-change', false)

  if (recognition) {
    try {
      recognition.stop()
    } catch (e) {
      console.error('Recognition stop error:', e)
    }
  }

  if (recordingInterval) {
    clearInterval(recordingInterval)
  }
}

const synthesizeSpeech = async () => {
  if (!inputText.value.trim()) {
    emit('show-error', '请输入要合成的文本')
    return
  }

  isSynthesizing.value = true
  emit('update-status', '正在合成语音...', 'loading')

  try {
    const response = await speechService.synthesize(
      inputText.value,
      synthesizeModel.value,
      synthesizeLanguage.value,
      synthesizeGender.value
    )

    if (response.status === 'success' && response.audio_path) {
      const audioUrl = `http://localhost:8080/${response.audio_path}`
      emit('update-status', '合成成功', 'success')
      emit('show-result', `音频文件路径: ${response.audio_path}`)
      emit('play-audio', audioUrl)
      emit('add-history', '语音合成', inputText.value.substring(0, 50) + (inputText.value.length > 50 ? '...' : ''))
    } else {
      throw new Error(response.message || '合成失败')
    }
  } catch (err) {
    emit('update-status', '合成失败', 'error')
    emit('show-error', err.message || '语音合成失败')
    emit('add-history', '语音合成', `错误: ${err.message}`)
  } finally {
    isSynthesizing.value = false
  }
}

const clearAll = () => {
  inputText.value = ''
  transcriptText.value = ''
  interimTranscript.value = ''
  emit('reset-result')
  stopListening()
}

const loadModels = async () => {
  try {
    const data = await speechService.getModels()
    if (data && data.models) {
      availableModels.value = data.models
      const firstAvailable = Object.keys(data.models).find(key => data.models[key].available)
      if (firstAvailable) {
        synthesizeModel.value = firstAvailable
      }
    }
  } catch (error) {
    console.error('Error loading models:', error)
    emit('show-error', '加载模型列表失败: ' + (error.message || '请检查后端服务是否启动'))
  }
}

const initSpeechRecognition = () => {
  if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
    recognition = new SpeechRecognition()
    recognition.continuous = true
    recognition.interimResults = true
    recognition.lang = synthesizeLanguage.value || 'zh-CN'

    recognition.onresult = (event) => {
      let finalTranscript = ''
      let interim = ''

      for (let i = event.resultIndex; i < event.results.length; i++) {
        const transcript = event.results[i][0].transcript
        if (event.results[i].isFinal) {
          finalTranscript += transcript
        } else {
          interim += transcript
        }
      }

      if (finalTranscript) {
        inputText.value += finalTranscript
        transcriptText.value = inputText.value
      }

      interimTranscript.value = interim
    }

    recognition.onerror = (event) => {
      console.error('Speech recognition error:', event.error)
      if (event.error === 'not-allowed') {
        statusMessage.value = '麦克风权限被拒绝，请允许访问'
        statusType.value = 'error'
      } else if (event.error !== 'no-speech') {
        statusMessage.value = '识别出错: ' + event.error
        statusType.value = 'error'
      }
      stopListening()
    }

    recognition.onend = () => {
      if (isListening.value) {
        try {
          recognition.start()
        } catch (e) {
          console.error('Failed to restart recognition:', e)
        }
      }
    }
  }
}

const emit = defineEmits(['update-status', 'show-error', 'show-result', 'play-audio', 'add-history', 'reset-result', 'listening-change'])

onMounted(() => {
  initSpeechRecognition()
  loadModels()
})

onUnmounted(() => {
  stopListening()
})
</script>

<style scoped>
.voice-btn {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  box-shadow: 0 8px 32px rgba(99, 102, 241, 0.4);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.voice-btn::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle, rgba(255,255,255,0.3) 0%, transparent 70%);
  transform: translate(-50%, -50%) scale(0);
  transition: transform 0.5s ease;
}

.voice-btn:hover::before {
  transform: translate(-50%, -50%) scale(1.5);
}

.voice-btn:hover {
  transform: scale(1.1);
  box-shadow: 0 12px 40px rgba(99, 102, 241, 0.6);
}

.voice-btn.listening {
  background: linear-gradient(135deg, #ef4444 0%, #f97316 100%);
  animation: pulse-ring 1.5s cubic-bezier(0.215, 0.61, 0.355, 1) infinite;
}

@keyframes pulse-ring {
  0% {
    transform: scale(1);
    box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7);
  }
  50% {
    transform: scale(1.05);
  }
  100% {
    transform: scale(1);
    box-shadow: 0 0 0 20px rgba(239, 68, 68, 0);
  }
}

.wave-animation {
  position: absolute;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: rgba(99, 102, 241, 0.3);
  animation: wave 2s ease-out infinite;
}

.listening .wave-animation:nth-child(2) {
  animation-delay: 0.5s;
}

.listening .wave-animation:nth-child(3) {
  animation-delay: 1s;
}

@keyframes wave {
  0% {
    transform: scale(1);
    opacity: 0.5;
  }
  100% {
    transform: scale(2);
    opacity: 0;
  }
}

.mic-icon {
  animation: none;
}

.listening .mic-icon {
  animation: bounce 1s infinite;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-5px); }
}

.transcript-text {
  white-space: pre-wrap;
  word-break: break-word;
}

@media (max-width: 768px) {
  .voice-btn {
    width: 56px;
    height: 56px;
  }
}
</style>
