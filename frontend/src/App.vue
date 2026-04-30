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
            <span class="font-heading font-bold text-xl tracking-tight">AI Canvas</span>
          </div>

          <!-- Nav Links -->
          <div class="hidden md:flex items-center gap-8">
            <a href="#features" class="text-sm font-medium text-content-secondary hover:text-primary-600 transition-colors">功能</a>
            <a href="#demo" class="text-sm font-medium text-content-secondary hover:text-primary-600 transition-colors">体验</a>
            <a href="#gallery" class="text-sm font-medium text-content-secondary hover:text-primary-600 transition-colors">画廊</a>
          </div>

          <!-- CTA -->
          <div class="flex items-center gap-3">
            <button 
              @click="showSettings = true"
              class="p-2 text-content-secondary hover:text-primary-600 transition-colors rounded-lg hover:bg-primary-50"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
            </button>
            <button 
              @click="scrollToDemo"
              class="px-5 py-2.5 bg-primary-600 hover:bg-primary-700 text-white text-sm font-semibold rounded-lg transition-all shadow-soft hover:shadow-glow"
            >
              立即创作
            </button>
          </div>
        </div>
      </div>
    </nav>

    <!-- Hero Section -->
    <section class="relative pt-32 pb-20 lg:pt-40 lg:pb-32 overflow-hidden">
      <!-- Background Elements -->
      <div class="absolute inset-0 pointer-events-none">
        <div class="absolute top-20 left-1/4 w-96 h-96 bg-primary-400/20 rounded-full blur-3xl"></div>
        <div class="absolute bottom-20 right-1/4 w-80 h-80 bg-primary-300/20 rounded-full blur-3xl"></div>
      </div>

      <div class="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center max-w-3xl mx-auto">
          <!-- Badge -->
          <div class="inline-flex items-center gap-2 px-4 py-2 bg-primary-50 border border-primary-200 rounded-full mb-8">
            <span class="w-2 h-2 bg-primary-500 rounded-full animate-pulse"></span>
            <span class="text-sm font-medium text-primary-700">基于 GPT Image API</span>
          </div>

          <!-- Title -->
          <h1 class="font-heading text-4xl sm:text-5xl lg:text-6xl font-bold tracking-tight mb-6 leading-tight">
            <span class="text-content-primary">用文字创造</span>
            <br />
            <span class="bg-gradient-to-r from-primary-600 to-primary-500 bg-clip-text text-transparent">无限视觉可能</span>
          </h1>

          <!-- Description -->
          <p class="text-lg sm:text-xl text-content-secondary mb-10 max-w-2xl mx-auto leading-relaxed">
            AI Canvas 是一款简洁高效的 AI 绘画工具，支持文本生图和图片编辑。只需描述你的想法，让 AI 为你创作。
          </p>

          <!-- CTA Buttons -->
          <div class="flex flex-col sm:flex-row items-center justify-center gap-4">
            <button 
              @click="scrollToDemo"
              class="w-full sm:w-auto px-8 py-4 bg-primary-600 hover:bg-primary-700 text-white font-semibold rounded-xl transition-all shadow-soft hover:shadow-glow-lg flex items-center justify-center gap-2"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
              开始创作
            </button>
            <button 
              @click="showHelp = true"
              class="w-full sm:w-auto px-8 py-4 bg-white hover:bg-surface-50 text-content-primary font-semibold rounded-xl border border-surface-200 transition-all shadow-soft flex items-center justify-center gap-2"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              使用帮助
            </button>
          </div>
        </div>

        <!-- Preview Images -->
        <div class="mt-16 grid grid-cols-2 md:grid-cols-4 gap-4 max-w-4xl mx-auto">
          <div 
            v-for="(img, i) in previewImages" 
            :key="i"
            class="group relative aspect-square rounded-2xl overflow-hidden shadow-soft bg-surface-100"
          >
            <img :src="img" class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110" />
            <div class="absolute inset-0 bg-gradient-to-t from-black/40 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
          </div>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section id="features" class="py-20 bg-white">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center max-w-2xl mx-auto mb-16">
          <h2 class="font-heading text-3xl font-bold text-content-primary mb-4">强大而简洁的功能</h2>
          <p class="text-content-secondary">专注于核心体验，让创作流程更加顺畅高效</p>
        </div>

        <div class="grid md:grid-cols-3 gap-8">
          <div 
            v-for="(feature, i) in features" 
            :key="i"
            class="group p-8 bg-surface-50 rounded-2xl border border-surface-200 hover:border-primary-300 transition-all hover:shadow-soft"
          >
            <div class="w-12 h-12 bg-primary-100 rounded-xl flex items-center justify-center mb-6 group-hover:bg-primary-600 transition-colors">
              <svg class="w-6 h-6 text-primary-600 group-hover:text-white transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="feature.icon" />
              </svg>
            </div>
            <h3 class="font-heading text-xl font-semibold text-content-primary mb-3">{{ feature.title }}</h3>
            <p class="text-content-secondary leading-relaxed">{{ feature.desc }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Demo Section - Main App Interface -->
    <section id="demo" class="py-20 bg-surface-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center max-w-2xl mx-auto mb-12">
          <h2 class="font-heading text-3xl font-bold text-content-primary mb-4">开始创作</h2>
          <p class="text-content-secondary">输入提示词或上传参考图，AI 将为你生成独特的视觉作品</p>
        </div>

        <!-- Main App Container -->
        <div class="bg-white rounded-2xl shadow-soft border border-surface-200 overflow-hidden">
          <!-- App Header -->
          <Header />

          <!-- Input Area -->
          <InputBar />

          <!-- Task Grid -->
          <TaskGrid />
        </div>
      </div>
    </section>

    <!-- Gallery Section -->
    <section id="gallery" class="py-20 bg-white">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center max-w-2xl mx-auto mb-12">
          <h2 class="font-heading text-3xl font-bold text-content-primary mb-4">灵感画廊</h2>
          <p class="text-content-secondary">探索 AI 创作的无限可能，激发你的创意灵感</p>
        </div>

        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div 
            v-for="(img, i) in galleryImages" 
            :key="i"
            class="group relative aspect-[4/5] rounded-xl overflow-hidden bg-surface-100 cursor-pointer"
            @click="openLightbox(img)"
          >
            <img :src="img.url" class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105" />
            <div class="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-all duration-300">
              <div class="absolute bottom-0 left-0 right-0 p-4">
                <p class="text-white text-sm font-medium line-clamp-2">{{ img.prompt }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="bg-surface-900 py-12">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex flex-col md:flex-row items-center justify-between gap-6">
          <div class="flex items-center gap-3">
            <div class="w-8 h-8 bg-gradient-to-br from-primary-500 to-primary-600 rounded-lg flex items-center justify-center">
              <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
            </div>
            <span class="font-heading font-bold text-lg text-white">AI Canvas</span>
          </div>
          <p class="text-content-muted text-sm">基于 GPT Image API • 本地存储保护隐私</p>
          <div class="flex items-center gap-6">
            <a href="#" class="text-content-muted hover:text-white text-sm transition-colors">GitHub</a>
            <a href="#" class="text-content-muted hover:text-white text-sm transition-colors">文档</a>
          </div>
        </div>
      </div>
    </footer>

    <!-- Help Modal -->
    <div v-if="showHelp" class="fixed inset-0 z-50 flex items-center justify-center p-4">
      <div class="absolute inset-0 bg-black/50 backdrop-blur-sm" @click="showHelp = false"></div>
      <div class="relative bg-white rounded-2xl shadow-xl max-w-lg w-full p-6 animate-modal-in">
        <div class="flex items-center justify-between mb-6">
          <h3 class="font-heading text-xl font-semibold">使用帮助</h3>
          <button @click="showHelp = false" class="p-2 hover:bg-surface-100 rounded-lg transition-colors">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <div class="space-y-4">
          <div class="p-4 bg-surface-50 rounded-xl">
            <h4 class="font-semibold text-content-primary mb-2">1. 配置 API</h4>
            <p class="text-sm text-content-secondary">点击右上角「设置」按钮，填入你的 API 地址、密钥和模型名称即可使用。</p>
          </div>
          <div class="p-4 bg-surface-50 rounded-xl">
            <h4 class="font-semibold text-content-primary mb-2">2. 生成图片</h4>
            <p class="text-sm text-content-secondary">输入提示词，选择尺寸、质量等参数，点击「生成图片」即可。也可以上传参考图进行图片编辑。</p>
          </div>
          <div class="p-4 bg-surface-50 rounded-xl">
            <h4 class="font-semibold text-content-primary mb-2">3. 本地存储</h4>
            <p class="text-sm text-content-secondary">所有任务记录和图片都存储在你的浏览器本地，不会上传到任何服务器，非常安全。</p>
          </div>
          <div class="p-4 bg-surface-50 rounded-xl">
            <h4 class="font-semibold text-content-primary mb-2">4. 数据导出导入</h4>
            <p class="text-sm text-content-secondary">可以导出所有数据为ZIP文件备份，也可以导入之前的备份数据。</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Lightbox -->
    <div v-if="lightboxImage" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/90 backdrop-blur-sm" @click="lightboxImage = null">
      <img :src="lightboxImage.url" class="max-w-full max-h-full rounded-lg shadow-2xl animate-zoom-in" @click.stop />
      <button @click="lightboxImage = null" class="absolute top-4 right-4 p-2 text-white/70 hover:text-white bg-black/50 rounded-full">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </div>

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
import Header from './components/Header.vue'
import InputBar from './components/InputBar.vue'
import TaskGrid from './components/TaskGrid.vue'

const appStore = useAppStore()
const showHelp = ref(false)
const showSettings = ref(false)
const lightboxImage = ref<{ url: string, prompt: string } | null>(null)

// Preview images for hero section
const previewImages = [
  'https://images.unsplash.com/photo-1686191128892-3b37add4a934?w=400&h=400&fit=crop',
  'https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=400&h=400&fit=crop',
  'https://images.unsplash.com/photo-1633177317976-3f9bc45e1d1d?w=400&h=400&fit=crop',
  'https://images.unsplash.com/photo-1614730321146-b6fa6a46bcb4?w=400&h=400&fit=crop',
]

const features = [
  {
    title: '文本生图',
    desc: '只需输入文字描述，AI 即可根据你的描述生成精美的图片。支持多种风格和尺寸选择。',
    icon: 'M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z'
  },
  {
    title: '图片编辑',
    desc: '上传参考图片，结合文字提示词进行编辑和再创作。支持多张图片同时编辑。',
    icon: 'M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z'
  },
  {
    title: '本地存储',
    desc: '所有生成的图片和任务记录都存储在浏览器本地，保护你的隐私和数据安全。',
    icon: 'M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z'
  }
]

const galleryImages = [
  { url: 'https://images.unsplash.com/photo-1686191128892-3b37add4a934?w=600&h=750&fit=crop', prompt: 'A serene Japanese garden with cherry blossoms, watercolor style' },
  { url: 'https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=600&h=750&fit=crop', prompt: 'Abstract geometric art with vibrant colors, modern minimalist design' },
  { url: 'https://images.unsplash.com/photo-1633177317976-3f9bc45e1d1d?w=600&h=750&fit=crop', prompt: 'Futuristic cityscape at sunset, cyberpunk aesthetic' },
  { url: 'https://images.unsplash.com/photo-1614730321146-b6fa6a46bcb4?w=600&h=750&fit=crop', prompt: 'Cosmic nebula with swirling galaxies, deep space photography' },
  { url: 'https://images.unsplash.com/photo-1634017839464-5c339ez3d0e2?w=600&h=750&fit=crop', prompt: 'Mystical forest with bioluminescent plants, fantasy art style' },
  { url: 'https://images.unsplash.com/photo-1617791160505-6f00504e3519?w=600&h=750&fit=crop', prompt: 'Cute robot in a field of flowers, 3D render, Pixar style' },
  { url: 'https://images.unsplash.com/photo-1567359781514-3b964e2b04d6?w=600&h=750&fit=crop', prompt: 'Vintage camera on wooden desk, still life photography' },
  { url: 'https://images.unsplash.com/photo-1579783902614-a3fb3927b6a5?w=600&h=750&fit=crop', prompt: 'Colorful abstract fluid art, acrylic pour painting' },
]

const scrollToDemo = () => {
  document.getElementById('demo')?.scrollIntoView({ behavior: 'smooth' })
}

const openLightbox = (img: { url: string, prompt: string }) => {
  lightboxImage.value = img
}

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
