<template>
    <div
        class="h-full flex flex-col bg-white border-r border-gray-200 text-gray-700 font-sans transition-all duration-300">

        <div class="h-14 flex items-center bg-gray-900 text-white shrink-0 shadow-sm px-3 hover:bg-gray-800 transition-colors"
            :class="isCollapsed ? 'justify-center' : 'justify-between'">

            <div class="flex items-center gap-2 overflow-hidden cursor-pointer w-full" @click="resetShop">
                <span class="text-xl">🛒</span>
                <span v-if="!isCollapsed" class="font-bold text-base tracking-wide text-gray-100">HyperMart</span>
            </div>

            <button @click="$emit('close-mobile')" class="lg:hidden text-gray-400 hover:text-white">✕</button>
            <button @click="$emit('toggle-collapse')"
                class="hidden lg:block text-gray-400 hover:text-white p-1 rounded hover:bg-gray-800 ml-auto">
                {{ isCollapsed ? '»' : '«' }}
            </button>
        </div>

        <div class="flex-1 overflow-y-auto custom-scrollbar text-[13px]">
            <div v-if="loading" class="p-4 text-center text-gray-400">Loading map...</div>

            <div v-else v-for="pin in treeData" :key="pin.pincode" class="border-b border-gray-50">

                <button @click="handleLevelClick('pincode', pin.pincode, {})"
                    class="w-full flex items-center py-3 hover:bg-gray-50 transition-colors group relative" :class="[
                        isCollapsed ? 'justify-center px-0' : 'justify-between px-3',
                        isPincodeActive(pin.pincode) ? 'bg-gray-100 text-gray-900 font-extrabold' : 'text-gray-600'
                    ]">
                    <div v-if="isPincodeActive(pin.pincode)" class="absolute left-0 top-0 bottom-0 w-1 bg-gray-800">
                    </div>

                    <div class="flex items-center gap-3">
                        <span class="text-base transition-transform"
                            :class="isPincodeActive(pin.pincode) ? 'scale-110' : 'group-hover:scale-110'">📍</span>
                        <span v-if="!isCollapsed" class="text-sm">{{ pin.pincode }}</span>
                    </div>
                    <span v-if="!isCollapsed" class="text-[10px] text-gray-400 transition-transform duration-300"
                        :class="expandedPincodes.includes(pin.pincode) ? 'rotate-180' : ''">▼</span>
                </button>

                <div v-show="expandedPincodes.includes(pin.pincode) && !isCollapsed"
                    class="bg-gray-50/50 pb-1 overflow-hidden transition-all">
                    <div v-for="society in pin.societies" :key="society.name">

                        <button @click.stop="handleLevelClick('society', society.name, { pincode: pin.pincode })"
                            class="w-full flex justify-between pl-8 pr-3 py-2.5 transition-all border-l-[3px] group"
                            :class="[
                                isSocietyActive(society.name)
                                    ? 'bg-blue-50 text-blue-700 font-bold border-blue-600 shadow-sm'
                                    : 'text-gray-600 hover:text-gray-900 hover:bg-white border-transparent'
                            ]">
                            <div class="flex items-center gap-2 truncate">
                                <span class="text-sm opacity-70 group-hover:scale-110 transition-transform">🏢</span>
                                <span class="truncate">{{ society.name }}</span>
                            </div>
                            <span class="text-[9px] text-gray-400 transition-transform duration-300"
                                :class="expandedSocieties.includes(society.name) ? 'rotate-180' : ''">▼</span>
                        </button>

                        <div v-show="expandedSocieties.includes(society.name)" class="transition-all">
                            <div v-for="category in society.categories" :key="category.name">
                                <button
                                    @click.stop="handleLevelClick('category', category.name, { pincode: pin.pincode, society: society.name })"
                                    class="w-full flex justify-between items-center gap-2 pl-12 pr-3 py-2 text-[11px] uppercase tracking-wider mt-0.5 transition-colors border-l-[3px] border-transparent"
                                    :class="[
                                        isCategoryActive(category.name)
                                            ? 'text-orange-700 font-bold bg-orange-50 border-l-orange-500'
                                            : 'text-gray-500 font-medium hover:text-gray-800 hover:bg-white'
                                    ]">
                                    <div class="flex items-center gap-2">
                                        <span>📂</span><span>{{ category.name }}</span>
                                    </div>
                                    <span class="text-[8px] opacity-50 transition-transform duration-300"
                                        :class="expandedCategories.includes(category.name) ? 'rotate-180' : ''">▼</span>
                                </button>

                                <div v-show="expandedCategories.includes(category.name)">
                                    <div v-for="seller in category.sellers" :key="seller.name">
                                        <button
                                            @click.stop="navigateTo('seller', { pincode: pin.pincode, society: society.name, category: category.name, sellerName: seller.name })"
                                            class="w-full text-left pl-[4rem] pr-3 py-2 text-[12px] flex justify-between items-center group transition-all"
                                            :class="[
                                                isSellerActive(seller.name, category.name)
                                                    ? 'bg-yellow-50 text-gray-900 font-bold border-r-4 border-yellow-400 shadow-inner'
                                                    : 'text-gray-500 hover:bg-white hover:text-gray-900'
                                            ]">
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
import { ref, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { session } from "../data/session"

const props = defineProps(['isCollapsed'])
const emit = defineEmits(['close-mobile', 'toggle-collapse'])

const router = useRouter()
const route = useRoute()
const treeData = ref([])
const loading = ref(true)

const expandedPincodes = ref([])
const expandedSocieties = ref([])
const expandedCategories = ref([])

const isPincodeActive = (pincode) => route.params.pincode === pincode
const isSocietyActive = (societyName) => route.params.society === societyName
const isCategoryActive = (catName) => route.params.category === catName
const isSellerActive = (sellerName, catName) => route.params.sellerName === sellerName && route.params.category === catName

const handleLevelClick = (level, id, context) => {
    if (level === 'pincode') {
        if (expandedPincodes.value.includes(id)) expandedPincodes.value = []
        else expandedPincodes.value = [id]
        navigateTo('pincode', { pincode: id })
    }
    else if (level === 'society') {
        if (expandedSocieties.value.includes(id)) expandedSocieties.value = []
        else expandedSocieties.value = [id]
        navigateTo('society', { pincode: context.pincode, society: id })
    }
    else if (level === 'category') {
        if (expandedCategories.value.includes(id)) expandedCategories.value = []
        else expandedCategories.value = [id]
        navigateTo('category', { pincode: context.pincode, society: context.society, category: id })
    }
}

const navigateTo = (level, params) => {
    let routeName = ''
    if (level === 'pincode') routeName = 'ShopPincode'
    if (level === 'society') routeName = 'ShopSociety'
    if (level === 'category') routeName = 'ShopCategory'
    if (level === 'seller') {
        routeName = 'SellerItems'
        emit('close-mobile')
    }
    router.push({ name: routeName, params: params })
}

// ✅ RESET SHOP LOGIC: Collapses everything and goes to Home
const resetShop = () => {
    expandedPincodes.value = []
    expandedSocieties.value = []
    expandedCategories.value = []
    router.push({ name: 'Home' }) // ✅ Points to Home route
}

const syncStateWithRoute = () => {
    const p = route.params
    if (p.pincode) expandedPincodes.value = [p.pincode]
    else expandedPincodes.value = []

    if (p.society) expandedSocieties.value = [p.society]
    else expandedSocieties.value = []

    if (p.category) expandedCategories.value = [p.category]
    else expandedCategories.value = []
}

watch(() => route.params, syncStateWithRoute, { deep: true, immediate: true })

const fetchSidebarData = async () => {
    loading.value = true
    try {
        const res = await fetch('/api/method/doppio_demo.api.get_customer_sidebar_data')
        const data = await res.json()
        if (data.message && data.message.status === 'success') {
            treeData.value = data.message.data
            syncStateWithRoute()
        }
    } catch (e) { console.error(e) } finally { loading.value = false }
}

onMounted(() => fetchSidebarData())

const handleLogout = async () => {
    try { await fetch('/api/method/logout', { method: 'POST' }); session.isLoggedIn = false; window.location.href = '/login'; } catch (e) { window.location.href = '/login'; }
}
</script>