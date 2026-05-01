<template>
  <div class="p-6">
    <!-- Filter Bar -->
    <div class="flex flex-wrap items-center justify-between gap-4 mb-6">
      <div class="flex items-center gap-3 flex-wrap">
        <!-- Search -->
        <div class="relative">
          <svg class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-content-muted" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 0 0114 0z" />
          </svg>
          <input
            v-model="searchQuery"
            type="text"
            placeholder="搜索提示词..."
            class="pl-10 pr-4 py-2 bg-white border border-surface-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary-500/20 focus:border-primary-500 transition-all w-64"
          />
        </div>

        <!-- Status Filter -->
        <select
          v-model="filterStatus"
          class="px-3 py-2 bg-white border border-surface-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary-500/20 focus:border-primary-500 transition-all cursor-pointer"
        >
          <option value="all">全部状态</option>
          <option value="running">生成中</option>
          <option value="done">已完成</option>
          <option value="error">失败</option>
        </select>

        <!-- 批量操作按钮 -->
        <button
          @click="appStore.setBatchSelectMode(!appStore.batchSelectMode)"
          class="px-3 py-2 bg-white border border-surface-200 hover:border-primary-500 hover:text-primary-600 rounded-lg text-sm transition-all"
          :class="{ 'bg-primary-50 border-primary-500 text-primary-600': appStore.batchSelectMode }"
        >
          {{ appStore.batchSelectMode ? '退出批量选择' : '批量选择' }}
        </button>

        <template v-if="appStore.batchSelectMode">
          <button
            @click="appStore.selectAllTasks"
            class="px-3 py-2 bg-white border border-surface-200 hover:border-primary-500 hover:text-primary-600 rounded-lg text-sm transition-all"
          >
            全选
          </button>
          <button
            @click="appStore.clearSelectedTasks"
            class="px-3 py-2 bg-white border border-surface-200 hover:border-primary-500 hover:text-primary-600 rounded-lg text-sm transition-all"
          >
            取消选择
          </button>
          <button
            @click="handleBatchDownload"
            class="px-3 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-lg text-sm transition-all"
            :disabled="appStore.selectedTaskIds.size === 0"
          >
            打包下载选中（{{ appStore.selectedTaskIds.size }}）
          </button>
        </template>
      </div>

      <!-- Count -->
      <div class="text-sm text-content-muted">
        共 <span class="font-semibold text-content-primary">{{ filteredTasks.length }}</span> 条记录
      </div>
    </div>

        <!-- Status Filter -->
        <select
          v-model="filterStatus"
          class="px-3 py-2 bg-white border border-surface-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary-500/20 focus:border-primary-500 transition-all cursor-pointer"
        >
          <option value="all">全部状态</option>
          <option value="running">生成中</option>
          <option value="done">已完成</option>
          <option value="error">失败</option>
        </select>
      </div>

      <!-- Count -->
      <div class="text-sm text-content-muted">
        共 <span class="font-semibold text-content-primary">{{ filteredTasks.length }}</span> 条记录
      </div>
    </div>

    <!-- Empty State -->
    <div
      v-if="filteredTasks.length === 0"
      class="bg-surface-50 rounded-2xl p-12 text-center border border-surface-200 border-dashed"
    >
      <div class="w-16 h-16 bg-surface-100 rounded-full flex items-center justify-center mx-auto mb-4">
        <svg class="w-8 h-8 text-content-muted" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
        </svg>
      </div>
      <h3 class="font-heading text-lg font-semibold text-content-primary mb-2">暂无生成记录</h3>
      <p class="text-sm text-content-secondary">输入提示词开始生成第一张图片吧</p>
    </div>

    <!-- Task Grid -->
    <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-5">
      <TaskCard
        v-for="task in filteredTasks"
        :key="task.id"
        :task="task"
      />
    </div>

    <!-- Lightbox -->
    <div 
      v-if="lightboxImageId && lightboxImages.length > 0" 
      class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/90 backdrop-blur-sm"
      @click="closeLightbox"
    >
      <div class="relative max-w-5xl max-h-[90vh]">
        <img 
          :src="lightboxImages[currentImageIndex]" 
          class="max-w-full max-h-[85vh] rounded-lg shadow-2xl"
          @click.stop
        />
        
        <!-- Navigation -->
        <button 
          v-if="lightboxImages.length > 1"
          @click.stop="prevImage"
          class="absolute left-4 top-1/2 -translate-y-1/2 w-10 h-10 bg-black/50 hover:bg-black/70 text-white rounded-full flex items-center justify-center transition-colors"
        >
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
        </button>
        <button 
          v-if="lightboxImages.length > 1"
          @click.stop="nextImage"
          class="absolute right-4 top-1/2 -translate-y-1/2 w-10 h-10 bg-black/50 hover:bg-black/70 text-white rounded-full flex items-center justify-center transition-colors"
        >
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
          </svg>
        </button>

        <!-- Counter -->
        <div 
          v-if="lightboxImages.length > 1"
          class="absolute bottom-4 left-1/2 -translate-x-1/2 px-4 py-1.5 bg-black/50 text-white text-sm rounded-full"
        >
          {{ currentImageIndex + 1 }} / {{ lightboxImages.length }}
        </div>
      </div>

      <!-- Close Button -->
      <button 
        @click="closeLightbox"
        class="absolute top-4 right-4 w-10 h-10 bg-black/50 hover:bg-black/70 text-white rounded-full flex items-center justify-center transition-colors"
      >
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { useAppStore } from '@/stores/app'
import { batchDownload } from '@/api'
import TaskCard from './TaskCard.vue'

const appStore = useAppStore()
const currentImageIndex = ref(0)

const searchQuery = computed({
  get: () => appStore.searchQuery,
  set: (val) => appStore.setSearchQuery(val)
})

const filterStatus = computed({
  get: () => appStore.filterStatus,
  set: (val) => appStore.setFilterStatus(val)
})

const filteredTasks = computed(() => appStore.filteredTasks)

const lightboxImageId = computed(() => appStore.lightboxImageId)
const lightboxImageList = computed(() => appStore.lightboxImageList)

const lightboxImages = computed(() => {
  return lightboxImageList.value.map(id => appStore.getCachedImage(id) || '')
})

watch(lightboxImageId, (newId) => {
  if (newId) {
    currentImageIndex.value = lightboxImageList.value.indexOf(newId)
  }
})

const prevImage = () => {
  currentImageIndex.value = (currentImageIndex.value - 1 + lightboxImages.value.length) % lightboxImages.value.length
}

const nextImage = () => {
  currentImageIndex.value = (currentImageIndex.value + 1) % lightboxImages.value.length
}

const closeLightbox = () => {
  appStore.setLightboxImageId(null)
}

const handleBatchDownload = async () => {
  if (appStore.selectedTaskIds.size === 0) return
  appStore.showToast('正在打包下载...', 'info')
  
  // 收集所有选中任务的原图URL
  const imageUrls: string[] = []
  for (const taskId of appStore.selectedTaskIds) {
    const task = appStore.tasks.find(t => t.id === taskId)
    if (task && task.outputImages) {
      task.outputImages.forEach(imgId => {
        const url = appStore.getCachedImage(imgId)
        if (url) imageUrls.push(url)
      })
    }
  }

  if (imageUrls.length === 0) {
    appStore.showToast('没有可下载的图片', 'error')
    return
  }

  try {
    await batchDownload(imageUrls)
    appStore.showToast(`下载完成，共 ${imageUrls.length} 张图片`, 'success')
    appStore.setBatchSelectMode(false)
  } catch (e) {
    appStore.showToast('下载失败，请重试', 'error')
  }
}
</script>
