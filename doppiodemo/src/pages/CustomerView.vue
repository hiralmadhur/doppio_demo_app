<template>
  <div class="flex h-screen bg-gray-50 overflow-hidden relative font-sans text-gray-900 selection:bg-orange-100">
    
    <Toast ref="toastRef" />
    <ConfirmDialog ref="confirmRef" />

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
        
        <header class="bg-white border-b border-gray-200 h-14 flex items-center justify-between px-4 sticky top-0 z-30 shadow-sm gap-2 sm:gap-4">
            
            <div class="flex items-center gap-2">
                <button @click="isMobileSidebarOpen = !isMobileSidebarOpen"
                    class="lg:hidden p-2 hover:bg-gray-100 rounded-md text-gray-600 transition-colors active:bg-gray-200">
                    <span class="text-xl">☰</span>
                </button>
                <button v-if="canGoBack" @click="goBack"
                    class="flex items-center gap-1 px-2 py-1 hover:bg-gray-100 rounded text-gray-600 transition-colors group">
                    <span class="text-base group-hover:-translate-x-0.5 transition-transform">←</span>
                    <span class="hidden sm:block text-[11px] font-bold uppercase tracking-wider">Back</span>
                </button>
            </div>

            <div class="flex-1 max-w-lg mx-auto transition-all duration-300"
                :class="showSearch ? 'opacity-100' : 'opacity-0 pointer-events-none'">
                <div class="relative group">
                    <input v-model="searchQuery" type="text" :placeholder="searchPlaceholder"
                        class="w-full bg-gray-100 focus:bg-white border border-transparent focus:border-orange-500 focus:ring-2 focus:ring-orange-200 rounded-lg py-1.5 pl-9 pr-8 text-sm transition-all outline-none shadow-sm" />
                    <span class="absolute left-3 top-2 text-gray-400 text-xs">🔍</span>
                    <button v-if="searchQuery" @click="searchQuery = ''"
                        class="absolute right-2 top-1.5 text-gray-400 hover:text-black text-sm">✕</button>
                </div>
            </div>

            <div class="flex items-center gap-1 sm:gap-3">
                <button @click="router.push({ name: 'Home' })"
                    class="p-2 hover:bg-gray-100 rounded-full transition-colors group relative" title="Go to Home">
                    <span class="text-lg sm:text-xl text-gray-500 group-hover:text-blue-600 transition-colors">🏠</span>
                </button>

                <button @click="router.push({ name: 'Cart' })"
                    class="relative p-2 hover:bg-orange-50 rounded-full transition-colors group"
                    :class="{ 'bg-orange-50 text-orange-600': currentView === 'Cart' }">
                    <span class="text-xl text-gray-600 group-hover:text-orange-600 transition-colors">🛒</span>
                    <span v-if="cart.length"
                        class="absolute top-0 right-0 bg-orange-600 text-white text-[9px] font-bold w-4 h-4 flex items-center justify-center rounded-full border-2 border-white shadow-sm animate-bounce-short">
                        {{ cart.length }}
                    </span>
                </button>

                <button v-if="currentView !== 'Orders'" @click="router.push({ name: 'Orders' })"
                    class="hidden sm:block bg-gray-900 text-white px-3 py-1.5 rounded text-[11px] font-bold uppercase hover:bg-gray-800 transition-colors shadow-sm active:scale-95">
                    My Orders
                </button>
                <button v-if="currentView !== 'Orders'" @click="router.push({ name: 'Orders' })"
                    class="sm:hidden p-2 text-gray-600 hover:text-orange-600 transition-colors">
                    📜
                </button>
            </div>
        </header>

        <div class="flex-1 overflow-y-auto p-4 sm:p-6 custom-scrollbar scroll-smooth relative">

            <div v-if="currentView === 'Home'" class="h-full flex flex-col items-center pt-4 sm:pt-8 animate-fade-in">
                <div class="max-w-5xl w-full">
                    <div class="bg-white rounded-2xl p-6 sm:p-10 shadow-sm border border-gray-100 mb-6 sm:mb-10 flex flex-col md:flex-row items-center justify-between text-center md:text-left relative overflow-hidden group">
                        <div class="z-10 max-w-xl w-full">
                            <h1 class="text-2xl sm:text-3xl lg:text-4xl font-extrabold text-gray-900 mb-3 leading-tight">
                                Welcome back, <br class="hidden sm:block" />
                                <span class="text-transparent bg-clip-text bg-gradient-to-r from-orange-600 to-yellow-500">{{ getUserName() }}</span>! 👋
                            </h1>
                            <p class="text-gray-500 text-sm sm:text-lg mb-6 sm:mb-8 font-medium">
                                Ready to order something fresh? <br class="sm:hidden"> Select your location to start.
                            </p>
                            <button @click="handleBrowseClick"
                                class="w-full md:w-auto bg-gray-900 hover:bg-black text-white px-8 py-3.5 rounded-xl text-sm font-bold uppercase tracking-wide shadow-lg shadow-gray-200 transition-all active:scale-95 flex items-center justify-center gap-2">
                                <span>Start Shopping</span> <span class="text-lg">➔</span>
                            </button>
                        </div>
                        <div class="text-[100px] sm:text-[140px] md:text-[180px] opacity-5 md:opacity-10 absolute -right-6 -bottom-8 sm:-right-10 sm:-bottom-10 rotate-12 select-none pointer-events-none transition-transform group-hover:rotate-6 group-hover:scale-110 duration-700">
                            🛒
                        </div>
                    </div>

                    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
                        <div @click="handleBrowseClick" class="bg-white p-5 sm:p-6 rounded-xl border border-gray-100 shadow-sm hover:shadow-lg hover:border-blue-100 transition-all cursor-pointer group active:scale-95">
                            <div class="flex items-center gap-4">
                                <div class="w-12 h-12 bg-blue-50 rounded-xl flex items-center justify-center text-2xl group-hover:scale-110 transition-transform duration-300">🏪</div>
                                <div class="text-left">
                                    <h3 class="font-bold text-gray-800 text-sm sm:text-base">Browse Shops</h3>
                                    <p class="text-[11px] sm:text-xs text-gray-500 mt-0.5">Explore sellers near you</p>
                                </div>
                            </div>
                        </div>
                        <div @click="router.push({ name: 'Orders' })" class="bg-white p-5 sm:p-6 rounded-xl border border-gray-100 shadow-sm hover:shadow-lg hover:border-orange-100 transition-all cursor-pointer group active:scale-95">
                            <div class="flex items-center gap-4">
                                <div class="w-12 h-12 bg-orange-50 rounded-xl flex items-center justify-center text-2xl group-hover:scale-110 transition-transform duration-300">📦</div>
                                <div class="text-left">
                                    <h3 class="font-bold text-gray-800 text-sm sm:text-base">My Orders</h3>
                                    <p class="text-[11px] sm:text-xs text-gray-500 mt-0.5">Track active & past orders</p>
                                </div>
                            </div>
                        </div>
                        <div class="bg-white p-5 sm:p-6 rounded-xl border border-gray-100 shadow-sm hover:shadow-lg hover:border-green-100 transition-all cursor-default group">
                            <div class="flex items-center gap-4">
                                <div class="w-12 h-12 bg-green-50 rounded-xl flex items-center justify-center text-2xl group-hover:rotate-12 transition-transform duration-300">🎧</div>
                                <div class="text-left">
                                    <h3 class="font-bold text-gray-800 text-sm sm:text-base">Support</h3>
                                    <p class="text-[11px] sm:text-xs text-gray-500 mt-0.5">Contact us for help</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div v-else-if="currentView === 'Orders'" class="max-w-4xl mx-auto space-y-5 animate-fade-in pb-10">
                <h2 class="text-xl sm:text-2xl font-bold text-gray-800 flex items-center gap-2"><span>📦</span> My Orders</h2>
                <div v-if="orders.loading" class="space-y-4">
                    <div v-for="n in 3" :key="n" class="h-40 bg-white rounded-xl border border-gray-200 animate-pulse"></div>
                </div>
                <div v-else-if="!filteredOrders.length" class="text-center py-20 bg-white rounded-xl border border-dashed border-gray-300">
                    <div class="text-5xl mb-4 grayscale opacity-20">📜</div>
                    <p class="text-gray-400 font-bold text-sm">No orders found.</p>
                    <button @click="router.push({ name: 'Home' })" class="mt-4 text-blue-600 font-bold text-xs uppercase hover:underline">Start Shopping</button>
                </div>
                <div v-else class="space-y-6">
                    <div v-for="order in filteredOrders" :key="order.name" class="bg-white rounded-xl border border-gray-200 overflow-hidden shadow-sm hover:shadow-md transition-shadow relative group">
                        <div class="bg-gray-50 px-4 sm:px-5 py-3 border-b border-gray-100">
                            <div class="flex flex-col sm:flex-row sm:justify-between sm:items-center gap-3">
                                <div class="flex justify-between items-center w-full sm:w-auto sm:gap-6">
                                    <div class="flex flex-col sm:block">
                                        <span class="text-[10px] font-bold uppercase text-gray-400 block">Order ID</span>
                                        <span class="font-mono text-xs sm:text-sm font-bold text-gray-900">#{{ order.name }}</span>
                                    </div>
                                    <span class="sm:hidden px-2 py-1 rounded text-[10px] font-bold uppercase border" :class="getStatusClass(order)">{{ order.status }}</span>
                                </div>
                                <div class="flex justify-between sm:justify-start gap-6 text-gray-600 w-full sm:w-auto">
                                    <div><span class="block text-[10px] font-bold uppercase text-gray-400">Placed On</span><span class="text-xs sm:text-sm font-bold text-gray-800">{{ order.transaction_date }}</span></div>
                                    <div><span class="block text-[10px] font-bold uppercase text-gray-400">Total</span><span class="text-xs sm:text-sm font-bold text-gray-800">₹{{ order.grand_total }}</span></div>
                                </div>
                                <span class="hidden sm:block px-2.5 py-1 rounded-full text-[10px] font-bold uppercase border" :class="getStatusClass(order)">{{ order.status }}</span>
                            </div>
                        </div>
                        <div class="p-4 sm:p-5 grid gap-4 relative">
                            <div v-if="order.status === 'Cancelled' || order.docstatus === 2" class="absolute inset-0 bg-white/40 z-10 pointer-events-none"></div>
                            <div v-for="item in order.items" :key="item.item_code" class="flex gap-3 sm:gap-4 items-center z-0 relative">
                                <div class="w-12 h-12 border rounded bg-white p-1 flex-shrink-0 flex items-center justify-center">
                                    <img v-if="item.image" :src="item.image" class="max-w-full max-h-full object-contain" />
                                    <div v-else class="text-lg opacity-20">📦</div>
                                </div>
                                <div class="flex-1 min-w-0">
                                    <p class="text-xs sm:text-sm font-bold text-gray-900 truncate">{{ item.item_name }}</p>
                                    <p class="text-[11px] text-gray-500">Qty: {{ item.qty }} × ₹{{ item.rate }}</p>
                                </div>
                                <button @click="buyAgain(item, order.company)" class="text-[10px] font-bold text-blue-600 bg-blue-50 px-3 py-1.5 rounded hover:bg-blue-100 transition-colors uppercase whitespace-nowrap border border-blue-100 active:scale-95">↻ Buy Again</button>
                            </div>
                        </div>
                        <div class="bg-gray-50/50 px-4 sm:px-5 py-3 border-t border-gray-100 flex justify-end gap-3">
                            <button v-if="order.status !== 'Cancelled' && order.docstatus !== 2 && order.status !== 'Completed'" @click="handleCancelOrder(order.name)" class="text-[11px] font-bold text-red-500 bg-white hover:bg-red-50 border border-red-200 hover:border-red-500 px-4 sm:px-6 py-2 rounded shadow-sm uppercase flex items-center gap-1 transition-all active:scale-95"><span>✕</span> Cancel</button>
                            <button v-if="order.status === 'Cancelled' || order.docstatus === 2" @click="handleDeleteOrder(order.name)" class="text-[11px] font-bold text-white bg-red-600 hover:bg-red-700 border border-red-600 px-4 sm:px-6 py-2 rounded shadow-sm uppercase flex items-center gap-1 transition-all active:scale-95"><span>🗑</span> Delete</button>
                        </div>
                    </div>
                </div>
            </div>

            <div v-else-if="isNavigatingTree" class="h-full flex flex-col items-center justify-center text-center animate-fade-in px-4">
                <div class="bg-white p-6 sm:p-8 rounded-2xl shadow-sm border border-gray-100 max-w-md w-full">
                    <h2 class="text-xl font-bold text-gray-800 mb-2">Browsing {{ activeContext }}</h2>
                    <p class="text-sm text-gray-500 mb-6 font-medium text-orange-600">{{ nextInstruction }}</p>
                    <div class="flex flex-wrap items-center justify-center gap-2 text-xs text-gray-400 font-mono bg-gray-50 p-2 rounded border border-gray-100">
                        <span :class="{ 'text-gray-900 font-bold': route.params.pincode }">Pin</span> ›
                        <span :class="{ 'text-gray-900 font-bold': route.params.society }">Soc</span> ›
                        <span :class="{ 'text-gray-900 font-bold': route.params.category }">Cat</span>
                    </div>
                </div>
            </div>

            <div v-else-if="currentView === 'SellerItems'" class="max-w-[1400px] mx-auto animate-fade-in">
                <div v-if="loadingItems" class="flex flex-col items-center justify-center h-64">
                    <div class="w-8 h-8 border-4 border-orange-500 border-t-transparent rounded-full animate-spin mb-4"></div>
                    <p class="text-sm text-gray-500 font-medium">Loading products...</p>
                </div>
                <div v-else>
                    <div class="flex justify-between items-end mb-4 border-b border-gray-200 pb-3 sticky top-0 bg-gray-50 z-10 pt-2">
                        <div>
                            <h2 class="text-lg sm:text-xl font-bold text-gray-900 leading-tight">{{ route.params.sellerName }}</h2>
                            <div class="flex flex-wrap items-center gap-2 text-[10px] text-gray-500 mt-1">
                                <span class="bg-white border px-1.5 rounded">{{ route.params.society }}</span><span class="text-gray-300">•</span>
                                <span class="bg-white border px-1.5 rounded">{{ route.params.category }}</span>
                            </div>
                        </div>
                        <span class="text-[10px] font-bold bg-gray-200 text-gray-700 px-2 py-1 rounded shadow-sm">{{ filteredItems.length }} ITEMS</span>
                    </div>
                    <div v-if="!filteredItems.length" class="text-center py-20 bg-white rounded-xl border border-dashed border-gray-300">
                        <div class="text-4xl grayscale opacity-30 mb-2">📦</div>
                        <p class="text-gray-400 font-bold text-sm">No items found in this category.</p>
                    </div>
                    <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-3 sm:gap-4 pb-20">
                        <div v-for="item in filteredItems" :key="item.item_code" class="bg-white rounded-lg border border-gray-200 hover:border-orange-400 hover:shadow-lg hover:-translate-y-1 transition-all duration-300 flex flex-col overflow-hidden group">
                            <div class="h-32 sm:h-40 p-4 flex items-center justify-center bg-white relative">
                                <img v-if="item.image" :src="item.image" loading="lazy" class="max-h-full max-w-full object-contain group-hover:scale-105 transition-transform duration-300" />
                                <div v-else class="text-4xl opacity-10 grayscale">📦</div>
                            </div>
                            <div class="p-3 flex flex-col flex-1 border-t border-gray-50 bg-gray-50/30">
                                <h3 class="font-semibold text-gray-800 text-[13px] leading-snug line-clamp-2 h-9 mb-2" :title="item.item_name"><span v-html="highlightText(item.item_name)"></span></h3>
                                <div class="mt-auto flex items-center justify-between">
                                    <div class="flex flex-col"><span class="text-base font-bold text-gray-900">₹{{ item.price }}</span><span class="text-[10px] text-gray-400 line-through">₹{{ Math.round(item.price * 1.1) }}</span></div>
                                    <button @click="addToCart(item)" class="bg-yellow-400 hover:bg-yellow-500 text-gray-900 px-3 py-1.5 rounded-md text-[11px] font-bold uppercase shadow-sm active:scale-95 transition-all">Add</button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div v-else-if="currentView === 'Cart'" class="max-w-3xl mx-auto animate-fade-in pb-10">
                <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
                    <div class="px-5 py-4 border-b border-gray-100 bg-gray-50 flex justify-between items-center">
                        <h2 class="font-bold text-gray-800 text-lg">Shopping Cart</h2>
                        <span class="text-xs text-gray-500 font-medium bg-white px-2 py-1 rounded border">{{ cart.length }} items</span>
                    </div>
                    <div v-if="!cart.length" class="p-10 sm:p-16 text-center">
                        <div class="text-6xl mb-4 grayscale opacity-20">🛒</div>
                        <p class="text-gray-400 font-bold text-sm mb-6">Your cart is empty.</p>
                        <button @click="router.push({ name: 'Home' })" class="bg-gray-900 text-white px-6 py-2 rounded-lg text-xs font-bold uppercase hover:bg-black shadow-md transition-transform active:scale-95">Start Shopping</button>
                    </div>
                    <div v-else>
                        <div class="divide-y divide-gray-100 max-h-[60vh] overflow-y-auto custom-scrollbar">
                            <div v-for="(item, i) in cart" :key="i" class="p-3 sm:p-4 flex gap-3 sm:gap-4 items-center hover:bg-gray-50 transition-colors">
                                <div class="w-14 h-14 sm:w-16 sm:h-16 border rounded-lg bg-white p-1 flex-shrink-0 flex items-center justify-center">
                                    <img v-if="item.image" :src="item.image" class="max-w-full max-h-full object-contain" />
                                    <div v-else class="text-xl opacity-20">📦</div>
                                </div>
                                <div class="flex-1 min-w-0">
                                    <p class="font-bold text-sm text-gray-900 truncate">{{ item.item_name }}</p>
                                    <p class="text-xs text-gray-500 flex items-center gap-1"><span>🏪</span> {{ item.seller_name }}</p>
                                    <p class="text-xs text-gray-500 mt-0.5">₹{{ item.price }} / unit</p>
                                </div>
                                <div class="flex items-center border border-gray-200 rounded-lg h-8 text-xs bg-white shadow-sm">
                                    <button @click="updateQty(item, -1)" :disabled="item.qty <= 1" class="px-2 hover:bg-gray-100 font-bold h-full disabled:opacity-30 text-gray-600 transition-colors">-</button>
                                    <span class="w-7 text-center font-bold bg-gray-50 h-full flex items-center justify-center border-x border-gray-200">{{ item.qty }}</span>
                                    <button @click="updateQty(item, 1)" class="px-2 hover:bg-gray-100 font-bold h-full text-gray-600 transition-colors">+</button>
                                </div>
                                <div class="text-right min-w-[70px] sm:min-w-[80px]">
                                    <p class="font-bold text-sm text-gray-900">₹{{ (item.price * item.qty).toFixed(2) }}</p>
                                    <button @click="removeFromCart(i)" class="text-[10px] text-red-500 font-bold hover:text-red-700 hover:underline mt-1">REMOVE</button>
                                </div>
                            </div>
                        </div>
                        <div class="p-5 bg-gray-50 border-t border-gray-200 flex justify-between items-center shadow-[0_-4px_6px_-1px_rgba(0,0,0,0.05)]">
                            <div>
                                <p class="text-[10px] font-bold text-gray-500 uppercase tracking-wider">Grand Total</p>
                                <p class="text-2xl font-black text-gray-900">₹{{ cartTotal }}</p>
                            </div>
                            <button @click="placeOrder" :disabled="isPlacingOrder" class="bg-gray-900 text-white px-6 sm:px-8 py-3 rounded-xl text-xs sm:text-sm font-bold uppercase hover:bg-black disabled:opacity-50 disabled:cursor-not-allowed shadow-lg flex items-center gap-2 transition-all active:scale-95">
                                <span v-if="isPlacingOrder" class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
                                {{ isPlacingOrder ? 'Processing...' : 'Place Order' }}
                            </button>
                        </div>
                    </div>
                </div>
            </div>

        </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, computed, onMounted, onUnmounted } from 'vue'
