import axios from 'axios'

const PYTHON_API_BASE = 'http://localhost:8080'

const voiceCloneApi = axios.create({
  baseURL: PYTHON_API_BASE,
  timeout: 120000,
  headers: {
    'Content-Type': 'multipart/form-data'
  }
})

const voiceCloneService = {
  async cloneVoice(formData) {
    try {
      const response = await voiceCloneApi.post('/api/voice-clone/synthesize', formData)
      return response.data
    } catch (error) {
      console.error('Voice clone error:', error)
      if (error.response?.data) {
        throw new Error(error.response.data.detail || '语音克隆失败')
      }
      throw new Error(error.message || '网络错误，请检查后端服务是否启动')
    }
  },

  async getCloneStatus() {
    try {
      const response = await voiceCloneApi.get('/api/voice-clone/status')
      return response.data
    } catch (error) {
      console.error('Get clone status error:', error)
      return { available: false, model: null, message: error.message }
    }
  },

  async uploadReferenceAudio(audioBlob) {
    const formData = new FormData()
    formData.append('audio', audioBlob, 'reference_audio.webm')
    
    try {
      const response = await voiceCloneApi.post('/api/voice-clone/upload', formData)
      return response.data
    } catch (error) {
      console.error('Upload audio error:', error)
      throw new Error('音频上传失败: ' + (error.message || '未知错误'))
    }
  },

  getAudioUrl(audioPath) {
    return `${PYTHON_API_BASE}/${audioPath}`
  }
}

export { voiceCloneService }
