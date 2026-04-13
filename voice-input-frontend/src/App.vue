<template>
  <div class="min-h-screen flex flex-col">
    <nav class="glass-card shadow-lg">
      <div class="container mx-auto px-4 py-4 flex justify-between items-center">
        <div class="flex items-center space-x-3">
          <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-primary to-secondary flex items-center justify-center">
            <i class="fa fa-microphone text-white text-lg"></i>
          </div>
          <div>
            <h1 class="text-xl font-bold bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent">语音处理服务</h1>
            <p class="text-xs text-gray-500">Voice Processing Service</p>
          </div>
        </div>
        <div class="flex items-center space-x-4">
          <span class="hidden sm:inline-flex items-center px-3 py-1 rounded-full bg-green-100 text-green-700 text-sm">
            <span class="w-2 h-2 rounded-full bg-green-500 mr-2 animate-pulse"></span>
            服务正常
          </span>
        </div>
      </div>
    </nav>

    <main class="flex-1 container mx-auto px-4 py-8">
      <div class="grid grid-cols-1 lg:grid-cols-5 gap-6 h-full">
        <div class="lg:col-span-3 space-y-6">
          <div class="input-panel p-6">
            <VoiceInputView
              ref="voiceInputRef"
              @update-status="handleUpdateStatus"
              @show-error="handleShowError"
              @show-result="handleShowResult"
              @play-audio="handlePlayAudio"
              @add-history="handleAddHistory"
              @reset-result="handleResetResult"
              @listening-change="isListening = $event"
            />
          </div>

          <div class="input-panel p-6">
            <VoiceCloneForm
              @status-change="handleCloneStatusChange"
              @error="handleShowError"
              @success="handleCloneSuccess"
            />
          </div>
        </div>

        <div class="lg:col-span-2">
          <ResultDisplay
            :status-message="statusMessage"
            :status-type="statusType"
            :result-text="resultText"
            :audio-url="audioUrl"
            :error-message="errorMessage"
            :history-items="historyItems"
            @dismiss-error="handleDismissError"
          />
        </div>
      </div>
    </main>

    <footer class="glass-card mt-auto">
      <div class="container mx-auto px-4 py-4 text-center text-gray-600 text-sm">
        <p>© 2026 语音处理服务 | 版本 2.0.0</p>
      </div>
    </footer>

    <div class="floating-btn">
      <button
        class="voice-btn flex items-center justify-center"
        :class="{ 'listening': isListening }"
        @click="$refs.voiceInputRef?.toggleVoiceInput()"
      >
        <div class="wave-animation" v-for="n in 3" :key="n" :class="{ 'hidden': !isListening }"></div>
        <i class="fa fa-microphone mic-icon text-white text-2xl relative z-10"></i>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import VoiceInputView from './views/VoiceInputView.vue'
import VoiceCloneForm from './components/voice-clone/VoiceCloneForm.vue'
import ResultDisplay from './components/ResultDisplay.vue'

const statusMessage = ref('等待操作...')
const statusType = ref('info')
const resultText = ref('')
const audioUrl = ref('')
const errorMessage = ref('')
const historyItems = ref([])
const isListening = ref(false)

const handleUpdateStatus = (message, type) => {
  statusMessage.value = message
  statusType.value = type || 'info'
}

const handleShowError = (message) => {
  errorMessage.value = message
  statusType.value = 'error'
}

const handleShowResult = (data) => {
  resultText.value = data
}

const handlePlayAudio = (url) => {
  audioUrl.value = url
}

const handleAddHistory = (action, result) => {
  const timestamp = new Date().toLocaleTimeString()
  historyItems.value.unshift({ timestamp, action, result })
  if (historyItems.value.length > 10) {
    historyItems.value = historyItems.value.slice(0, 10)
  }
}

const handleResetResult = () => {
  resultText.value = ''
  audioUrl.value = ''
  errorMessage.value = ''
  statusMessage.value = '等待操作...'
  statusType.value = 'info'
}

const handleDismissError = () => {
  errorMessage.value = ''
  if (statusType.value === 'error') {
    statusType.value = 'info'
    statusMessage.value = '等待操作...'
  }
}

const handleCloneStatusChange = (status) => {
  if (status === 'processing') {
    statusMessage.value = '正在生成克隆语音...'
    statusType.value = 'loading'
  } else if (status === 'idle') {
    statusMessage.value = '等待操作...'
    statusType.value = 'info'
  }
}

const handleCloneSuccess = (message) => {
  handleAddHistory('语音克隆', message)
}
</script>

<style>
body {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.glass-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.input-panel {
  background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
  border-radius: 24px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
}

.voice-btn {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  box-shadow: 0 8px 32px rgba(99, 102, 241, 0.4);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  border: none;
  cursor: pointer;
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

.floating-btn {
  position: fixed;
  bottom: 32px;
  right: 32px;
  z-index: 1000;
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

@media (max-width: 768px) {
  .floating-btn {
    bottom: 20px;
    right: 20px;
  }

  .voice-btn {
    width: 56px;
    height: 56px;
  }
}
</style>
