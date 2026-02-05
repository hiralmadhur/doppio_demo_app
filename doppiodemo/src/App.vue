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
         <customer-view
    @toggle-mobile="isMobileSidebarOpen = !isMobileSidebarOpen" 
    @open-sidebar="isDesktopCollapsed = false" 
/>
    </div>

    <div class="flex-1 flex flex-col min-w-0 h-full w-full relative transition-all duration-300">
        <router-view 
            @toggle-mobile="isMobileSidebarOpen = !isMobileSidebarOpen"
        />
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, provide } from 'vue'
import { useRouter } from 'vue-router'
import MarketSidebar from './components/MarketSidebar.vue'

const router = useRouter()
const isMobileSidebarOpen = ref(false)
const isDesktopCollapsed = ref(false)
const isMobile = ref(false)

// Handle Sidebar Clicks - Navigate via Router
const handleSelection = (data) => {
    if (data.action === 'Show Seller Items') {
        // Route change karein seller ke naam ke saath
        router.push({ 
            name: 'SellerItems', 
            params: { sellerName: data.seller.name } 
        })
    }
    isMobileSidebarOpen.value = false
}

const checkScreen = () => {
    isMobile.value = window.innerWidth < 1024
    if (!isMobile.value) {
        isMobileSidebarOpen.value = false 
    }
}

onMounted(() => {
    checkScreen()
    window.addEventListener('resize', checkScreen)
})
onUnmounted(() => window.removeEventListener('resize', checkScreen))
</script>