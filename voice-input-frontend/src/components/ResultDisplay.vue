<template>
  <div class="result-display-panel p-6 sticky top-6">
    <div class="flex items-center justify-between mb-6">
      <h2 class="text-xl font-semibold text-white">结果展示</h2>
      <div class="flex items-center space-x-2">
        <i :class="statusIndicatorIcon" class="text-xs"></i>
        <span class="text-sm" :class="statusIndicatorClass">{{ statusIndicatorText }}</span>
      </div>
    </div>

    <div id="status" class="mb-4 p-4 rounded-xl border" :class="statusClass">
      <p :class="statusTextClass">{{ statusMessage }}</p>
    </div>

    <ErrorDisplay
      v-if="parsedError"
      :error="parsedError"
      @dismiss="handleDismissError"
    />

    <div v-show="resultText" id="result" class="mb-4">
      <h4 class="font-medium mb-3 text-indigo-300">识别结果</h4>
      <div id="result-content" class="p-4 rounded-xl bg-white/10 border border-white/20 text-white">{{ resultText }}</div>
    </div>

    <div v-show="audioUrl" id="audio-player" class="mb-4">
      <h4 class="font-medium mb-3 text-indigo-300">音频播放</h4>
      <audio ref="audioPlayer" :src="audioUrl" controls class="w-full rounded-lg"></audio>
    </div>

    <div class="mt-6">
      <h4 class="font-medium mb-3 text-indigo-300">
        <i class="fa fa-history mr-2"></i>操作历史
      </h4>
      <div id="history" class="max-h-48 overflow-y-auto space-y-2">
        <div v-if="historyItems.length === 0" class="text-indigo-300/60 text-sm">暂无操作历史</div>
        <div
          v-for="(item, index) in historyItems"
          :key="index"
          class="p-3 rounded-lg bg-white/5 border border-white/10"
        >
          <div class="flex justify-between items-start mb-1">
            <span class="text-white font-medium">{{ item.action }}</span>
            <span class="text-indigo-400 text-xs">{{ item.timestamp }}</span>
          </div>
          <p class="text-indigo-300/70 text-xs break-words">{{ item.result }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import ErrorDisplay from './ErrorDisplay.vue'
import { parseError } from '../utils/errorHandler'

const props = defineProps({
  statusMessage: {
    type: String,
    default: '等待操作...'
  },
  statusType: {
    type: String,
    default: 'info'
  },
  resultText: {
    type: String,
    default: ''
  },
  audioUrl: {
    type: String,
    default: ''
  },
  errorMessage: {
    type: String,
    default: ''
  },
  historyItems: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['dismiss-error'])

const audioPlayer = ref(null)

const parsedError = computed(() => {
  if (!props.errorMessage) return null
  return parseError(props.errorMessage)
})

const handleDismissError = () => {
  emit('dismiss-error')
}

const statusClass = computed(() => {
  if (props.statusType === 'success') return 'bg-green-500/20 border-green-500/30 text-green-200'
  if (props.statusType === 'error') return 'bg-red-500/20 border-red-500/30 text-red-200'
  if (props.statusType === 'loading') return 'bg-blue-500/20 border-blue-500/30 text-blue-200'
  return 'bg-white/10 border-white/20 text-indigo-200'
})

const statusTextClass = computed(() => {
  if (props.statusType === 'success') return 'text-green-200'
  if (props.statusType === 'error') return 'text-red-200'
  if (props.statusType === 'loading') return 'text-blue-200'
  return 'text-indigo-200'
})

const statusIndicatorIcon = computed(() => {
  if (props.statusType === 'listening') return 'fa fa-circle text-green-400 animate-pulse'
  return 'fa fa-circle text-indigo-300'
})

const statusIndicatorClass = computed(() => {
  if (props.statusType === 'listening') return 'text-green-400'
  return 'text-indigo-300'
})

const statusIndicatorText = computed(() => {
  if (props.statusType === 'listening') return '录音中'
  return '就绪'
})

watch(() => props.audioUrl, (newUrl) => {
  if (newUrl && audioPlayer.value) {
    audioPlayer.value.load()
  }
})
</script>

<style scoped>
.result-display-panel {
  background: linear-gradient(145deg, #1e1b4b 0%, #312e81 100%);
  border-radius: 24px;
  min-height: 400px;
}
</style>
