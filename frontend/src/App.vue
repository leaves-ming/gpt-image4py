<template>
  <div class="min-h-screen bg-surface-50 font-body text-content-primary">
    <!-- Navigation -->
    <nav class="fixed top-0 left-0 right-0 z-50 bg-white/80 backdrop-blur-xl border-b border-surface-200/60">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between h-16">
          <!-- Logo -->
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 bg-gradient-to-br from-primary-500 to-primary-600 rounded-xl flex items-center justify-center shadow-glow">
              <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
            </div>
            <span class="font-heading font-bold text-xl tracking-tight">AI 图片生成</span>
          </div>

          <!-- Nav Links -->
          <div class="flex items-center gap-6">
          </div>

          <!-- CTA -->
          <div class="flex items-center gap-3">
            <button 
              @click="showSettings = true"
              class="px-4 py-2 text-sm font-medium bg-primary-50 text-primary-600 hover:bg-primary-100 transition-colors rounded-lg"
            >
              设置
            </button>
          </div>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <main class="pt-24 pb-16">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <!-- Input Section -->
        <InputBar />
        
        <!-- Task Grid -->
        <TaskGrid />
      </div>
    </main>

    <!-- Settings Modal -->
    <SettingsModal v-model="showSettings" />

    <!-- Toast -->
    <div v-if="appStore.toast" class="fixed bottom-8 left-1/2 -translate-x-1/2 z-50 px-6 py-3 rounded-full text-sm font-medium shadow-lg animate-toast-enter"
      :class="{
        'bg-content-primary text-white': appStore.toast.type === 'info',
        'bg-green-500 text-white': appStore.toast.type === 'success',
        'bg-red-500 text-white': appStore.toast.type === 'error'
      }"
    >
      {{ appStore.toast.message }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useAppStore } from '@/stores/app'
import SettingsModal from './components/SettingsModal.vue'
import InputBar from './components/InputBar.vue'
import TaskGrid from './components/TaskGrid.vue'

const appStore = useAppStore()
const showSettings = ref(false)

onMounted(() => {
  appStore.initStore()
})
</script>

<style scoped>
.animate-modal-in {
  animation: modal-in 0.25s cubic-bezier(0.16, 1, 0.3, 1) both;
}

.animate-zoom-in {
  animation: zoom-in 0.25s cubic-bezier(0.16, 1, 0.3, 1) both;
}

.animate-toast-enter {
  animation: toast-enter 0.3s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

@keyframes modal-in {
  from { opacity: 0; transform: scale(0.95) translateY(10px); }
  to { opacity: 1; transform: scale(1) translateY(0); }
}

@keyframes zoom-in {
  from { opacity: 0; transform: scale(0.9); }
  to { opacity: 1; transform: scale(1); }
}

@keyframes toast-enter {
  0% { transform: translate(-50%, 16px); opacity: 0; }
  100% { transform: translate(-50%, 0); opacity: 1; }
}
</style>
