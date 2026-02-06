<template>
  <div class="h-full flex flex-col bg-white border-r border-gray-200 text-gray-700 font-sans transition-all duration-300">
    <div class="h-14 flex items-center bg-gray-900 text-white shrink-0 px-3 justify-between">
      <div class="flex items-center gap-2 cursor-pointer w-full" @click="resetView">
        <span class="text-xl">🏪</span>
        <span v-if="!isCollapsed" class="font-bold text-base tracking-wide">Orders</span>
      </div>
      <button @click="$emit('close-mobile')" class="lg:hidden text-gray-400 hover:text-white">✕</button>
    </div>

    <div class="flex-1 overflow-y-auto custom-scrollbar text-[13px]">
      <div v-if="loading" class="p-6 text-center text-gray-400 text-sm">Loading...</div>
      <div v-else-if="!treeData.length" class="p-6 text-center text-gray-400">No active orders.</div>

      <div v-else v-for="pin in treeData" :key="pin.pincode" class="border-b border-gray-50">
        <button @click="toggle('pincode', pin.pincode)" 
          class="w-full flex items-center py-3 hover:bg-gray-50 transition-colors group relative"
          :class="[isCollapsed ? 'justify-center px-0' : 'justify-between px-3', expandedPincodes.includes(pin.pincode) ? 'bg-gray-100 font-bold text-gray-900' : 'text-gray-600']">
          <div class="flex items-center gap-3">
            <span class="text-base text-orange-500">📍</span>
            <span v-if="!isCollapsed" class="text-sm flex items-center gap-2">
                {{ pin.pincode }}
                <span v-if="pin.is_primary" class="text-[9px] bg-yellow-100 text-yellow-700 px-1.5 py-0.5 rounded border border-yellow-200 font-bold uppercase">Primary</span>
            </span>
          </div>
          <span v-if="!isCollapsed" class="text-[10px] text-gray-400 transition-transform" :class="expandedPincodes.includes(pin.pincode) ? 'rotate-180' : ''">▼</span>
        </button>

        <div v-show="expandedPincodes.includes(pin.pincode) && !isCollapsed" class="bg-gray-50/50 pb-1">
          <div v-for="society in pin.societies" :key="society.name">
            <button @click.stop="toggle('society', society.name)" 
              class="w-full flex justify-between pl-8 pr-3 py-2.5 transition-all border-l-[3px]"
              :class="expandedSocieties.includes(society.name) ? 'border-blue-600 text-blue-700 bg-blue-50 font-bold' : 'border-transparent text-gray-600 hover:bg-white'">
              <div class="flex items-center gap-2 truncate"><span class="text-sm opacity-70">🏢</span><span class="truncate">{{ society.name }}</span></div>
              <span class="text-[9px] text-gray-400" :class="expandedSocieties.includes(society.name) ? 'rotate-180' : ''">▼</span>
            </button>

            <div v-show="expandedSocieties.includes(society.name)">
              <div v-for="category in society.categories" :key="category.name">
                <button @click.stop="toggle('category', category.name)" 
                  class="w-full flex justify-between items-center pl-12 pr-3 py-2 text-[11px] uppercase tracking-wider mt-0.5 border-l-[3px] transition-colors"
                  :class="expandedCategories.includes(category.name) ? 'border-orange-500 text-orange-700 bg-orange-50 font-bold' : 'border-transparent text-gray-500 hover:text-gray-800 hover:bg-white'">
                  <div class="flex items-center gap-2"><span>📂</span><span>{{ category.name }}</span></div>
                  <span class="text-[8px] opacity-50" :class="expandedCategories.includes(category.name) ? 'rotate-180' : ''">▼</span>
                </button>

                <div v-show="expandedCategories.includes(category.name)">
                  <div v-for="customer in category.customers" :key="customer.name">
                    <button @click.stop="selectCustomer(customer)" 
                      class="w-full text-left pl-[4rem] pr-3 py-2 text-[12px] flex justify-between items-center group transition-all"
                      :class="activeCustomer === customer.name ? 'bg-yellow-50 text-gray-900 font-bold border-r-4 border-yellow-400 shadow-inner' : 'text-gray-500 hover:bg-white hover:text-gray-900'">
                      <div class="flex items-center gap-2 truncate"><span>👤</span><span class="truncate">{{ customer.name }}</span></div>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="p-3 border-t border-gray-200 bg-gray-50 text-center text-[10px] text-gray-500 font-bold uppercase tracking-wider">Seller Panel</div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
const props = defineProps(['isCollapsed'])
const emit = defineEmits(['close-mobile', 'filter-orders', 'reset-filter'])
const treeData = ref([])
const loading = ref(false)
const expandedPincodes = ref([])
const expandedSocieties = ref([])
const expandedCategories = ref([])
const activeCustomer = ref(null)

const fetchSidebarData = async () => {
    loading.value = true
    try {
        const res = await fetch('/api/method/doppio_demo.api.get_seller_sidebar_data')
        const data = await res.json()
        if (data.message && data.message.status === 'success') {
            treeData.value = data.message.data
            const primary = treeData.value.find(p => p.is_primary)
            if(primary) expandedPincodes.value.push(primary.pincode)
            else if(treeData.value.length > 0) expandedPincodes.value.push(treeData.value[0].pincode)
        }
    } catch(e) { console.error(e) } finally { loading.value = false }
}
onMounted(() => fetchSidebarData())
const toggle = (level, id) => {
    const list = level === 'pincode' ? expandedPincodes : level === 'society' ? expandedSocieties : expandedCategories
    const index = list.value.indexOf(id)
    if (index > -1) list.value.splice(index, 1); else list.value.push(id)
}
const selectCustomer = (customer) => { activeCustomer.value = customer.name; emit('filter-orders', customer.name); emit('close-mobile') }
const resetView = () => { activeCustomer.value = null; emit('reset-filter') }
</script>