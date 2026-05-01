<template>
  <div class="bg-white rounded-2xl border border-surface-200 shadow-soft overflow-hidden hover:shadow-lg transition-shadow">
    <!-- Header -->
    <div class="px-4 py-3 bg-surface-50 border-b border-surface-200 flex items-center justify-between">
      <div class="flex items-center gap-3">
        <!-- Status Badge -->
        <span 
          class="px-2.5 py-1 rounded-full text-xs font-semibold"
          :class="{
            'bg-green-100 text-green-700': task.status === 'done',
            'bg-yellow-100 text-yellow-700': task.status === 'running',
            'bg-red-100 text-red-700': task.status === 'error'
          }"
        >
          {{ statusText }}
        </span>
        <!-- Time -->
        <span v-if="task.elapsed" class="text-xs text-content-muted">
          {{ Math.round(task.elapsed / 1000) }}s
        </span>
      </div>

      <!-- Actions -->
      <div class="flex items-center gap-1">
        <button 
          @click="handleReuse"
          class="p-1.5 text-content-muted hover:text-primary-600 hover:bg-primary-50 rounded-lg transition-colors"
          title="复用配置"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
          </svg>
        </button>
        <button 
          @click="handleEdit"
          class="p-1.5 text-content-muted hover:text-primary-600 hover:bg-primary-50 rounded-lg transition-colors"
          title="编辑图片"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
          </svg>
        </button>
        <button 
          @click="handleDelete"
          class="p-1.5 text-content-muted hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors"
          title="删除任务"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
          </svg>
        </button>
      </div>
    </div>

    <!-- Prompt -->
    <div class="px-4 py-3 border-b border-surface-200">
      <p class="text-sm text-content-primary line-clamp-2 leading-relaxed">{{ task.prompt || '无提示词' }}</p>
    </div>

    <!-- Images Grid -->
    <div class="grid grid-cols-2 gap-1 p-1">
      <!-- Output Images -->
      <div
        v-for="imgId in task.outputImages"
        :key="imgId"
        class="aspect-square relative group cursor-pointer overflow-hidden rounded-lg bg-surface-100"
        @click="openLightbox(imgId)"
      >
        <img
          :src="getImageUrl(imgId)"
          class="w-full h-full object-cover transition-transform duration-300 group-hover:scale-105"
          loading="lazy"
          alt="Generated image"
        />
        <div class="absolute inset-0 bg-black/0 group-hover:bg-black/20 transition-colors flex flex-col items-center justify-center gap-2">
          <!-- 预览按钮 -->
          <svg class="w-6 h-6 text-white opacity-0 group-hover:opacity-100 transition-opacity" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 0 0114 0zM10 7v3m0 0v3m0-3h3m-3 0H7" />
          </svg>
          <!-- 下载按钮组 -->
          <div class="flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
            <button 
              @click.stop="downloadImage(imgId, 'original')"
              class="p-1.5 bg-white/90 hover:bg-white rounded-lg transition-colors"
              title="下载原画"
            >
              <svg class="w-4 h-4 text-content-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
              </svg>
            </button>
            <button 
              @click.stop="downloadImage(imgId, 'compressed')"
              class="p-1.5 bg-white/90 hover:bg-white rounded-lg transition-colors"
              title="下载压缩图"
            >
              <svg class="w-4 h-4 text-content-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 14l-7 7m0 0l-7-7m7 7V3" />
              </svg>
            </button>
          </div>
        </div>
      </div>

      <!-- Loading State -->
      <div
        v-if="task.status === 'running'"
        class="aspect-square flex items-center justify-center bg-surface-50"
      >
        <div class="flex flex-col items-center gap-2">
          <svg class="w-8 h-8 text-primary-500 animate-spin" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
          </svg>
          <span class="text-xs text-content-muted">生成中...</span>
        </div>
      </div>

      <!-- Error State -->
      <div
        v-if="task.status === 'error'"
        class="aspect-square flex flex-col items-center justify-center bg-red-50 p-4 text-center"
      >
        <svg class="w-8 h-8 text-red-500 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <p class="text-xs text-red-600 line-clamp-3">{{ task.error }}</p>
      </div>
    </div>

    <!-- Params -->
    <div class="px-4 py-2 bg-surface-50 border-t border-surface-200 text-xs text-content-muted flex flex-wrap gap-x-4 gap-y-1">
      <span class="flex items-center gap-1">
        <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
        </svg>
        {{ task.params.size }}
      </span>
      <span class="flex items-center gap-1">
        <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z" />
        </svg>
        {{ qualityText }}
      </span>
      <span class="flex items-center gap-1">
        <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4m0 5c0 2.21-3.582 4-8 4s-8-1.79-8-4" />
        </svg>
        {{ task.params.output_format.toUpperCase() }}
      </span>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteConfirm" class="fixed inset-0 z-50 flex items-center justify-center p-4">
      <div class="absolute inset-0 bg-black/50 backdrop-blur-sm" @click="showDeleteConfirm = false"></div>
      <div class="relative bg-white rounded-2xl shadow-xl max-w-sm w-full p-6 animate-modal-in">
        <div class="text-center mb-6">
          <div class="w-12 h-12 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg class="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
          </div>
          <h3 class="font-heading text-lg font-semibold text-content-primary mb-2">确认删除</h3>
          <p class="text-sm text-content-secondary">此操作不可恢复，确定要删除这条任务记录吗？</p>
        </div>
        <div class="flex gap-3">
          <button 
            @click="showDeleteConfirm = false"
            class="flex-1 px-4 py-2.5 bg-surface-100 hover:bg-surface-200 text-content-primary font-medium rounded-lg transition-colors"
          >
            取消
          </button>
          <button 
            @click="confirmDelete"
            class="flex-1 px-4 py-2.5 bg-red-500 hover:bg-red-600 text-white font-medium rounded-lg transition-colors"
          >
            确认删除
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useAppStore } from '@/stores/app'

const props = defineProps<{
  task: any
}>()

const appStore = useAppStore()
const showDeleteConfirm = ref(false)

const statusText = computed(() => {
  const map: Record<string, string> = {
    'done': '已完成',
    'running': '生成中',
    'error': '失败'
  }
  return map[props.task.status] || '未知'
})

const qualityText = computed(() => {
  const map: Record<string, string> = {
    'auto': '自动',
    'low': '低',
    'medium': '中',
    'high': '高'
  }
  return `质量: ${map[props.task.params.quality] || props.task.params.quality}`
})

const getImageUrl = (id: string) => {
  return appStore.getCachedImage(id) || ''
}

const openLightbox = (imgId: string) => {
  appStore.setLightboxImageId(imgId, props.task.outputImages)
}

const handleReuse = () => {
  appStore.reuseConfig(props.task)
}

const handleEdit = () => {
  appStore.editOutputs(props.task)
}

const handleDelete = () => {
  showDeleteConfirm.value = true
}

const confirmDelete = () => {
  appStore.removeTask(props.task)
  showDeleteConfirm.value = false
}

const downloadImage = (originalImgId: string, type: 'original' | 'compressed') => {
  const imgIndex = props.task.outputImages.indexOf(originalImgId)
  const imgId = type === 'original' ? originalImgId : props.task.compressedOutputImages?.[imgIndex] || originalImgId
  const dataUrl = appStore.getCachedImage(imgId)
  if (!dataUrl) return
  
  const match = dataUrl.match(/^data:image\/(\w+);base64,/)
  const ext = match?.[1] ?? 'png'
  const a = document.createElement('a')
  a.href = dataUrl
  a.download = `${props.task.prompt.slice(0, 20) || 'image'}_${type}.${ext}`
  a.click()
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
