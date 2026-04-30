<template>
  <div class="px-6 py-4 bg-white border-b border-surface-200">
    <div class="flex items-center justify-between">
      <div class="flex items-center gap-3">
        <div class="w-8 h-8 bg-gradient-to-br from-primary-500 to-primary-600 rounded-lg flex items-center justify-center">
          <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
        </div>
        <div>
          <h1 class="font-heading font-bold text-lg text-content-primary">AI Canvas</h1>
          <p class="text-xs text-content-muted">GPT Image API 本地版</p>
        </div>
      </div>

      <button
        @click="showHelp = true"
        class="flex items-center gap-2 px-3 py-1.5 text-sm text-content-secondary hover:text-primary-600 hover:bg-primary-50 rounded-lg transition-all"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        使用帮助
      </button>
    </div>

    <!-- Help Modal -->
    <div v-if="showHelp" class="fixed inset-0 z-50 flex items-center justify-center p-4">
      <div class="absolute inset-0 bg-black/50 backdrop-blur-sm" @click="showHelp = false"></div>
      <div class="relative bg-white rounded-2xl shadow-xl max-w-lg w-full p-6 animate-modal-in">
        <div class="flex items-center justify-between mb-6">
          <h3 class="font-heading text-xl font-semibold text-content-primary">使用帮助</h3>
          <button @click="showHelp = false" class="p-2 hover:bg-surface-100 rounded-lg transition-colors">
            <svg class="w-5 h-5 text-content-secondary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        <div class="space-y-4">
          <div class="p-4 bg-surface-50 rounded-xl">
            <div class="flex items-center gap-2 mb-2">
              <span class="w-6 h-6 bg-primary-100 text-primary-600 rounded-full flex items-center justify-center text-sm font-semibold">1</span>
              <h4 class="font-semibold text-content-primary">配置 API</h4>
            </div>
            <p class="text-sm text-content-secondary pl-8">点击「设置」按钮，填入你的 API 地址、密钥和模型名称即可使用。</p>
          </div>

          <div class="p-4 bg-surface-50 rounded-xl">
            <div class="flex items-center gap-2 mb-2">
              <span class="w-6 h-6 bg-primary-100 text-primary-600 rounded-full flex items-center justify-center text-sm font-semibold">2</span>
              <h4 class="font-semibold text-content-primary">生成图片</h4>
            </div>
            <p class="text-sm text-content-secondary pl-8">输入提示词，选择尺寸、质量等参数，点击「生成图片」即可。也可以上传参考图进行图片编辑。</p>
          </div>

          <div class="p-4 bg-surface-50 rounded-xl">
            <div class="flex items-center gap-2 mb-2">
              <span class="w-6 h-6 bg-primary-100 text-primary-600 rounded-full flex items-center justify-center text-sm font-semibold">3</span>
              <h4 class="font-semibold text-content-primary">本地存储</h4>
            </div>
            <p class="text-sm text-content-secondary pl-8">所有任务记录和图片都存储在你的浏览器本地，不会上传到任何服务器，非常安全。</p>
          </div>

          <div class="p-4 bg-surface-50 rounded-xl">
            <div class="flex items-center gap-2 mb-2">
              <span class="w-6 h-6 bg-primary-100 text-primary-600 rounded-full flex items-center justify-center text-sm font-semibold">4</span>
              <h4 class="font-semibold text-content-primary">数据导出导入</h4>
            </div>
            <p class="text-sm text-content-secondary pl-8">可以导出所有数据为ZIP文件备份，也可以导入之前的备份数据。</p>
          </div>
        </div>

        <div class="mt-6 flex justify-end">
          <button 
            @click="showHelp = false"
            class="px-6 py-2.5 bg-primary-600 hover:bg-primary-700 text-white font-medium rounded-lg transition-colors"
          >
            知道了
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const showHelp = ref(false)
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