import { createResource } from 'frappe-ui'
import { useRoute, useRouter } from 'vue-router'
import { session } from '../data/session'
import Toast from '../components/Toast.vue'
import ConfirmDialog from '../components/ConfirmDialog.vue'
import MarketSidebar from '../components/MarketSidebar.vue' // ✅ Customer Specific Sidebar

const router = useRouter()
const route = useRoute()
const toastRef = ref(null)
const confirmRef = ref(null)

const isMobileSidebarOpen = ref(false)
const isDesktopCollapsed = ref(false)
const isMobile = ref(false)

const getUserName = () => session.user ? session.user.split('@')[0] : 'User'

// --- SIDEBAR HANDLING ---
const handleSelection = (data) => {
    if (data.action === 'Show Seller Items') {
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

const handleBrowseClick = () => {
  if (isMobile.value) {
    isMobileSidebarOpen.value = true
  } else {
    // If desktop and sidebar is collapsed, open it.
    // If open, just toast to guide user.
    if(isDesktopCollapsed.value) {
        isDesktopCollapsed.value = false;
    }
    toastRef.value?.add('👈 Please select a Pincode from the sidebar.', 'info')
  }
}

// --- VIEW STATE LOGIC ---
const currentView = computed(() => {
  if (route.name === 'Cart') return 'Cart'
  if (route.name === 'Orders') return 'Orders'
  if (route.name === 'SellerItems') return 'SellerItems'
  if (['ShopPincode', 'ShopSociety', 'ShopCategory'].includes(route.name)) return 'Navigating'
  return 'Home'
})

const isNavigatingTree = computed(() => currentView.value === 'Navigating')
const canGoBack = computed(() => currentView.value !== 'Home')
const showSearch = computed(() => ['SellerItems', 'Orders'].includes(currentView.value))

const activeContext = computed(() => {
  if (route.params.category) return route.params.category
  if (route.params.society) return route.params.society
  if (route.params.pincode) return `Pincode ${route.params.pincode}`
  return ''
})

const nextInstruction = computed(() => {
  if (route.params.category) return "Select a Shop (Seller) from the sidebar."
  if (route.params.society) return "Select a Category (e.g., Grocery) from the sidebar."
  if (route.params.pincode) return "Select your Society from the sidebar."
  return ""
})

const goBack = () => router.back()

// --- DATA LOGIC ---
const searchQuery = ref('')
const cart = ref([])
const isPlacingOrder = ref(false)
const sellerItems = ref([])
const loadingItems = ref(false)

onMounted(() => {
  checkScreen()
  window.addEventListener('resize', checkScreen)
  try {
    const savedCart = localStorage.getItem('my_cart')
    if (savedCart) cart.value = JSON.parse(savedCart)
  } catch (e) { console.error("Cart Load Error", e) }
})

onUnmounted(() => window.removeEventListener('resize', checkScreen))

const saveCart = () => {
  localStorage.setItem('my_cart', JSON.stringify(cart.value))
}

const searchPlaceholder = computed(() => currentView.value === 'Orders' ? 'Search past orders...' : 'Search products...')
const highlightText = (text) => searchQuery.value ? text.replace(new RegExp(`(${searchQuery.value})`, 'gi'), '<span class="bg-yellow-200">$1</span>') : text

const fetchSellerItems = async (sellerName) => {
  if (!sellerName) return
  loadingItems.value = true
  sellerItems.value = []
  try {
    const res = await fetch('/api/method/doppio_demo.api.get_customer_sidebar_data')
    const data = await res.json()
    if (data.message && data.message.status === 'success') {
      let foundItems = []
      const targetPin = route.params.pincode;
      const targetSoc = route.params.society;
      const targetCat = route.params.category;

      const pinObj = data.message.data.find(p => p.pincode === targetPin);
      if (pinObj) {
        const socObj = pinObj.societies.find(s => s.name === targetSoc);
        if (socObj) {
          const catObj = socObj.categories.find(c => c.name === targetCat);
          if (catObj) {
            const sellerObj = catObj.sellers.find(sel => sel.name === sellerName);
            if (sellerObj) {
              foundItems = sellerObj.items;
            }
          }
        }
      }
      sellerItems.value = foundItems
    }
  } catch (e) { console.error("Fetch Items Error", e) }
  finally { loadingItems.value = false }
}

watch(() => route.params.sellerName, (newSeller) => {
  if (newSeller) {
    searchQuery.value = ''
    fetchSellerItems(newSeller)
  }
}, { immediate: true })

const filteredItems = computed(() => {
  if (!sellerItems.value.length) return []
  if (!searchQuery.value) return sellerItems.value
  return sellerItems.value.filter(i => i.item_name.toLowerCase().includes(searchQuery.value.toLowerCase()))
})

const orders = createResource({ url: 'doppio_demo.api.get_my_orders', auto: true })

const filteredOrders = computed(() => {
  if (!orders.data) return []
  if (!searchQuery.value) return orders.data
  const q = searchQuery.value.toLowerCase()
  return orders.data.filter(o => o.name.toLowerCase().includes(q) || o.items.some(i => i.item_name.toLowerCase().includes(q)))
})

const cartTotal = computed(() => cart.value.reduce((t, i) => t + (i.price * i.qty), 0))

// --- ACTIONS ---
const addToCart = async (item) => {
  const seller = route.params.sellerName || item.seller_name || 'Unknown'
  if (cart.value.length > 0 && cart.value[0].seller_name !== seller && route.params.sellerName) {
    if (!await confirmRef.value.open('Clear Cart?', `Your cart has items from ${cart.value[0].seller_name}. Clear it to add from ${seller}?`)) return;
    cart.value = []
  }
  const existing = cart.value.find(i => i.item_code === item.item_code)
  if (existing) { existing.qty++ } else { cart.value.push({ ...item, qty: 1, price: item.price || item.rate, seller_name: seller }) }
  saveCart()
  if (currentView.value === 'Orders') toastRef.value?.add('Item added to cart', 'success')
  else if (currentView.value === 'SellerItems') toastRef.value?.add('Added to cart', 'success')
}

const buyAgain = async (item, orderCompany) => {
  const seller = orderCompany || item.seller_name || 'Unknown'
  if (cart.value.length > 0 && cart.value[0].seller_name !== seller && cart.value[0].seller_name !== 'Unknown') {
    if (!await confirmRef.value.open('Clear Cart?', `Cart has items from ${cart.value[0].seller_name}. Clear to add ${item.item_name}?`)) return;
    cart.value = []
  }
  const existing = cart.value.find(i => i.item_code === item.item_code)
  if (existing) { existing.qty++ } else { cart.value.push({ ...item, qty: 1, price: item.price || item.rate, seller_name: seller, image: item.image }) }
  saveCart()
  toastRef.value?.add('Item added to cart! Proceed to checkout.', 'success')
}

const updateQty = (item, change) => {
  const newQty = item.qty + change
  if (newQty >= 1) item.qty = newQty
  saveCart()
}

const removeFromCart = (index) => {
  cart.value.splice(index, 1)
  saveCart()
  toastRef.value?.add('Item removed from cart', 'success')
}

const placeOrder = async () => {
  if (!cart.value.length) return;
  isPlacingOrder.value = true
  const sellerName = cart.value[0].seller_name
  try {
    const res = await fetch('/api/method/doppio_demo.api.place_custom_order', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ cart_items: JSON.stringify(cart.value), seller_company: sellerName })
    })
    const data = await res.json()
    if (data.message && data.message.status === 'success') {
      toastRef.value?.add('Order Placed Successfully! 🎉', 'success')
      cart.value = []
      saveCart()
      orders.fetch()
      router.push({ name: 'Orders' })
    } else { throw new Error(data.message?.message || "Unknown Error") }
  } catch (e) { toastRef.value?.add("Failed to place order: " + e.message, 'error') }
  finally { isPlacingOrder.value = false }
}

