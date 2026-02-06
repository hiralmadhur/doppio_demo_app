<template>
  <div class="flex h-screen bg-gray-50 font-sans text-gray-900">
    <Toast ref="toastRef" />
    <ConfirmDialog ref="confirmRef" />

    <div v-if="isMobileSidebarOpen" @click="isMobileSidebarOpen = false" class="fixed inset-0 bg-black/60 z-40 lg:hidden backdrop-blur-sm transition-opacity"></div>

    <div class="fixed lg:static inset-y-0 left-0 z-20 shadow-xl transform transition-all duration-300 ease-in-out h-full w-72 shrink-0 bg-white"
         :class="isMobileSidebarOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'">
         <SellerSidebar :isCollapsed="false" @close-mobile="isMobileSidebarOpen = false" @filter-orders="handleCustomerFilter" @reset-filter="handleResetFilter"/>
    </div>

    <div class="flex-1 flex flex-col h-full overflow-hidden relative w-full">
        <header class="bg-white h-16 border-b border-gray-200 flex items-center justify-between px-6 shadow-sm z-10">
            <div class="flex items-center gap-3">
                <button @click="isMobileSidebarOpen = !isMobileSidebarOpen" class="lg:hidden text-gray-600 text-xl">☰</button>
                <h1 class="text-xl font-bold text-gray-800">{{ pageTitle }}</h1>
            </div>
            <button @click="handleLogout" class="px-3 py-1.5 rounded text-xs font-bold text-red-600 bg-red-50 hover:bg-red-600 hover:text-white border border-red-100 transition-all">Logout</button>
        </header>

        <div class="flex-1 overflow-y-auto p-4 sm:p-8 custom-scrollbar bg-gray-50/50">
            
            <div v-if="activeCustomerFilter" class="mb-4 flex justify-between items-center bg-orange-50 border border-orange-200 p-3 rounded-lg">
                <span class="text-orange-800 text-sm font-bold flex gap-2"><span>👤</span> Showing orders for: <span class="uppercase">{{ activeCustomerFilter }}</span></span>
                <button @click="handleResetFilter" class="text-xs font-bold text-orange-600 hover:underline">Clear</button>
            </div>

            <div class="space-y-4">
                <div v-if="sellerOrders.loading" class="text-center py-10"><p class="text-gray-400 text-xs font-bold uppercase">Syncing...</p></div>
                <div v-else-if="!ordersList.length" class="text-center py-20 bg-white rounded-2xl border border-dashed border-gray-300"><p class="text-gray-400 font-bold">No orders found.</p></div>

                <div v-else v-for="order in ordersList" :key="order.name" class="bg-white rounded-xl border border-gray-200 overflow-hidden shadow-sm hover:shadow-md transition-all">
                    
                    <div class="bg-gray-50 px-6 py-3 border-b border-gray-100 flex justify-between items-center">
                        <div>
                            <span class="font-mono font-bold text-gray-900">#{{ order.name }}</span>
                            <span class="text-xs text-gray-500 ml-2">{{ order.customer_name }}</span>
                        </div>
                        <div class="flex items-center gap-3">
                            <span class="px-2 py-1 rounded text-[10px] font-bold uppercase border shadow-sm" :class="getStatusClass(order)">
                                {{ order.docstatus === 0 ? 'Pending Acceptance' : order.status }}
                            </span>
                            <span class="font-bold text-gray-800">₹{{ order.grand_total }}</span>
                        </div>
                    </div>

                    <div class="p-6">
                        <div v-for="item in order.items" :key="item.item_code" class="flex gap-4 items-center py-3 border-b border-gray-100 last:border-0">
                            <div class="w-12 h-12 border rounded bg-white p-1 flex-shrink-0 flex items-center justify-center overflow-hidden">
                                <img v-if="item.image" :src="item.image" class="w-full h-full object-contain" />
                                <div v-else class="text-xl opacity-20">📦</div>
                            </div>
                            <div class="flex-1">
                                <p class="text-sm font-bold text-gray-800">{{ item.item_name }}</p>
                                <p class="text-xs text-gray-500">{{ item.qty }} x ₹{{ item.amount / item.qty }}</p>
                            </div>
                            <span class="text-sm font-bold text-gray-900">₹{{ item.amount }}</span>
                        </div>

                        <div class="mt-6 flex justify-end gap-3 pt-4 border-t border-gray-100">
                            
                            <button v-if="order.docstatus === 0" 
                                @click="processOrder(order.name)" 
                                class="bg-blue-600 hover:bg-blue-700 text-white px-5 py-2 rounded-lg text-xs font-bold uppercase shadow-md transition-all flex items-center gap-2">
                                <span>⚡</span> Accept Order
                            </button>

                            <button v-if="order.docstatus === 1 && (order.per_delivered || 0) < 100" 
                                @click="createDelivery(order.name)" 
                                class="bg-orange-500 hover:bg-orange-600 text-white px-5 py-2 rounded-lg text-xs font-bold uppercase shadow-md transition-all flex items-center gap-2">
                                <span>🚚</span> Deliver
                            </button>

                            <button v-if="order.docstatus === 1 && (order.per_billed || 0) < 100" 
                                @click="createInvoice(order.name)" 
                                class="bg-green-600 hover:bg-green-700 text-white px-5 py-2 rounded-lg text-xs font-bold uppercase shadow-md transition-all flex items-center gap-2">
                                <span>🧾</span> Invoice
                            </button>

                            <span v-if="isCompleted(order)" class="text-green-600 font-bold text-sm self-center flex items-center gap-1">✅ Completed</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { createResource } from 'frappe-ui'
