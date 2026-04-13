<template>
  <div class="audio-player-wrapper">
    <div class="player-container" :class="{ 'playing': isPlaying }">
      <button class="btn-play" @click="togglePlay" :disabled="!src">
        <i :class="isPlaying ? 'fa fa-pause' : 'fa fa-play'"></i>
      </button>

      <div class="player-info">
        <div class="waveform-visual" ref="waveformRef">
          <div
            v-for="(bar, index) in waveformBars"
            :key="index"
            class="wave-bar"
            :style="{ height: bar + '%' }"
          ></div>
        </div>
        
        <div class="time-display">
          <span class="current-time">{{ formatTime(currentTime) }}</span>
          <input 
            type="range" 
            v-model.number="currentTime" 
            :max="duration || 0"
            @input="seekTo"
            class="progress-slider"
          />
          <span class="total-time">{{ formatTime(duration) }}</span>
        </div>
      </div>

      <div class="player-controls">
        <button @click="changeVolume(-0.1)" class="btn-control" title="降低音量">
          <i class="fa fa-volume-down"></i>
        </button>
        <div class="volume-bar">
          <input 
            type="range" 
            v-model.number="volume" 
            min="0" 
            max="1" 
            step="0.05"
            class="volume-slider"
          />
        </div>
        <button @click="changeVolume(0.1)" class="btn-control" title="增加音量">
          <i class="fa fa-volume-up"></i>
        </button>
        <button v-if="showDownload" @click="$emit('download')" class="btn-control btn-download" title="下载">
          <i class="fa fa-download"></i>
        </button>
      </div>
    </div>

    <audio 
      ref="audioRef" 
      :src="src"
      @timeupdate="onTimeUpdate"
      @loadedmetadata="onLoadedMetadata"
      @ended="onEnded"
      @error="onError"
      preload="metadata"
    ></audio>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  src: {
    type: String,
    default: ''
  },
  showDownload: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['play', 'pause', 'download', 'error'])

const audioRef = ref(null)
const waveformRef = ref(null)

const isPlaying = ref(false)
const currentTime = ref(0)
const duration = ref(0)
const volume = ref(0.8)

const waveformBars = computed(() => {
  if (!isPlaying.value) {
    return Array.from({ length: 40 }, () => 10)
  }
  
  const bars = []
  for (let i = 0; i < 40; i++) {
    bars.push(Math.random() * 80 + 20)
  }
  return bars
})

const togglePlay = () => {
  if (!audioRef.value || !props.src) return

  if (isPlaying.value) {
    audioRef.value.pause()
  } else {
    audioRef.value.play()
  }
}

const seekTo = () => {
  if (audioRef.value) {
    audioRef.value.currentTime = currentTime.value
  }
}

const changeVolume = (delta) => {
  const newVolume = Math.max(0, Math.min(1, volume.value + delta))
  volume.value = newVolume
  if (audioRef.value) {
    audioRef.value.volume = newVolume
  }
}

const onTimeUpdate = () => {
  if (audioRef.value) {
    currentTime.value = audioRef.value.currentTime
  }
}

const onLoadedMetadata = () => {
  if (audioRef.value) {
    duration.value = audioRef.value.duration
  }
}

const onEnded = () => {
  isPlaying.value = false
  currentTime.value = 0
}

const onError = (e) => {
  console.error('Audio error:', e)
  emit('error', e)
}

const formatTime = (seconds) => {
  if (!seconds || isNaN(seconds)) return '0:00'
  const mins = Math.floor(seconds / 60)
  const secs = Math.floor(seconds % 60)
  return `${mins}:${secs.toString().padStart(2, '0')}`
}

let playInterval = null

const startWaveAnimation = () => {
  playInterval = setInterval(() => {
    if (waveformRef.value && isPlaying.value) {
      const bars = waveformRef.value.querySelectorAll('.wave-bar')
      bars.forEach(bar => {
        bar.style.height = (Math.random() * 80 + 20) + '%'
      })
    }
  }, 100)
}

const stopWaveAnimation = () => {
  if (playInterval) {
    clearInterval(playInterval)
    playInterval = null
  }
}

onMounted(() => {
  if (audioRef.value) {
    audioRef.value.volume = volume.value
    
    audioRef.value.addEventListener('play', () => {
      isPlaying.value = true
      emit('play')
      startWaveAnimation()
    })

    audioRef.value.addEventListener('pause', () => {
      isPlaying.value = false
      emit('pause')
      stopWaveAnimation()
    })
  }
})

onUnmounted(() => {
  stopWaveAnimation()
})
</script>

<style scoped>
.audio-player-wrapper {
  width: 100%;
}

.player-container {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 14px 18px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  border: 1px solid #e2e8f0;
  transition: all 0.3s ease;
}

.player-container.playing {
  border-color: #6366f1;
  box-shadow: 0 4px 20px rgba(99, 102, 241, 0.15);
}

.btn-play {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  border: none;
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  color: white;
  font-size: 16px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  flex-shrink: 0;
}

.btn-play:hover:not(:disabled) {
  transform: scale(1.05);
  box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4);
}

.btn-play:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.player-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
  min-width: 0;
}

.waveform-visual {
  display: flex;
  align-items: center;
  gap: 2px;
  height: 28px;
  padding: 0 4px;
}

.wave-bar {
  flex: 1;
  min-width: 2px;
  max-width: 8px;
  background: linear-gradient(to top, #6366f1, #a78bfa);
  border-radius: 2px;
  transition: height 0.1s ease;
}

.time-display {
  display: flex;
  align-items: center;
  gap: 10px;
}

.current-time,
.total-time {
  font-size: 11px;
  font-weight: 600;
  color: #64748b;
  min-width: 35px;
  text-align: center;
}

.progress-slider {
  flex: 1;
  height: 4px;
  -webkit-appearance: none;
  appearance: none;
  background: #e2e8f0;
  border-radius: 2px;
  outline: none;
  cursor: pointer;
}

.progress-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #6366f1;
  cursor: pointer;
}

.player-controls {
  display: flex;
  align-items: center;
  gap: 6px;
  flex-shrink: 0;
}

.btn-control {
  width: 30px;
  height: 30px;
  border: none;
  border-radius: 6px;
  background: transparent;
  color: #64748b;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-control:hover {
  background: #f1f5f9;
  color: #6366f1;
}

.btn-download:hover {
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  color: white;
}

.volume-bar {
  width: 60px;
}

.volume-slider {
  width: 100%;
  height: 3px;
  -webkit-appearance: none;
  appearance: none;
  background: #e2e8f0;
  border-radius: 2px;
  outline: none;
  cursor: pointer;
}

.volume-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #64748b;
  cursor: pointer;
}
</style>
