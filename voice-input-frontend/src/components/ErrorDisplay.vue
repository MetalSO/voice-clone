<template>
  <div v-if="error" class="error-display" :class="errorClass">
    <div class="error-header">
      <div class="error-icon-wrapper">
        <i :class="errorIcon" class="error-icon"></i>
      </div>
      <div class="error-title-section">
        <h4 class="error-title">{{ errorTitle }}</h4>
        <span class="error-badge" :class="errorBadgeClass">{{ errorCategory }}</span>
      </div>
      <button @click="onDismiss" class="error-close" aria-label="关闭">
        <i class="fa fa-times"></i>
      </button>
    </div>

    <div class="error-body">
      <div class="error-message-box">
        <span class="error-label">错误描述</span>
        <p class="error-message">{{ error.message }}</p>
      </div>

      <div v-if="error.code" class="error-code-box">
        <span class="error-label">错误代码</span>
        <code class="error-code">{{ error.code }}</code>
      </div>

      <div v-if="suggestions.length > 0" class="error-suggestions">
        <span class="error-label">
          <i class="fa fa-lightbulb-o mr-1"></i>解决方案
        </span>
        <ul class="suggestion-list">
          <li v-for="(suggestion, index) in suggestions" :key="index" class="suggestion-item">
            <i class="fa fa-check-circle suggestion-icon"></i>
            <span>{{ suggestion }}</span>
          </li>
        </ul>
      </div>
    </div>

    <div v-if="error.details" class="error-details">
      <button @click="toggleDetails" class="details-toggle">
        <i :class="showDetails ? 'fa fa-chevron-up' : 'fa fa-chevron-down'"></i>
        <span>{{ showDetails ? '收起详情' : '查看详情' }}</span>
      </button>
      <div v-show="showDetails" class="details-content">
        <pre class="details-pre">{{ error.details }}</pre>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

const props = defineProps({
  error: {
    type: Object,
    default: null
  },
  autoDismiss: {
    type: Boolean,
    default: false
  },
  dismissTime: {
    type: Number,
    default: 5000
  }
})

const emit = defineEmits(['dismiss'])

const showDetails = ref(false)

const errorClass = computed(() => {
  if (!props.error) return ''
  switch (props.error.level) {
    case 'critical': return 'error-critical'
    case 'warning': return 'error-warning'
    case 'info': return 'error-info'
    default: return 'error-critical'
  }
})

const errorIcon = computed(() => {
  if (!props.error) return 'fa fa-exclamation-circle'
  switch (props.error.level) {
    case 'critical': return 'fa fa-exclamation-triangle'
    case 'warning': return 'fa fa-exclamation-circle'
    case 'info': return 'fa fa-info-circle'
    default: return 'fa fa-exclamation-triangle'
  }
})

const errorTitle = computed(() => {
  if (!props.error) return ''
  return props.error.title || '操作失败'
})

const errorCategory = computed(() => {
  if (!props.error) return ''
  return props.error.category || '未知错误'
})

const errorBadgeClass = computed(() => {
  if (!props.error) return ''
  switch (props.error.level) {
    case 'critical': return 'badge-critical'
    case 'warning': return 'badge-warning'
    case 'info': return 'badge-info'
    default: return 'badge-critical'
  }
})

const suggestions = computed(() => {
  if (!props.error || !props.error.suggestions) return []
  return props.error.suggestions
})

const toggleDetails = () => {
  showDetails.value = !showDetails.value
}

const onDismiss = () => {
  emit('dismiss')
}

watch(() => props.error, (newError) => {
  if (newError && props.autoDismiss) {
    setTimeout(() => {
      emit('dismiss')
    }, props.dismissTime)
  }
  showDetails.value = false
})
</script>

