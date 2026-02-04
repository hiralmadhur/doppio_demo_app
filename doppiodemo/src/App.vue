<template>
  <div class="flex h-screen bg-gray-50 overflow-hidden relative">
    
    <div v-if="isMobileSidebarOpen" @click="isMobileSidebarOpen = false" 
         class="fixed inset-0 bg-black/60 z-40 lg:hidden backdrop-blur-sm transition-opacity">
    </div>

    <div class="fixed lg:static inset-y-0 left-0 z-50 bg-white shadow-2xl lg:shadow-none transform transition-all duration-300 ease-in-out h-full border-r border-gray-200"
         :class="[
            isMobileSidebarOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0',
            isDesktopCollapsed ? 'w-20' : 'w-72 xl:w-80'
         ]">
         
         <MarketSidebar 
            :isCollapsed="isDesktopCollapsed && !isMobile"
            @select-action="handleSelection"
            @close-mobile="isMobileSidebarOpen = false"
            @toggle-collapse="isDesktopCollapsed = !isDesktopCollapsed"
         />
    </div>

    <div class="flex-1 flex flex-col min-w-0 h-full w-full relative transition-all duration-300">
        <CustomerView 
            :incomingAction="currentAction"
            @toggle-mobile="isMobileSidebarOpen = !isMobileSidebarOpen"
        />
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
// ✅ Correct filenames imported based on your structure
import MarketSidebar from './components/MarketSidebar.vue'
import CustomerView from './pages/CustomerView.vue'

const isMobileSidebarOpen = ref(false)
const isDesktopCollapsed = ref(false)
const isMobile = ref(false)
const currentAction = ref(null)

const handleSelection = (data) => {
    currentAction.value = data
}

const checkScreen = () => {
    isMobile.value = window.innerWidth < 1024
    if (!isMobile.value) {
        isMobileSidebarOpen.value = false // Reset mobile drawer on desktop
    }
}

onMounted(() => {
    checkScreen()
    window.addEventListener('resize', checkScreen)
})
onUnmounted(() => window.removeEventListener('resize', checkScreen))
</script>