<template>
  <div v-if="modelValue" class="fixed inset-0 z-50 flex items-center justify-center p-4">
    <!-- Backdrop -->
    <div class="absolute inset-0 bg-black/50 backdrop-blur-sm" @click="close"></div>
    
    <!-- Modal -->
    <div class="relative bg-white rounded-2xl shadow-xl max-w-lg w-full max-h-[90vh] overflow-y-auto animate-modal-in">
      <!-- Header -->
      <div class="sticky top-0 bg-white border-b border-surface-200 px-6 py-4 flex items-center justify-between">
        <h3 class="font-heading text-xl font-semibold text-content-primary">设置</h3>
        <button @click="close" class="p-2 hover:bg-surface-100 rounded-lg transition-colors">
          <svg class="w-5 h-5 text-content-secondary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <!-- Form -->
      <div class="p-6 space-y-5">
        <!-- API Base URL -->
        <div>
          <label class="block text-sm font-medium text-content-primary mb-2">API 地址</label>
          <input
            v-model="form.baseUrl"
            type="text"
            placeholder="https://api.openai.com"
            class="w-full px-4 py-2.5 bg-white border border-surface-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary-500/20 focus:border-primary-500 transition-all"
          />
        </div>

        <!-- API Key -->
        <div>
          <label class="block text-sm font-medium text-content-primary mb-2">API 密钥</label>
          <div class="relative">
            <input
              v-model="form.apiKey"
              :type="showApiKey ? 'text' : 'password'"
              placeholder="sk-xxxx"
              class="w-full px-4 py-2.5 bg-white border border-surface-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary-500/20 focus:border-primary-500 transition-all pr-10"
            />
            <button
              @click="showApiKey = !showApiKey"
              class="absolute right-3 top-1/2 -translate-y-1/2 text-content-muted hover:text-content-secondary"
            >
              <svg v-if="showApiKey" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
              </svg>
              <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
              </svg>
            </button>
          </div>
          <p class="mt-1 text-xs text-content-muted">你的 API 密钥仅存储在本地浏览器中</p>
        </div>

        <!-- Model -->
        <div>
          <label class="block text-sm font-medium text-content-primary mb-2">模型名称</label>
          <input
            v-model="form.model"
            type="text"
            placeholder="gpt-image-2"
            class="w-full px-4 py-2.5 bg-white border border-surface-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary-500/20 focus:border-primary-500 transition-all"
          />
        </div>

        <!-- Generation Path -->
        <div>
          <label class="block text-sm font-medium text-content-primary mb-2">文本生图接口</label>
          <input
            v-model="form.generationPath"
            type="text"
            placeholder="v1/images/generations"
            class="w-full px-4 py-2.5 bg-white border border-surface-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary-500/20 focus:border-primary-500 transition-all"
          />
          <p class="mt-1 text-xs text-content-muted">支持输入自定义完整 URL</p>
        </div>

        <!-- Edit Path -->
        <div>
          <label class="block text-sm font-medium text-content-primary mb-2">图片编辑接口</label>
          <input
            v-model="form.editPath"
            type="text"
            placeholder="v1/images/edits"
            class="w-full px-4 py-2.5 bg-white border border-surface-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary-500/20 focus:border-primary-500 transition-all"
          />
          <p class="mt-1 text-xs text-content-muted">支持输入自定义完整 URL</p>
        </div>

        <!-- Timeout -->
        <div>
          <label class="block text-sm font-medium text-content-primary mb-2">请求超时（秒）</label>
          <input
            v-model.number="form.timeout"
            type="number"
            min="10"
            max="600"
            class="w-full px-4 py-2.5 bg-white border border-surface-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary-500/20 focus:border-primary-500 transition-all"
          />
        </div>

        <!-- Auto Compress -->
        <div class="flex items-center justify-between">
          <div>
            <label class="block text-sm font-medium text-content-primary">生成后自动压缩图片</label>
            <p class="text-xs text-content-muted mt-1">兼顾画质和下载速度，默认关闭</p>
          </div>
          <button
            @click="form.enableCompress = !form.enableCompress"
            class="relative inline-flex h-6 w-11 items-center rounded-full transition-colors"
            :class="form.enableCompress ? 'bg-primary-600' : 'bg-surface-300'"
          >
            <span
              class="inline-block h-4 w-4 rounded-full bg-white transition-transform"
              :class="form.enableCompress ? 'translate-x-6' : 'translate-x-1'"
            />
          </button>
        </div>
      </div>

      <!-- Footer -->
      <div class="sticky bottom-0 bg-surface-50 border-t border-surface-200 px-6 py-4 flex items-center justify-between">
        <button
          @click="showClearConfirm = true"
          class="px-4 py-2 text-sm font-medium text-red-600 hover:bg-red-50 rounded-lg transition-colors"
        >
          清空所有数据
        </button>
        <div class="flex items-center gap-3">
          <button
            @click="close"
            class="px-5 py-2.5 text-sm font-medium text-content-secondary hover:bg-surface-100 rounded-lg transition-colors"
          >
            取消
          </button>
          <button
            @click="save"
            class="px-5 py-2.5 text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 rounded-lg transition-colors"
          >
            保存
          </button>
        </div>
      </div>
    </div>

    <!-- Clear Data Confirmation -->
    <div v-if="showClearConfirm" class="fixed inset-0 z-[60] flex items-center justify-center p-4">
      <div class="absolute inset-0 bg-black/60 backdrop-blur-sm" @click="showClearConfirm = false"></div>
      <div class="relative bg-white rounded-2xl shadow-xl max-w-sm w-full p-6 animate-modal-in">
        <div class="text-center mb-6">
          <div class="w-12 h-12 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg class="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
          </div>
          <h3 class="font-heading text-lg font-semibold text-content-primary mb-2">确认清空</h3>
          <p class="text-sm text-content-secondary">此操作将删除所有任务记录、图片和配置，且不可恢复！</p>
        </div>
        <div class="flex gap-3">
          <button 
            @click="showClearConfirm = false"
            class="flex-1 px-4 py-2.5 bg-surface-100 hover:bg-surface-200 text-content-primary font-medium rounded-lg transition-colors"
          >
            取消
          </button>
          <button 
            @click="clearData"
            class="flex-1 px-4 py-2.5 bg-red-500 hover:bg-red-600 text-white font-medium rounded-lg transition-colors"
          >
            确认清空
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { useAppStore } from '@/stores/app'

const props = defineProps<{
  modelValue: boolean
}>()

const emit = defineEmits<{
  'update:modelValue': [value: boolean]
}>()

const appStore = useAppStore()
const showApiKey = ref(false)
const showClearConfirm = ref(false)

const form = ref({ ...appStore.settings })

watch(() => props.modelValue, (val) => {
  if (val) {
    form.value = { ...appStore.settings }
  }
})

const close = () => {
  emit('update:modelValue', false)
  showApiKey.value = false
}

const save = () => {
  appStore.setSettings(form.value)
  appStore.showToast('设置已保存', 'success')
  close()
}

const clearData = async () => {
  await appStore.clearAllData()
  form.value = { ...appStore.settings }
  showClearConfirm.value = false
  close()
}
</script>

<style scoped>
.animate-modal-in {
  animation: modal-in 0.25s cubic-bezier(0.16, 1, 0.3, 1) both;
}

@keyframes modal-in {
  from { opacity: 0; transform: scale(0.95) translateY(10px); }
  to { opacity: 1; transform: scale(1) translateY(0); }
}
</style>
