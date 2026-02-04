<template>
  <div class="h-full flex flex-col bg-gray-50 font-sans text-gray-900 selection:bg-orange-100">

    <header
      class="bg-white border-b border-gray-200 h-14 flex items-center justify-between px-4 sticky top-0 z-30 shadow-sm gap-4">

      <div class="flex items-center gap-2">
        <button @click="$emit('toggle-mobile')" class="lg:hidden p-1.5 hover:bg-gray-100 rounded text-gray-600">
          <span class="text-lg">☰</span>
        </button>
        <button v-if="viewMode !== 'default'" @click="goBack"
          class="flex items-center gap-1 px-2 py-1 hover:bg-gray-100 rounded text-gray-600 transition-colors">
          <span class="text-base">←</span> <span
            class="hidden sm:block text-[11px] font-bold uppercase tracking-wider">Back</span>
        </button>
      </div>

      <div class="flex-1 max-w-lg mx-auto">
        <div class="relative group">
          <input v-model="searchQuery" type="text" :placeholder="searchPlaceholder"
            class="w-full bg-gray-100 focus:bg-white border border-transparent focus:border-orange-500 focus:ring-2 focus:ring-orange-200 rounded-lg py-1.5 pl-9 pr-8 text-sm transition-all outline-none" />
          <span class="absolute left-3 top-2 text-gray-400 text-xs">🔍</span>
          <button v-if="searchQuery" @click="searchQuery = ''"
            class="absolute right-2 top-1.5 text-gray-400 hover:text-black text-sm">✕</button>
        </div>
      </div>

      <div class="flex items-center gap-3">
        <button @click="viewMode = 'cart'" class="relative p-2 hover:bg-orange-50 rounded transition-colors group">
          <span class="text-xl text-gray-600 group-hover:text-orange-600">🛒</span>
          <span v-if="cart.length"
            class="absolute top-0 right-0 bg-orange-600 text-white text-[9px] font-bold w-4 h-4 flex items-center justify-center rounded-full">{{
              cart.length }}</span>
        </button>
        <button v-if="viewMode !== 'list'" @click="viewMode = 'list'"
          class="hidden sm:block bg-gray-900 text-white px-3 py-1.5 rounded text-[11px] font-bold uppercase hover:bg-gray-800 transition-colors">
          Orders
        </button>
      </div>
    </header>

    <div class="flex-1 overflow-y-auto p-4 custom-scrollbar scroll-smooth">

      <div v-if="viewMode === 'default'" class="h-full flex flex-col items-center justify-center text-center">
        <div class="text-5xl opacity-20 grayscale mb-4">🏪</div>
        <h2 class="text-xl font-bold text-gray-700">Welcome to HyperMart</h2>
        <p class="text-sm text-gray-500 mt-1">Select a shop to start.</p>
        <button @click="$emit('toggle-mobile')"
          class="mt-6 lg:hidden bg-blue-600 text-white px-6 py-2 rounded-full text-sm font-bold shadow-lg">Browse
          Shops</button>
      </div>

      <div v-else-if="viewMode === 'seller_items'" class="max-w-[1400px] mx-auto">
        <div class="flex justify-between items-end mb-4 border-b border-gray-200 pb-2">
          <div>
            <h2 class="text-xl font-bold text-gray-900">{{ selectedSeller?.name }}</h2>
            <p class="text-xs text-gray-500">Verified Seller ✓</p>
          </div>
          <span class="text-[10px] font-bold bg-gray-100 px-2 py-1 rounded text-gray-600">{{ filteredItems.length }}
            ITEMS</span>
        </div>

        <div v-if="!filteredItems.length" class="text-center py-20 text-gray-400 font-medium">No items found.</div>

        <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-3 sm:gap-4">
          <div v-for="item in filteredItems" :key="item.item_code"
            class="bg-white rounded-lg border border-gray-200 hover:border-orange-400 hover:shadow-md transition-all flex flex-col overflow-hidden group">

            <div class="h-32 sm:h-40 p-3 flex items-center justify-center bg-white relative">
              <img v-if="item.image" :src="item.image"
                class="max-h-full max-w-full object-contain group-hover:scale-105 transition-transform duration-300" />
              <div v-else class="text-3xl opacity-10">📦</div>
            </div>

            <div class="p-3 flex flex-col flex-1 border-t border-gray-50">
              <h3 class="font-semibold text-gray-800 text-[13px] leading-snug line-clamp-2 h-9 mb-2"
                :title="item.item_name">
                <span v-html="highlightText(item.item_name)"></span>
              </h3>
              <div class="mt-auto flex items-center justify-between">
                <div class="flex flex-col">
                  <span class="text-base font-bold text-gray-900">₹{{ item.price }}</span>
                  <span class="text-[10px] text-gray-400 line-through">₹{{ Math.round(item.price * 1.1) }}</span>
                </div>
                <button @click="addToCart(item)"
                  class="bg-yellow-400 hover:bg-yellow-500 text-gray-900 px-3 py-1 rounded text-[11px] font-bold uppercase shadow-sm active:scale-95 transition-all">
                  Add
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-else-if="viewMode === 'cart'" class="max-w-4xl mx-auto">
        <div class="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
          <div class="px-4 py-3 border-b border-gray-100 bg-gray-50 flex justify-between items-center">
            <h2 class="font-bold text-gray-800 text-base">Shopping Cart</h2>
            <span class="text-xs text-gray-500 font-medium">{{ cart.length }} items</span>
          </div>

          <div v-if="!cart.length" class="p-10 text-center">
            <p class="text-gray-400 font-bold text-sm mb-4">Cart is empty</p>
            <button @click="goBack" class="text-blue-600 font-bold text-xs uppercase hover:underline">Start
              Shopping</button>
          </div>

          <div v-else>
            <div class="divide-y divide-gray-100">
              <div v-for="(item, i) in cart" :key="i" class="p-3 sm:p-4 flex gap-4 items-center">
                <div class="w-16 h-16 border rounded bg-white p-1 flex-shrink-0 flex items-center justify-center">
                  <img :src="item.image" class="max-w-full max-h-full object-contain" />
                </div>
                <div class="flex-1 min-w-0">
                  <p class="font-semibold text-sm text-gray-900 truncate">{{ item.item_name }}</p>
                  <p class="text-xs text-gray-500">₹{{ item.price }}</p>
                </div>
                <div class="flex items-center border rounded h-7 text-xs">
                  <button @click="updateQty(item, -1)" :disabled="item.qty <= 1"
                    class="px-2 hover:bg-gray-100 font-bold h-full disabled:opacity-30">-</button>
                  <span class="w-8 text-center font-bold bg-gray-50 h-full flex items-center justify-center border-x">{{
                    item.qty }}</span>
                  <button @click="updateQty(item, 1)" class="px-2 hover:bg-gray-100 font-bold h-full">+</button>
                </div>
                <div class="text-right min-w-[70px]">
                  <p class="font-bold text-sm text-gray-900">₹{{ item.price * item.qty }}</p>
                  <button @click="cart.splice(i, 1)"
                    class="text-[10px] text-red-500 font-bold hover:underline">REMOVE</button>
                </div>
              </div>
            </div>
            <div class="p-4 bg-gray-50 border-t border-gray-200 flex justify-between items-center">
              <div>
                <p class="text-[10px] font-bold text-gray-500 uppercase">Total</p>
                <p class="text-xl font-black text-gray-900">₹{{ cartTotal }}</p>
              </div>
              <button @click="placeOrder" :disabled="isPlacingOrder"
                class="bg-gray-900 text-white px-6 py-2 rounded-lg text-xs font-bold uppercase hover:bg-black disabled:opacity-50 shadow-md">
                {{ isPlacingOrder ? 'Processing...' : 'Place Order' }}
              </button>
            </div>
          </div>
        </div>
      </div>

      <div v-else-if="viewMode === 'list'" class="max-w-4xl mx-auto space-y-4">
        <h2 class="text-xl font-bold text-gray-800">Your Orders</h2>

        <div v-if="orders.loading" class="animate-pulse space-y-3">
          <div v-for="n in 2" :key="n" class="h-32 bg-gray-200 rounded-lg"></div>
        </div>

        <div v-else-if="!filteredOrders.length" class="text-center py-16 bg-white rounded-lg border border-dashed">
          <p class="text-gray-400 font-bold text-sm">No orders found.</p>
        </div>

        <div v-else class="space-y-4">
          <div v-for="order in filteredOrders" :key="order.name"
            class="bg-white rounded-lg border border-gray-200 overflow-hidden shadow-sm">
            <div class="bg-gray-50 px-4 py-2 flex justify-between items-center text-xs border-b">
              <div class="flex gap-4 sm:gap-8 text-gray-500">
                <div><span class="font-bold uppercase block text-[9px]">Date</span><span
                    class="font-bold text-gray-700">{{ order.transaction_date }}</span></div>
                <div><span class="font-bold uppercase block text-[9px]">Total</span><span
                    class="font-bold text-gray-700">₹{{ order.grand_total }}</span></div>
                <div class="hidden sm:block"><span class="font-bold uppercase block text-[9px]">ID</span><span
                    class="font-bold text-gray-700">#{{ order.name }}</span></div>
              </div>
              <span class="px-2 py-0.5 rounded text-[10px] font-bold uppercase border"
                :class="order.status === 'Completed' ? 'bg-green-50 text-green-700 border-green-200' : 'bg-orange-50 text-orange-700 border-orange-200'">{{
                order.status }}</span>
            </div>
            <div class="p-3 sm:p-4">
              <div v-for="item in order.items" :key="item.item_code" class="flex gap-3 mb-3 last:mb-0 items-center">
                <div class="w-12 h-12 border rounded bg-white p-1 flex-shrink-0 flex items-center justify-center">
                  <img v-if="item.image" :src="item.image" class="max-w-full max-h-full object-contain" />
                  <div v-else class="text-xl opacity-20">📦</div>
                </div>
                <div class="flex-1">
                  <h4 class="font-bold text-gray-900 text-xs sm:text-sm truncate w-full max-w-[200px] sm:max-w-md">{{
                    item.item_name }}</h4>
                  <p class="text-[11px] text-gray-500">Qty: {{ item.qty }} × ₹{{ item.rate }}</p>
                </div>
                <button @click="addToCart(item)"
                  class="text-[10px] font-bold border border-gray-300 bg-white px-2 py-1 rounded hover:bg-gray-50 transition-colors uppercase">
                  ↻ Buy Again
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
import { ref, watch, computed } from 'vue'
import { createResource } from 'frappe-ui'

