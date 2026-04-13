<template>
  <div class="voice-recorder">
    <div class="recorder-status">
      <el-tag :type="statusType" size="large">{{ statusText }}</el-tag>
    </div>
    
    <div class="recorder-visualization">
      <div class="wave-container" :class="{ active: isRecording }">
        <div v-for="i in 20" :key="i" class="wave-bar" :style="getWaveStyle(i)"></div>
      </div>
    </div>
    
    <div class="recorder-time" v-if="isRecording || recordedTime > 0">
      <span class="time">{{ formatTime(recordedTime) }}</span>
    </div>
    
    <div class="recorder-controls">
      <el-button 
        :type="isRecording ? 'danger' : 'primary'" 
        :icon="isRecording ? 'VideoPause' : 'Microphone'"
        size="large"
        circle
        @click="toggleRecording"
        :disabled="!isSupported"
      >
      </el-button>
      
      <el-button 
        v-if="recordedTime > 0 && !isRecording"
        type="success" 
        icon="Check"
        circle
        @click="confirmRecording"
      >
      </el-button>
      
      <el-button 
        v-if="recordedTime > 0 && !isRecording"
        type="warning" 
        icon="Refresh"
        circle
        @click="resetRecording"
      >
      </el-button>
    </div>
    
    <div class="recorder-hint" v-if="!isSupported">
      <el-alert type="error" :closable="false">
        您的浏览器不支持语音录制功能，请使用 Chrome 或 Firefox。
      </el-alert>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { ElMessage } from 'element-plus'

const isRecording = ref(false)
const recordedTime = ref(0)
const mediaRecorder = ref(null)
const audioChunks = ref([])
const timer = ref(null)
const isSupported = ref(false)

const statusText = computed(() => {
  if (!isSupported.value) return '不支持'
  if (isRecording.value) return '录音中'
  if (recordedTime.value > 0) return '录音完成'
  return '就绪'
})

const statusType = computed(() => {
  if (!isSupported.value) return 'info'
  if (isRecording.value) return 'danger'
  if (recordedTime.value > 0) return 'success'
  return 'info'
})

const getWaveStyle = (index) => {
  if (!isRecording.value) {
    return { height: '20px' }
  }
  const height = Math.random() * 60 + 20
  return { height: `${height}px` }
}

const formatTime = (seconds) => {
  const mins = Math.floor(seconds / 60)
  const secs = seconds % 60
  return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
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
    mediaRecorder.value = new MediaRecorder(stream)
    audioChunks.value = []
    
    mediaRecorder.value.ondataavailable = (event) => {
      audioChunks.value.push(event.data)
    }
    
    mediaRecorder.value.onstop = () => {
      stream.getTracks().forEach(track => track.stop())
    }
    
    mediaRecorder.value.start()
    isRecording.value = true
    
    timer.value = setInterval(() => {
      recordedTime.value++
    }, 1000)
    
    ElMessage.success('开始录音')
  } catch (error) {
    ElMessage.error('无法访问麦克风，请检查权限设置')
    console.error('录音错误:', error)
  }
}

const stopRecording = () => {
  if (mediaRecorder.value && isRecording.value) {
    mediaRecorder.value.stop()
    isRecording.value = false
    clearInterval(timer.value)
    ElMessage.info('录音已停止')
  }
}

const emit = defineEmits(['recording-complete'])

const confirmRecording = () => {
  const audioBlob = new Blob(audioChunks.value, { type: 'audio/webm' })
  emit('recording-complete', audioBlob)
}

const resetRecording = () => {
  audioChunks.value = []
  recordedTime.value = 0
}

onMounted(() => {
  isSupported.value = !!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia)
})

onUnmounted(() => {
  if (timer.value) {
    clearInterval(timer.value)
  }
  if (mediaRecorder.value && isRecording.value) {
    mediaRecorder.value.stop()
  }
})
</script>

<style scoped>
.voice-recorder {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 40px;
  background: white;
  border-radius: 20px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
  max-width: 500px;
  margin: 0 auto;
}

.recorder-status {
  margin-bottom: 30px;
}

.recorder-visualization {
  width: 100%;
  height: 100px;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 20px;
}

.wave-container {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  height: 100%;
}

.wave-bar {
  width: 6px;
  background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
  border-radius: 3px;
  transition: height 0.1s ease;
}

.wave-container.active .wave-bar {
  animation: wave 0.5s ease-in-out infinite;
}

.wave-container.active .wave-bar:nth-child(odd) {
  animation-delay: 0.1s;
}

@keyframes wave {
  0%, 100% { transform: scaleY(1); }
  50% { transform: scaleY(0.5); }
}

.recorder-time {
  margin-bottom: 30px;
}

.time {
  font-size: 48px;
  font-weight: 300;
  color: #333;
  font-family: 'Roboto Mono', monospace;
}

.recorder-controls {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
}

.recorder-hint {
  width: 100%;
  margin-top: 20px;
}
</style>
