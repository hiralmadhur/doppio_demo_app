<template>
  <Transition name="fade">
    <div v-if="isVisible" class="fixed inset-0 z-[60] flex items-center justify-center p-4 bg-black/40 backdrop-blur-sm">
      <div class="bg-white rounded-xl shadow-2xl max-w-sm w-full p-6 transform transition-all scale-100">
        <div class="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-red-100 mb-4">
          <span class="text-xl text-red-600">⚠️</span>
        </div>
        
        <div class="text-center">
          <h3 class="text-lg font-bold text-gray-900">{{ title }}</h3>
          <p class="text-sm text-gray-500 mt-2">{{ message }}</p>
        </div>

        <div class="mt-6 flex gap-3">
          <button @click="cancel" 
            class="flex-1 px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 font-semibold rounded-lg text-sm transition-colors">
            No, Cancel
          </button>
          <button @click="confirm" 
            class="flex-1 px-4 py-2 bg-red-600 hover:bg-red-700 text-white font-semibold rounded-lg text-sm shadow-md transition-all active:scale-95">
            Yes, Proceed
          </button>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { ref } from 'vue'

const isVisible = ref(false)
const title = ref('')
const message = ref('')
let resolvePromise = null

const open = (t, m) => {
  title.value = t
  message.value = m
  isVisible.value = true
  return new Promise((resolve) => {
    resolvePromise = resolve
  })
}

const confirm = () => {
  isVisible.value = false
  if (resolvePromise) resolvePromise(true)
}

const cancel = () => {
  isVisible.value = false
  if (resolvePromise) resolvePromise(false)
}

defineExpose({ open })
</script>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.2s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>