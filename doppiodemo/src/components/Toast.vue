<template>
  <div class="fixed top-5 right-5 z-[70] flex flex-col gap-3 pointer-events-none">
    <TransitionGroup name="toast">
      <div v-for="toast in toasts" :key="toast.id" 
           class="pointer-events-auto flex items-center gap-3 px-4 py-3 rounded-lg shadow-xl border-l-4 min-w-[300px] bg-white transform transition-all duration-300"
           :class="[
             toast.type === 'success' ? 'border-green-500' : 
             toast.type === 'error' ? 'border-red-500' : 
             'border-blue-500' 
           ]">
        
        <span class="text-xl">
          {{ toast.type === 'success' ? '✅' : toast.type === 'error' ? '❌' : 'ℹ️' }}
        </span>
        
        <div class="flex-1">
          <h4 class="text-sm font-bold" 
              :class="[
                toast.type === 'success' ? 'text-green-700' : 
                toast.type === 'error' ? 'text-red-700' : 
                'text-blue-700'
              ]">
            {{ toast.type === 'success' ? 'Success' : toast.type === 'error' ? 'Error' : 'Message' }}
          </h4>
          <p class="text-xs text-gray-600 font-medium">{{ toast.message }}</p>
        </div>

        <button @click="removeToast(toast.id)" class="text-gray-400 hover:text-gray-600">✕</button>
      </div>
    </TransitionGroup>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const toasts = ref([])
let toastId = 0


const add = (message, type = 'info') => {
  const id = toastId++
  toasts.value.push({ id, message, type })
  setTimeout(() => removeToast(id), 4000) 
}

const removeToast = (id) => {
  toasts.value = toasts.value.filter(t => t.id !== id)
}

defineExpose({ add })
</script>

<style scoped>
.toast-enter-active, .toast-leave-active { transition: all 0.3s ease; }
.toast-enter-from { opacity: 0; transform: translateY(-30px); }
.toast-leave-to { opacity: 0; transform: translateY(-30px); }
</style>