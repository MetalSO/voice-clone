<template>
  <div class="recognition-result">
    <el-card class="result-card">
      <template #header>
        <div class="card-header">
          <span>识别结果</span>
          <el-button 
            v-if="text" 
            type="primary" 
            link 
            @click="copyText"
            :icon="copied ? 'Check' : 'DocumentCopy'"
          >
            {{ copied ? '已复制' : '复制' }}
          </el-button>
        </div>
      </template>
      
      <div class="result-content">
        <el-empty v-if="!text && !loading" description="暂无识别结果"></el-empty>
        
        <div v-else-if="loading" class="loading-container">
          <el-icon class="is-loading"><Loading /></el-icon>
          <span>正在识别...</span>
        </div>
        
        <div v-else class="text-result">
          <p class="recognized-text">{{ text }}</p>
          
          <div class="result-actions">
            <el-button type="success" @click="useText">使用此文本</el-button>
            <el-button @click="clearText">清除</el-button>
          </div>
        </div>
      </div>
      
      <div v-if="error" class="error-container">
        <el-alert type="error" :closable="false">{{ error }}</el-alert>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'

const props = defineProps({
  text: {
    type: String,
    default: ''
  },
  loading: {
    type: Boolean,
    default: false
  },
  error: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['use-text', 'clear'])
const copied = ref(false)

const copyText = async () => {
  try {
    await navigator.clipboard.writeText(props.text)
    copied.value = true
    ElMessage.success('已复制到剪贴板')
    setTimeout(() => {
      copied.value = false
    }, 2000)
  } catch (error) {
    ElMessage.error('复制失败')
  }
}

const useText = () => {
  emit('use-text', props.text)
}

const clearText = () => {
  emit('clear')
}
</script>

<style scoped>
.recognition-result {
  margin-top: 20px;
}

.result-card {
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
  font-size: 16px;
}

.result-content {
  min-height: 150px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 15px;
  color: #666;
  font-size: 16px;
}

.text-result {
  width: 100%;
}

.recognized-text {
  font-size: 18px;
  line-height: 1.8;
  color: #333;
  padding: 20px;
  background: #f5f7fa;
  border-radius: 10px;
  margin-bottom: 20px;
  word-break: break-all;
}

.result-actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
}

.error-container {
  margin-top: 15px;
}
</style>
