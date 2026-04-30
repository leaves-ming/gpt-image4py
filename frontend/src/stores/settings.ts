import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { AppSettings } from '@/types'
import { DEFAULT_SETTINGS } from '@/types'

export const useSettingsStore = defineStore('settings', () => {
  const settings = ref<AppSettings>({ ...DEFAULT_SETTINGS })

  const loadSettings = async () => {
    const saved = localStorage.getItem('app_settings')
    if (saved) {
      settings.value = { ...settings.value, ...JSON.parse(saved) }
    }
  }

  const saveSettings = async (newSettings: Partial<AppSettings>) => {
    settings.value = { ...settings.value, ...newSettings }
    localStorage.setItem('app_settings', JSON.stringify(settings.value))
  }

  return {
    settings,
    loadSettings,
    saveSettings
  }
})
