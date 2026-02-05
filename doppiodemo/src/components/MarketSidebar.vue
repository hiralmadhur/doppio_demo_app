<template>
    <div
        class="h-full flex flex-col bg-white border-r border-gray-200 text-gray-700 font-sans transition-all duration-300">

        <div class="h-14 flex items-center bg-gray-900 text-white shrink-0 shadow-sm px-3"
            :class="isCollapsed ? 'justify-center' : 'justify-between'">

            <div class="flex items-center gap-2 ">
                <span class="text-xl">🛒</span>
                <span v-if="!isCollapsed" class="font-bold text-base tracking-wide text-gray-100">HyperMart</span>
            </div>

            <button @click="$emit('close-mobile')" class="lg:hidden text-gray-400 hover:text-white">✕</button>
            <button @click="$emit('toggle-collapse')"
                class="hidden lg:block text-gray-400 hover:text-white p-1 rounded hover:bg-gray-800">
                {{ isCollapsed ? '»' : '«' }}
            </button>
        </div>

        <div class="flex-1 overflow-y-auto custom-scrollbar text-[13px]">
            <div v-for="pin in treeData" :key="pin.pincode" class="border-b border-gray-50">

                <button @click="toggle(expandedPincodes, pin.pincode)"
                    class="w-full flex items-center py-2.5 hover:bg-gray-50 transition-colors group"
                    :class="isCollapsed ? 'justify-center px-0' : 'justify-between px-3'">

                    <div class="flex items-center gap-2.5">
                        <span class="text-base group-hover:scale-110 transition-transform">📍</span>
                        <span v-if="!isCollapsed" class="font-semibold text-gray-800">{{ pin.pincode }}</span>
                    </div>
                    <span v-if="!isCollapsed" class="text-[10px] text-gray-400"
                        :class="isOpen(expandedPincodes, pin.pincode) ? 'rotate-180' : ''">▼</span>
                </button>

                <div v-if="isOpen(expandedPincodes, pin.pincode) && !isCollapsed" class="bg-gray-50/50 pb-1">
                    <div v-for="society in pin.societies" :key="society.name">

                        <button @click="toggle(expandedSocieties, society.name)"
                            class="w-full flex justify-between pl-8 pr-3 py-2 hover:bg-blue-50 text-gray-700 hover:text-blue-700 border-l-[3px] border-transparent hover:border-blue-500 transition-all">
                            <div class="flex items-center gap-2 truncate">
                                <span class="text-sm opacity-70">🏢</span>
                                <span class="font-medium truncate">{{ society.name }}</span>
                            </div>
                        </button>

                        <div v-if="isOpen(expandedSocieties, society.name)">
                            <div v-for="category in society.categories" :key="category.name">
                                <button @click="toggle(expandedCategories, category.name)"
                                    class="w-full flex items-center gap-2 pl-12 pr-3 py-1 text-[11px] font-bold text-gray-400 uppercase tracking-wider hover:text-orange-600 mt-0.5">
                                    <span>📂</span><span>{{ category.name }}</span>
                                </button>

                                <div v-if="isOpen(expandedCategories, category.name)">
                                    <div v-for="seller in category.sellers" :key="seller.name">
                                        <button @click="selectSeller(seller, pin.pincode)"
                                            class="w-full text-left pl-[4rem] pr-3 py-2 text-[13px] text-gray-600 hover:bg-white hover:text-gray-900 flex justify-between items-center group transition-all"
                                            :class="{ 'bg-yellow-50 text-gray-900 font-bold border-r-4 border-yellow-400': selectedSellerName === seller.name }">
                                            <div class="flex items-center gap-2 truncate">
                                                <span>🏪</span><span class="truncate">{{ seller.name }}</span>
                                            </div>
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="p-3 border-t border-gray-200 bg-gray-50 shrink-0">
            <button @click="handleLogout"
                class="w-full flex items-center justify-center gap-2 text-red-600 font-bold text-xs hover:bg-red-50 py-2 rounded border border-transparent hover:border-red-100 transition-colors">
                <span>🔴</span><span v-if="!isCollapsed">Logout</span>
            </button>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const props = defineProps(['isCollapsed'])
const emit = defineEmits(['select-action', 'close-mobile', 'toggle-collapse'])

const treeData = ref([])
const expandedPincodes = ref([])
const expandedSocieties = ref([])
const expandedCategories = ref([])
const selectedSellerName = ref("")

const toggle = (arr, id) => {
    const idx = arr.indexOf(id); if (idx > -1) arr.splice(idx, 1); else arr.push(id)
}
const isOpen = (arr, id) => arr.includes(id)

const selectSeller = (seller, pincode) => {
    selectedSellerName.value = seller.name
    emit('select-action', { action: 'Show Seller Items', seller, pincode })
    emit('close-mobile')
}

const fetchSidebarData = async () => {
    try {
        const res = await fetch('/api/method/doppio_demo.api.get_customer_sidebar_data')
        if (!res.ok) {
            console.error(`Sidebar API Error: ${res.status}`);
            return;
        }
       const data = await res.json()
        if (data.message && data.message.status === 'success') {
            treeData.value = data.message.data
        }
    } catch (e) {
        console.error("Sidebar fetch failed:", e)
    }
}
onMounted(() => fetchSidebarData())

import { session } from "../data/session"

const handleLogout = async () => {
    try {

        await fetch('/api/method/logout', { method: 'POST' })
        session.isLoggedIn = false
        session.user = null
        window.location.href = '/login'
    } catch (e) {
        window.location.href = '/login'
    }
}
</script>