const props = defineProps(['incomingAction'])
const emit = defineEmits(['toggle-mobile'])

const viewMode = ref('default')
const searchQuery = ref('')
const selectedSeller = ref(null)
const cart = ref([])
const isPlacingOrder = ref(false)

const goBack = () => { viewMode.value = viewMode.value === 'cart' ? (selectedSeller.value ? 'seller_items' : 'list') : 'default' }

watch(() => props.incomingAction, (newVal) => {
  if (newVal?.action === 'Show Seller Items') {
    viewMode.value = 'seller_items'
    selectedSeller.value = newVal.seller
    searchQuery.value = ''
  }
})

const searchPlaceholder = computed(() => viewMode.value === 'list' ? 'Search orders...' : 'Search products...')
const highlightText = (text) => searchQuery.value ? text.replace(new RegExp(`(${searchQuery.value})`, 'gi'), '<span class="bg-yellow-200">$1</span>') : text

const filteredItems = computed(() => {
  if (!selectedSeller.value) return []
  if (!searchQuery.value) return selectedSeller.value.items
  return selectedSeller.value.items.filter(i => i.item_name.toLowerCase().includes(searchQuery.value.toLowerCase()))
})

const orders = createResource({ url: 'doppio_demo.api.get_my_orders', auto: true })