<style scoped>
.error-display {
  border-radius: 16px;
  overflow: hidden;
  transition: all 0.3s ease;
  animation: slideIn 0.3s ease;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.error-critical {
  background: linear-gradient(145deg, rgba(239, 68, 68, 0.15), rgba(239, 68, 68, 0.05));
  border: 1px solid rgba(239, 68, 68, 0.3);
}

.error-warning {
  background: linear-gradient(145deg, rgba(245, 158, 11, 0.15), rgba(245, 158, 11, 0.05));
  border: 1px solid rgba(245, 158, 11, 0.3);
}

.error-info {
  background: linear-gradient(145deg, rgba(59, 130, 246, 0.15), rgba(59, 130, 246, 0.05));
  border: 1px solid rgba(59, 130, 246, 0.3);
}

.error-header {
  display: flex;
  align-items: center;
  padding: 16px 20px;
  gap: 12px;
}

.error-icon-wrapper {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.error-critical .error-icon-wrapper {
  background: rgba(239, 68, 68, 0.2);
}

.error-warning .error-icon-wrapper {
  background: rgba(245, 158, 11, 0.2);
}

.error-info .error-icon-wrapper {
  background: rgba(59, 130, 246, 0.2);
}

.error-icon {
  font-size: 18px;
}

.error-critical .error-icon {
  color: #f87171;
}

.error-warning .error-icon {
  color: #fbbf24;
}

.error-info .error-icon {
  color: #60a5fa;
}

.error-title-section {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 10px;
  min-width: 0;
}

.error-title {
  font-size: 15px;
  font-weight: 600;
  color: #f1f5f9;
  margin: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.error-badge {
  font-size: 10px;
  font-weight: 600;
  padding: 3px 8px;
  border-radius: 20px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  flex-shrink: 0;
}

.badge-critical {
  background: rgba(239, 68, 68, 0.25);
  color: #fca5a5;
}

.badge-warning {
  background: rgba(245, 158, 11, 0.25);
  color: #fcd34d;
}

.badge-info {
  background: rgba(59, 130, 246, 0.25);
  color: #93c5fd;
}

.error-close {
  width: 28px;
  height: 28px;
  border-radius: 8px;
  border: none;
  background: rgba(255, 255, 255, 0.1);
  color: #94a3b8;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  flex-shrink: 0;
}

.error-close:hover {
  background: rgba(255, 255, 255, 0.15);
  color: #f1f5f9;
}

.error-body {
  padding: 0 20px 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.error-label {
  display: block;
  font-size: 11px;
  font-weight: 600;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 6px;
}

.error-message-box {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 10px;
  padding: 12px 14px;
}

.error-message {
  font-size: 14px;
  line-height: 1.6;
  color: #e2e8f0;
  margin: 0;
  word-break: break-word;
}

.error-code-box {
  display: flex;
  align-items: center;
  gap: 12px;
}

.error-code-box .error-label {
  margin-bottom: 0;
}

.error-code {
  font-family: 'SF Mono', 'Consolas', monospace;
  font-size: 12px;
  background: rgba(0, 0, 0, 0.3);
  color: #94a3b8;
  padding: 4px 10px;
  border-radius: 6px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.error-suggestions {
  background: rgba(16, 185, 129, 0.1);
  border: 1px solid rgba(16, 185, 129, 0.2);
  border-radius: 10px;
  padding: 12px 14px;
}

.error-suggestions .error-label {
  color: #6ee7b7;
}

.suggestion-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.suggestion-item {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  font-size: 13px;
  color: #d1fae5;
  line-height: 1.5;
}

.suggestion-icon {
  color: #34d399;
  margin-top: 2px;
  flex-shrink: 0;
}

.error-details {
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  padding: 12px 20px;
}

.details-toggle {
  display: flex;
  align-items: center;
  gap: 6px;
  background: none;
  border: none;
  color: #64748b;
  font-size: 12px;
  cursor: pointer;
  padding: 4px 0;
  transition: color 0.2s ease;
}

.details-toggle:hover {
  color: #94a3b8;
}

.details-content {
  margin-top: 10px;
}

.details-pre {
  font-family: 'SF Mono', 'Consolas', monospace;
  font-size: 11px;
  line-height: 1.6;
  color: #94a3b8;
  background: rgba(0, 0, 0, 0.3);
  padding: 12px;
  border-radius: 8px;
  overflow-x: auto;
  margin: 0;
  white-space: pre-wrap;
  word-break: break-all;
}

@media (max-width: 640px) {
  .error-header {
    padding: 12px 16px;
  }

  .error-body {
    padding: 0 16px 12px;
  }

  .error-details {
    padding: 12px 16px;
  }

  .error-title-section {
    flex-direction: column;
    align-items: flex-start;
    gap: 4px;
  }

  .error-title {
    font-size: 14px;
  }

  .error-message {
    font-size: 13px;
  }
}
</style>
