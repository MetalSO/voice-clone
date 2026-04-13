import axios from 'axios'

const PYTHON_API_BASE = 'http://localhost:8080'

const speechApi = axios.create({
  baseURL: PYTHON_API_BASE,
  timeout: 60000,
  headers: {
    'Content-Type': 'application/json'
  }
})

speechApi.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    const message = error.response?.data?.detail || error.message || '请求失败'
    return Promise.reject(new Error(message))
  }
)

export const speechService = {
  async synthesize(text, model = 'gtts', language = 'zh-CN', gender = 'female') {
    const response = await speechApi.post('/api/speech/synthesize', {
      text,
      model,
      language,
      gender
    })
    return response
  },

  async getAudioFile(audioPath) {
    const response = await axios.get(`${PYTHON_API_BASE}/${audioPath}`, {
      responseType: 'blob'
    })
    return response.data
  },

  async getModels() {
    const response = await speechApi.get('/api/speech/models')
    return response
  },

  async checkHealth() {
    try {
      await speechApi.get('/health')
      return true
    } catch {
      return false
    }
  }
}

export const speechRecognition = {
  isSupported() {
    return !!(window.SpeechRecognition || window.webkitSpeechRecognition)
  },

  createRecognizer() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition

    if (!SpeechRecognition) {
      return null
    }

    const recognizer = new SpeechRecognition()
    recognizer.continuous = true
    recognizer.interimResults = true
    recognizer.lang = 'zh-CN'

    return recognizer
  }
}

export default {
  speechService,
  speechRecognition
}