const handleCancelOrder = async (orderName) => {
  if (!await confirmRef.value.open('Cancel Order?', `Are you sure you want to cancel Order #${orderName}?`)) return;
  try {
    const res = await fetch('/api/method/doppio_demo.api.cancel_custom_order', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ order_name: orderName })
    })
    const data = await res.json()
    if (data.message && data.message.status === 'success') {
      toastRef.value?.add('Order Cancelled Successfully', 'success')
      orders.fetch()
    } else { toastRef.value?.add("Error: " + (data.message?.message || "Could not cancel"), 'error') }
  } catch (e) { console.error(e); toastRef.value?.add("Network Error", 'error') }
}

const handleDeleteOrder = async (orderName) => {
  if (!await confirmRef.value.open('Delete Order?', `Permanently delete Order #${orderName}? This cannot be undone.`)) return;
  try {
    const res = await fetch('/api/method/doppio_demo.api.delete_custom_order', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ order_name: orderName })
    })
    const data = await res.json()
    if (data.message && data.message.status === 'success') {
      toastRef.value?.add('Order Deleted Successfully', 'success')
      orders.fetch()
    } else { toastRef.value?.add("Error: " + (data.message?.message || "Could not delete"), 'error') }
  } catch (e) { console.error(e); toastRef.value?.add("Network Error", 'error') }
}

const getStatusClass = (order) => {
  if (order.status === 'Cancelled' || order.docstatus === 2) return 'bg-red-50 text-red-600 border-red-200'
  if (order.status === 'Completed') return 'bg-green-50 text-green-700 border-green-200'
  return 'bg-orange-50 text-orange-700 border-orange-200'
}
</script>

<style scoped>
@keyframes bounce-x { 0%, 100% { transform: translateX(-25%); } 50% { transform: translateX(0); } }
.animate-bounce-x { animation: bounce-x 1s infinite; }
.animate-fade-in { animation: fadeIn 0.4s ease-out; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
</style>