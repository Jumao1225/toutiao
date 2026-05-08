/**
 * API配置文件
 * 包含API基础URL和AI问答功能所需的API参数
 */

// API基础URL配置
export const apiConfig = {
  // 后端API基础URL
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000',
}

export const aiChatConfig = {
  // AI API地址
  apiEndpoint: import.meta.env.VITE_AI_API_ENDPOINT || 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions',

  // API Key（请放到 .env，不要写死到代码）
  apiKey: import.meta.env.VITE_AI_API_KEY || '',

  // 使用的模型
  model: import.meta.env.VITE_AI_MODEL || 'qwen3-max-preview'
}
