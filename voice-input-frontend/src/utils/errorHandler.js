export const ErrorLevel = {
  CRITICAL: 'critical',
  WARNING: 'warning',
  INFO: 'info'
}

export const ErrorCategory = {
  NETWORK: '网络错误',
  AUDIO: '音频错误',
  PERMISSION: '权限错误',
  SERVER: '服务器错误',
  VALIDATION: '验证错误',
  UNKNOWN: '未知错误'
}

export const ErrorMessages = {
  NETWORK_ERROR: {
    title: '网络连接失败',
    level: ErrorLevel.CRITICAL,
    category: ErrorCategory.NETWORK,
    suggestions: [
      '请检查您的网络连接是否正常',
      '确认后端服务是否已启动',
      '尝试刷新页面后重新操作'
    ]
  },
  SERVER_ERROR: {
    title: '服务器错误',
    level: ErrorLevel.CRITICAL,
    category: ErrorCategory.SERVER,
    suggestions: [
      '后端服务可能未启动，请先启动后端服务',
      '服务器处理超时，请稍后重试',
      '如果问题持续存在，请联系技术支持'
    ]
  },
  PERMISSION_DENIED: {
    title: '权限被拒绝',
    level: ErrorLevel.WARNING,
    category: ErrorCategory.PERMISSION,
    suggestions: [
      '请在浏览器设置中允许麦克风权限',
      '刷新页面后重新尝试录音功能'
    ]
  },
  AUDIO_NOT_SUPPORTED: {
    title: '浏览器不支持音频',
    level: ErrorLevel.WARNING,
    category: ErrorCategory.AUDIO,
    suggestions: [
      '请使用 Chrome、Firefox、Edge 或 Safari 等现代浏览器',
      '确保浏览器版本为最新版本'
    ]
  },
  SYNTHESIS_FAILED: {
    title: '语音合成失败',
    level: ErrorLevel.CRITICAL,
    category: ErrorCategory.AUDIO,
    suggestions: [
      '请检查选择的语音模型是否可用',
      '尝试更换为其他语音模型',
      '确认文本内容不为空'
    ]
  },
  MODEL_LOAD_FAILED: {
    title: '模型加载失败',
    level: ErrorLevel.WARNING,
    category: ErrorCategory.SERVER,
    suggestions: [
      '后端服务可能未启动或模型未正确加载',
      '请重启后端服务',
      '尝试使用其他可用的语音模型'
    ]
  },
  INVALID_INPUT: {
    title: '输入无效',
    level: ErrorLevel.INFO,
    category: ErrorCategory.VALIDATION,
    suggestions: [
      '请输入要转换的文本内容',
      '确保文本长度在有效范围内'
    ]
  },
  RECOGNITION_FAILED: {
    title: '语音识别失败',
    level: ErrorLevel.WARNING,
    category: ErrorCategory.AUDIO,
    suggestions: [
      '请确保在安静的环境中进行语音输入',
      '说话声音要清晰，语速适中',
      '检查麦克风是否正常工作'
    ]
  },
  TIMEOUT: {
    title: '请求超时',
    level: ErrorLevel.WARNING,
    category: ErrorCategory.NETWORK,
    suggestions: [
      '网络连接不稳定，请检查网络',
      '服务器响应缓慢，请稍后重试'
    ]
  }
}

export function parseError(error) {
  if (!error) return null

  if (typeof error === 'string') {
    return parseErrorMessage(error)
  }

  if (error instanceof Error) {
    return parseErrorObject(error)
  }

  return {
    title: '操作失败',
    message: error.message || String(error),
    level: ErrorLevel.CRITICAL,
    category: ErrorCategory.UNKNOWN,
    suggestions: ['请稍后重试，如果问题持续存在请联系我们']
  }
}

function parseErrorMessage(message) {
  const lowerMessage = message.toLowerCase()

  if (lowerMessage.includes('network') || lowerMessage.includes('fetch') || lowerMessage.includes('断开连接')) {
    return { ...ErrorMessages.NETWORK_ERROR, message }
  }

  if (lowerMessage.includes('permission') || lowerMessage.includes('denied') || lowerMessage.includes('拒绝')) {
    return { ...ErrorMessages.PERMISSION_DENIED, message }
  }

  if (lowerMessage.includes('timeout') || lowerMessage.includes('超时')) {
    return { ...ErrorMessages.TIMEOUT, message }
  }

  if (lowerMessage.includes('synthesize') || lowerMessage.includes('合成')) {
    return { ...ErrorMessages.SYNTHESIS_FAILED, message }
  }

  if (lowerMessage.includes('model') || lowerMessage.includes('模型')) {
    return { ...ErrorMessages.MODEL_LOAD_FAILED, message }
  }

  if (lowerMessage.includes('recognition') || lowerMessage.includes('识别')) {
    return { ...ErrorMessages.RECOGNITION_FAILED, message }
  }

  if (lowerMessage.includes('audio') || lowerMessage.includes('音频')) {
    return { ...ErrorMessages.AUDIO_NOT_SUPPORTED, message }
  }

  return {
    title: '操作失败',
    message,
    level: ErrorLevel.CRITICAL,
    category: ErrorCategory.UNKNOWN,
    suggestions: ['请稍后重试，如果问题持续存在请联系我们']
  }
}

function parseErrorObject(errorObj) {
  const code = errorObj.code || errorObj.status || null
  let parsed = parseErrorMessage(errorObj.message || errorObj.msg || '')

  if (code) {
    parsed.code = code
  }

  if (errorObj.details) {
    parsed.details = typeof errorObj.details === 'object'
      ? JSON.stringify(errorObj.details, null, 2)
      : errorObj.details
  }

  return parsed
}

export function formatErrorForDisplay(error) {
  const parsed = parseError(error)

  return {
    ...parsed,
    message: parsed.message || '发生了一个未知错误'
  }
}
