<template>
  <div class="p-6 bg-surface-50 border-b border-surface-200">
    <!-- Prompt Input -->
    <div class="mb-4">
      <textarea
        v-model="prompt"
        rows="3"
        placeholder="描述你想要生成的图片..."
        class="w-full px-4 py-3 bg-white border border-surface-200 rounded-xl text-content-primary placeholder-content-muted focus:outline-none focus:ring-2 focus:ring-primary-500/20 focus:border-primary-500 transition-all resize-none"
        @keydown.ctrl.enter="handleSubmit"
      />
    </div>

    <!-- Input Images -->
    <div v-if="inputImages.length > 0" class="flex gap-3 mb-4 overflow-x-auto pb-2">
      <div
        v-for="(img, index) in inputImages"
        :key="img.id"
        class="relative flex-shrink-0 w-24 h-24 rounded-xl overflow-hidden border border-surface-200 group"
      >
        <img :src="img.dataUrl" class="w-full h-full object-cover" />
        <button
          @click="removeInputImage(index)"
          class="absolute top-1 right-1 w-6 h-6 bg-black/50 hover:bg-red-500 text-white rounded-full flex items-center justify-center opacity-0 group-hover:opacity-100 transition-all"
        >
          <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
    </div>

    <!-- Controls -->
    <div class="flex flex-wrap items-center justify-between gap-4">
      <!-- Left: Actions -->
      <div class="flex items-center gap-3">
        <!-- File Upload -->
        <label class="px-4 py-2 bg-white border border-surface-200 hover:border-primary-400 hover:text-primary-600 text-content-secondary rounded-lg cursor-pointer transition-all flex items-center gap-2 text-sm font-medium">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
          添加参考图
          <input 
            type="file" 
            accept="image/*" 
            multiple 
            class="hidden" 
            @change="handleFileUpload"
          />
        </label>

        <button 
          @click="showSettings = true"
          class="px-4 py-2 bg-white border border-surface-200 hover:border-primary-400 hover:text-primary-600 text-content-secondary rounded-lg transition-all flex items-center gap-2 text-sm font-medium"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
          </svg>
          设置
        </button>

        <button 
          @click="handleExport"
          class="px-4 py-2 bg-white border border-surface-200 hover:border-primary-400 hover:text-primary-600 text-content-secondary rounded-lg transition-all flex items-center gap-2 text-sm font-medium"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
          </svg>
          导出
        </button>

        <label class="px-4 py-2 bg-white border border-surface-200 hover:border-primary-400 hover:text-primary-600 text-content-secondary rounded-lg cursor-pointer transition-all flex items-center gap-2 text-sm font-medium">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
          </svg>
          导入
          <input 
            type="file" 
            accept=".zip" 
            class="hidden" 
            @change="handleImport"
          />
        </label>
      </div>

      <!-- Right: Parameters & Submit -->
      <div class="flex items-center gap-3">
        <!-- Size -->
        <input
          v-model="size"
          type="text"
          placeholder="尺寸 (如 1024x1024)"
          class="px-3 py-2 bg-white border border-surface-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary-500/20 focus:border-primary-500 transition-all w-32"
          @input="updateParams('size', $event.target.value)"
        />

        <!-- Quality -->
        <select
          v-model="quality"
          class="px-3 py-2 bg-white border border-surface-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary-500/20 focus:border-primary-500 transition-all cursor-pointer"
          @change="updateParams('quality', $event.target.value)"
        >
          <option value="auto">自动质量</option>
          <option value="low">低</option>
          <option value="medium">中</option>
          <option value="high">高</option>
        </select>

        <!-- Count -->
        <select
          v-model="n"
          class="px-3 py-2 bg-white border border-surface-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary-500/20 focus:border-primary-500 transition-all cursor-pointer"
          @change="updateParams('n', Number($event.target.value))"
        >
          <option :value="1">1 张</option>
          <option :value="2">2 张</option>
          <option :value="3">3 张</option>
          <option :value="4">4 张</option>
        </select>

        <!-- Submit -->
        <button
          @click="handleSubmit"
          :disabled="submitting"
          class="px-6 py-2.5 bg-primary-600 hover:bg-primary-700 disabled:bg-surface-300 disabled:cursor-not-allowed text-white font-semibold rounded-lg transition-all flex items-center gap-2 shadow-soft hover:shadow-glow"
        >
          <svg v-if="!submitting" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
          <svg v-else class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
          </svg>
          {{ submitting ? '生成中...' : '生成图片' }}
        </button>
      </div>
    </div>

    <!-- Settings Modal -->
    <SettingsModal v-model="showSettings" />
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useAppStore } from '@/stores/app'
import SettingsModal from './SettingsModal.vue'

const appStore = useAppStore()
const submitting = ref(false)
const showSettings = ref(false)

const prompt = computed({
  get: () => appStore.prompt,
  set: (val) => appStore.setPrompt(val)
})

const inputImages = computed(() => appStore.inputImages)

const size = computed({
  get: () => appStore.params.size,
  set: (val) => appStore.setParams({ size: val })
})

const quality = computed({
  get: () => appStore.params.quality,
  set: (val) => appStore.setParams({ quality: val })
})

const n = computed({
  get: () => appStore.params.n,
  set: (val) => appStore.setParams({ n: val })
})

const updateParams = (key: string, value: any) => {
  appStore.setParams({ [key]: value })
}

const removeInputImage = (index: number) => {
  appStore.removeInputImage(index)
}

const handleFileUpload = (event: Event) => {
  const target = event.target as HTMLInputElement
  const files = target.files
  if (files) {
    Array.from(files).forEach(file => {
      if (file.type.startsWith('image/')) {
        appStore.addImageFromFile(file)
      }
    })
  }
  target.value = ''
}

const handleSubmit = async () => {
  if (submitting.value) return
  submitting.value = true
  try {
    await appStore.submitTask()
  } finally {
    submitting.value = false
  }
}

const handleExport = () => {
  appStore.exportData()
}

const handleImport = (event: Event) => {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  if (file) {
    appStore.importData(file)
  }
  target.value = ''
}
</script>
