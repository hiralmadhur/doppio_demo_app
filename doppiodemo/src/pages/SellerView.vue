<template>
  <div class="flex h-screen bg-gray-50 overflow-hidden relative font-sans text-gray-900">
    
    <div v-if="isMobileSidebarOpen" @click="isMobileSidebarOpen = false" 
         class="fixed inset-0 bg-black/60 z-40 lg:hidden backdrop-blur-sm transition-opacity"></div>

    <div class="fixed lg:static inset-y-0 left-0 z-50 bg-white shadow-2xl lg:shadow-none transform transition-all duration-300 ease-in-out h-full border-r border-gray-200"
         :class="[isMobileSidebarOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0', 'w-64']">
         
         <SellerSidebar 
            :isCollapsed="false"
            :newOrderCount="pendingOrdersCount"
            @close-mobile="isMobileSidebarOpen = false"
            @logout="handleLogout"
         />
    </div>

    <div class="flex-1 flex flex-col min-w-0 h-full w-full relative">
      <header class="bg-white border-b border-gray-200 h-16 flex items-center justify-between px-6 sticky top-0 z-30 shadow-sm">
        <div class="flex items-center gap-3">
           <button @click="isMobileSidebarOpen = true" class="lg:hidden text-xl p-2">☰</button>
           <h1 class="font-bold text-gray-800 text-xl">{{ pageTitle }}</h1>
        </div>
        <div class="flex items-center gap-4">
             <span class="bg-orange-100 text-orange-800 text-xs px-2 py-1 rounded border border-orange-200 font-bold">
                 {{ session.sellerCompany || 'Store' }}
             </span>
        </div>
      </header>

      <div class="flex-1 overflow-y-auto p-4 sm:p-8 custom-scrollbar bg-gray-50/50">
        
        <div v-if="route.name === 'SellerDashboard'" class="grid grid-cols-1 md:grid-cols-2 gap-6">
           <div class="bg-white p-6 rounded-xl border border-gray-200 shadow-sm border-l-4 border-l-orange-500">
              <h3 class="text-gray-500 text-xs font-bold uppercase">Pending Orders</h3>
              <p class="text-4xl font-bold text-gray-900 mt-2">{{ pendingOrdersCount }}</p>
           </div>
           <div class="bg-white p-6 rounded-xl border border-gray-200 shadow-sm border-l-4 border-l-green-500">
              <h3 class="text-gray-500 text-xs font-bold uppercase">Today's Sales</h3>
              <p class="text-4xl font-bold text-green-600 mt-2">₹{{ todaySales }}</p>
           </div>
        </div>

        <div v-else-if="route.name === 'SellerOrders'" class="space-y-4 max-w-5xl mx-auto">
            <div v-if="!ordersList.length" class="text-center py-10 text-gray-500">No orders found.</div>
            
            <div v-else v-for="order in ordersList" :key="order.name" class="bg-white p-4 rounded-xl border border-gray-200 shadow-sm">
                <div class="flex justify-between items-center mb-2">
                    <span class="font-bold">#{{ order.name }}</span>
                    <span :class="getStatusClass(order.status)" class="text-xs px-2 py-1 rounded font-bold border uppercase">{{ order.status }}</span>
                </div>
                <div class="text-sm text-gray-600 mb-2">Customer: {{ order.customer_name }} | Total: ₹{{ order.grand_total }}</div>
                
                <div class="bg-gray-50 p-2 rounded mb-3 text-sm">
                    <div v-for="item in order.items" :key="item.item_code" class="flex justify-between">
                        <span>{{ item.qty }}x {{ item.item_name }}</span><span>₹{{ item.amount }}</span>
                    </div>
                </div>

                <div class="flex gap-2 justify-end">
                    <button v-if="['Pending', 'Draft'].includes(order.status)" @click="updateStatus(order.name, 'Processing')" class="bg-blue-600 text-white px-3 py-1 rounded text-xs">Accept</button>
                    <button v-if="order.status === 'Processing'" @click="updateStatus(order.name, 'Completed')" class="bg-green-600 text-white px-3 py-1 rounded text-xs">Deliver</button>
                </div>
            </div>
        </div>

        <div v-else-if="route.name === 'SellerProducts'" class="text-center py-20 text-gray-500">
            🚧 Inventory Management Coming Soon
        </div>

      </div>
    </div>
    <Toast ref="toastRef" />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import { createResource } from 'frappe-ui'
import { session } from '../data/session'
import SellerSidebar from '../components/SellerSidebar.vue' // ✅
import Toast from '../components/Toast.vue'

const route = useRoute()
const isMobileSidebarOpen = ref(false)
const toastRef = ref(null)

const sellerOrders = createResource({ url: 'doppio_demo.api.get_seller_orders', auto: true })
const ordersList = computed(() => sellerOrders.data || [])
const pendingOrdersCount = computed(() => ordersList.value.filter(o => ['Pending', 'Draft'].includes(o.status)).length)
const todaySales = computed(() => {
    const today = new Date().toISOString().split('T')[0]
    return ordersList.value.filter(o => o.transaction_date === today && o.status !== 'Cancelled').reduce((sum, order) => sum + order.grand_total, 0)
})
const pageTitle = computed(() => route.name === 'SellerOrders' ? 'Manage Orders' : 'Seller Dashboard')

const updateStatus = async (orderId, newStatus) => {
    try {
        const res = await fetch('/api/method/doppio_demo.api.update_order_status', {
            method: 'POST', headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ order_name: orderId, status: newStatus })
        })
        const data = await res.json()
        if (data.message.status === 'success') {
            toastRef.value.add('Status Updated', 'success')
            sellerOrders.fetch()
        }
    } catch(e) { toastRef.value.add('Error', 'error') }
}

const getStatusClass = (status) => {
    if (['Pending', 'Draft'].includes(status)) return 'bg-yellow-100 text-yellow-800'
    if (status === 'Completed') return 'bg-green-100 text-green-800'
    return 'bg-gray-100'
}

const handleLogout = async () => {
    try { await fetch('/api/method/logout', { method: 'POST' }); session.isLoggedIn = false; window.location.href = '/login'; } catch (e) { window.location.href = '/login' }
}
</script>