const filteredOrders = computed(() => {
  if (!orders.data) return []
  if (!searchQuery.value) return orders.data
  const q = searchQuery.value.toLowerCase()
  return orders.data.filter(o => o.name.toLowerCase().includes(q) || o.items.some(i => i.item_name.toLowerCase().includes(q)))
})

const cartTotal = computed(() => cart.value.reduce((t, i) => t + (i.price * i.qty), 0))

const addToCart = (item) => {
  const existing = cart.value.find(i => i.item_code === item.item_code)
  if (existing) existing.qty++
  else cart.value.push({ ...item, qty: 1, price: item.price || item.rate })
  if (viewMode.value === 'list') alert("Item added to cart")
}

const updateQty = (item, change) => {
  const newQty = item.qty + change
  if (newQty >= 1) item.qty = newQty
}

const placeOrder = async () => {
  isPlacingOrder.value = true
  try {
    const res = await fetch('/api/method/doppio_demo.api.place_custom_order', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ cart_items: JSON.stringify(cart.value), seller_company: selectedSeller.value.name })
    })
    const data = await res.json()
    if (data.message.status === 'success') {
      alert("Order Placed Successfully!")
      cart.value = []
      orders.fetch()
      viewMode.value = 'list'
    } else alert("Error: " + data.message.message)
  } catch (e) { console.error(e) } finally { isPlacingOrder.value = false }
}
</script>