<template>
  <div class="flex h-screen w-screen overflow-hidden bg-white">
    
    <MarketSidebar />

    <div class="flex-1 relative h-full overflow-y-auto pt-16 md:pt-0">
      <router-view />
    </div>

  </div>
</template>

<script setup>
// Path dhyan se check karna (Components folder ke andar)
import MarketSidebar from '@/components/MarketSidebar.vue' 
</script>