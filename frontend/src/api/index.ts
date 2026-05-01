import axios from 'axios'
import type { TaskParams, AppSettings } from '../types'

const api = axios.create({
  baseURL: '/api/v1',
  timeout: 300000
})

// 文本生图
export async function generateImage(
  prompt: string, 
  params: TaskParams, 
  settings: AppSettings
) {
  const res = await api.post('/images/generate', { 
    prompt, 
    params,
    api_base_url: settings.baseUrl,
    api_path: settings.generationPath,
    api_keys: settings.apiKey.split('\n').map(k => k.trim()).filter(k => k),
    model: settings.model
  })
  return res.data.data
}

// 图片编辑
export async function editImage(
  prompt: string, 
  params: TaskParams, 
  settings: AppSettings,
  files: File[]
) {
  const formData = new FormData()
  formData.append('prompt', prompt)
  formData.append('params', JSON.stringify(params))
  formData.append('api_base_url', settings.baseUrl)
  formData.append('api_path', settings.editPath)
  formData.append('api_keys', JSON.stringify(settings.apiKey.split('\n').map(k => k.trim()).filter(k => k)))
  formData.append('model', settings.model)
  files.forEach((file, index) => {
    formData.append(`images`, file, `input_${index}.png`)
  })
  const res = await api.post('/images/edit', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
  return res.data.data
}

/**
 * 统一调用图片API，自动判断是文本生图还是图片编辑
 */
export async function callImageApi(options: {
  settings: AppSettings
  prompt: string
  params: TaskParams
  inputImageDataUrls: string[]
}) {
  const { settings, prompt, params, inputImageDataUrls } = options

  if (inputImageDataUrls.length > 0) {
    // 有输入图片，使用编辑接口
    const files = inputImageDataUrls.map((dataUrl, index) => {
      const arr = dataUrl.split(',')
      const mime = arr[0].match(/:(.*?);/)?.[1] ?? 'image/png'
      const bstr = atob(arr[1])
      let n = bstr.length
      const u8arr = new Uint8Array(n)
      while (n--) {
        u8arr[n] = bstr.charCodeAt(n)
      }
      return new File([u8arr], `input_${index}.png`, { type: mime })
    })
    return editImage(prompt, params, settings, files)
  } else {
    // 没有输入图片，使用生成接口
    return generateImage(prompt, params, settings)
  }
}

// 批量打包下载
export async function batchDownload(imageUrls: string[]) {
  const res = await api.post('/images/batch-download', { image_urls: imageUrls }, {
    responseType: 'blob'
  })
  // 下载文件
  const blob = new Blob([res.data], { type: 'application/zip' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `ai_images_${Date.now()}.zip`
  a.click()
  URL.revokeObjectURL(url)
  return true
}
