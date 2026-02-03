<template>
  <div class="h-screen flex flex-col bg-gray-50 font-sans">
    
    <div class="bg-white px-8 py-5 border-b shadow-sm flex justify-between items-center">
      <div>
        <h1 class="text-2xl font-bold text-gray-800">My Orders</h1>
        <div class="text-sm text-gray-500 flex gap-2 mt-1">
          <span v-if="society" class="bg-green-100 text-green-800 px-2 rounded text-xs font-bold pt-0.5">
            🏠 {{ society }}
          </span>
          <span v-if="society && company">•</span>
          <span v-if="company">
            Seller: <span class="font-bold text-gray-800">{{ company }}</span>
          </span>
        </div>
      </div>
      <button class="bg-gray-900 text-white px-6 py-2 rounded-lg font-bold hover:bg-black transition shadow-lg flex items-center gap-2">
        <span>+</span> Place New Order
      </button>
    </div>

    <div class="flex-1 overflow-auto p-8">
      
      <div v-if="orders.loading" class="text-center py-20 text-gray-400 flex flex-col items-center">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900 mb-2"></div>
        Fetching orders for {{ company }}...
      </div>
      
      <div v-else-if="orders.data?.length" class="space-y-4 max-w-5xl mx-auto">
        <div v-for="order in orders.data" :key="order.name" 
             class="bg-white p-6 rounded-xl border border-gray-200 shadow-sm hover:shadow-md transition cursor-pointer flex justify-between items-center group">
          
          <div>
            <div class="text-lg font-bold text-blue-600 group-hover:text-blue-700">{{ order.name }}</div>
            <div class="text-gray-400 text-xs mt-1 flex gap-2">
              <span>📅 {{ order.transaction_date }}</span>
            </div>
          </div>

          <div class="text-right">
            <div class="text-xl font-bold text-gray-900">₹ {{ order.grand_total }}</div>
            <span :class="['inline-block mt-1 px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wide', 
              order.status === 'Completed' ? 'bg-green-100 text-green-700' : 
              order.status === 'Cancelled' ? 'bg-red-100 text-red-700' : 'bg-yellow-100 text-yellow-700']">
              {{ order.status }}
            </span>
          </div>
        </div>
      </div>

      <div v-else class="flex flex-col items-center justify-center h-64 text-gray-400">
        <div class="text-5xl mb-4">🛍️</div>
        <p class="text-lg text-gray-500">No orders found.</p>
        <p class="text-sm">Start shopping from <b>{{ company }}</b>!</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, watch } from 'vue'
import { createResource } from 'frappe-ui'
import { useRoute } from 'vue-router'

const route = useRoute()

// --- 1. REACTIVE VARIABLES ---
// Computed use kar rahe hain taaki jab URL query change ho, ye variables apne aap update ho jayein
const company = computed(() => route.query.company)
const society = computed(() => route.query.society)

// --- 2. DATA FETCHING ---
const orders = createResource({
  url: 'frappe.client.get_list',
  makeParams() {
    return {
      doctype: 'Sales Order',
      filters: { 
        // Note: .value lagana zaroori hai kyunki ye computed properties hain
        company: company.value 
      },
      fields: ['name', 'transaction_date', 'grand_total', 'status'],
      order_by: 'creation desc'
    }
  },
  auto: true
})

// --- 3. WATCHER (The Magic) ---
// Jab user sidebar se naya seller select karega, URL change hoga.
// Ye watcher URL change detect karega aur naya data fetch karega.
watch(
  () => route.query.company, 
  (newCompany) => {
    if (newCompany) {
      orders.fetch()
    }
  }
)
</script>