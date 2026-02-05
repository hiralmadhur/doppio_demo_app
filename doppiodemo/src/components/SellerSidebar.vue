<template>
  <div class="h-full flex flex-col bg-white border-r border-gray-200 text-gray-700 font-sans">
    <div class="h-14 flex items-center bg-orange-600 text-white shrink-0 px-4 justify-between">
      <div class="flex items-center gap-2 font-bold text-base tracking-wide">
        <span class="text-xl">🏪</span>
        <span v-if="!isCollapsed">Seller Panel</span>
      </div>
      <button @click="$emit('close-mobile')" class="lg:hidden text-white">✕</button>
    </div>

    <div class="flex-1 overflow-y-auto py-2">
      <nav class="space-y-1">
        <button @click="navigate('SellerDashboard')"
          class="w-full flex items-center px-4 py-3 hover:bg-orange-50 transition-colors"
          :class="isActive('SellerDashboard') ? 'bg-orange-50 text-orange-700 border-r-4 border-orange-600' : 'text-gray-600'">
          <span class="text-xl">📊</span><span v-if="!isCollapsed" class="ml-3 font-medium">Dashboard</span>
        </button>
        <button @click="navigate('SellerOrders')"
          class="w-full flex items-center px-4 py-3 hover:bg-orange-50 transition-colors"
          :class="isActive('SellerOrders') ? 'bg-orange-50 text-orange-700 border-r-4 border-orange-600' : 'text-gray-600'">
          <span class="text-xl">📦</span><span v-if="!isCollapsed" class="ml-3 font-medium">Orders</span>
          <span v-if="!isCollapsed && newOrderCount > 0" class="ml-auto bg-red-500 text-white text-[10px] px-2 py-0.5 rounded-full">{{ newOrderCount }}</span>
        </button>
        <button @click="navigate('SellerProducts')"
          class="w-full flex items-center px-4 py-3 hover:bg-orange-50 transition-colors"
          :class="isActive('SellerProducts') ? 'bg-orange-50 text-orange-700 border-r-4 border-orange-600' : 'text-gray-600'">
          <span class="text-xl">🏷️</span><span v-if="!isCollapsed" class="ml-3 font-medium">Products</span>
        </button>
      </nav>
    </div>

    <div class="p-3 border-t border-gray-200 bg-gray-50">
      <button @click="$emit('logout')"
        class="w-full flex items-center justify-center gap-2 text-red-600 font-bold text-xs hover:bg-red-50 py-2 rounded">
        <span>🔴</span><span v-if="!isCollapsed">Logout</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { useRouter, useRoute } from 'vue-router'
const props = defineProps(['isCollapsed', 'newOrderCount'])
const emit = defineEmits(['close-mobile', 'logout'])
const router = useRouter()
const route = useRoute()

const navigate = (name) => {
  router.push({ name })
  emit('close-mobile')
}
const isActive = (name) => route.name === name
</script>