import { session } from '../data/session'
import Toast from '../components/Toast.vue'
import ConfirmDialog from '../components/ConfirmDialog.vue'
import SellerSidebar from '../components/SellerSidebar.vue'

const router = useRouter()
const toastRef = ref(null)
const confirmRef = ref(null)
const isMobileSidebarOpen = ref(false)
const activeCustomerFilter = ref(null)
const pageTitle = computed(() => activeCustomerFilter.value ? 'Filtered Orders' : 'Dashboard')

const sellerOrders = createResource({ url: 'doppio_demo.api.get_seller_orders', auto: true })
const ordersList = computed(() => sellerOrders.data || [])

const handleCustomerFilter = (name) => { activeCustomerFilter.value = name; sellerOrders.submit({ customer_name: name }) }
const handleResetFilter = () => { activeCustomerFilter.value = null; sellerOrders.submit({ customer_name: null }) }
const handleLogout = async () => { await session.logout.submit(); router.push({ name: 'Home', query: { login: 'true' } }) }

const isCompleted = (order) => (order.per_delivered >= 100 && order.per_billed >= 100) || order.status === 'Completed'

const getStatusClass = (order) => {
    if (order.docstatus === 0) return 'bg-yellow-100 text-yellow-800' // Draft
    if (isCompleted(order)) return 'bg-green-100 text-green-800'
    return 'bg-blue-100 text-blue-800' // Submitted
}

const processOrder = async (id) => {
    try {
        const res = await fetch('/api/method/doppio_demo.api.update_order_status', {
            method: 'POST', headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ order_name: id, status: 'To Deliver and Bill' })
        })
        const data = await res.json()
        if (data.message.status === 'success') {
            toastRef.value.add('Order Accepted!', 'success')
            sellerOrders.fetch()
        } else throw new Error(data.message.message)
    } catch(e) { toastRef.value.add(e.message, 'error') }
}

const createDelivery = async (id) => {
    if (!await confirmRef.value.open('Create Delivery?', 'Generate Delivery Note?')) return;
    try {
        const res = await fetch('/api/method/doppio_demo.api.create_delivery_note', {
            method: 'POST', headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ order_name: id })
        })
        const data = await res.json()
        if (data.message.status === 'success') {
            toastRef.value.add('Delivery Note Created!', 'success')
            sellerOrders.fetch()
        } else throw new Error(data.message.message)
    } catch(e) { toastRef.value.add(e.message, 'error') }
}

const createInvoice = async (id) => {
    if (!await confirmRef.value.open('Create Invoice?', 'Generate Sales Invoice?')) return;
    try {
        const res = await fetch('/api/method/doppio_demo.api.create_sales_invoice', {
            method: 'POST', headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ order_name: id })
        })
        const data = await res.json()
        if (data.message.status === 'success') {
            toastRef.value.add('Invoice Created!', 'success')
            sellerOrders.fetch()
        } else throw new Error(data.message.message)
    } catch(e) { toastRef.value.add(e.message, 'error') }
}
</script>