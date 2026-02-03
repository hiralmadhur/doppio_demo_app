<template>
  <div>
    <div v-if="isOpen" @click="isOpen = false" class="md:hidden fixed inset-0 bg-black/60 z-40 backdrop-blur-sm transition-opacity"></div>

    <div class="md:hidden fixed top-0 left-0 w-full bg-slate-800 text-white p-4 z-50 flex items-center justify-between shadow-md">
      <div class="flex items-center gap-3">
        <button @click="isOpen = !isOpen" class="focus:outline-none p-1 rounded hover:bg-slate-700 transition">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path></svg>
        </button>
        <span class="font-bold text-lg tracking-wide">HyperMart</span>
      </div>
    </div>

    <div :class="[
      'fixed top-0 left-0 h-screen w-80 bg-white text-gray-800 flex flex-col border-r border-gray-200 shadow-xl z-50 font-sans transition-transform duration-300 ease-in-out',
      isOpen ? 'translate-x-0' : '-translate-x-full',
      'md:translate-x-0 md:relative md:block'
    ]">
      
      <div class="h-16 flex items-center px-6 bg-slate-800 text-white mt-16 md:mt-0 shrink-0 shadow-md z-10">
        <h2 class="text-lg font-bold flex items-center gap-3 tracking-wide">
          <svg class="w-6 h-6 text-yellow-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"></path></svg>
          Browse Market
        </h2>
      </div>

      <div class="flex-1 overflow-y-auto custom-scrollbar p-0 bg-white hover:overflow-y-scroll">
        
        <div class="px-6 py-4 border-b border-gray-100 flex justify-between items-center sticky top-0 bg-white z-10 shadow-sm">
          <h3 class="text-xs font-bold text-gray-500 uppercase tracking-wider">Select Location</h3>
          <button @click="collapseAll" class="text-[10px] text-blue-600 hover:underline cursor-pointer font-medium bg-blue-50 px-2 py-1 rounded border border-blue-100">Collapse All</button>
        </div>

        <div v-for="pin in treeData" :key="pin.pincode" class="select-none border-b border-gray-100 last:border-0">
          
          <button @click="togglePincode(pin.pincode)" 
            :class="['w-full flex items-center justify-between px-6 py-4 hover:bg-gray-50 transition-colors group', 
            expandedPincodes.includes(pin.pincode) ? 'bg-blue-50 text-blue-800' : 'text-gray-700']">
            <div class="flex items-center gap-3">
              <span class="font-bold text-base tracking-wide">{{ pin.pincode }}</span>
            </div>
            <svg :class="['w-4 h-4 text-gray-400 transition-transform duration-300', expandedPincodes.includes(pin.pincode) ? 'rotate-90 text-blue-600' : '']" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path></svg>
          </button>

          <div v-show="expandedPincodes.includes(pin.pincode)" class="bg-gray-50/80 pb-2 shadow-inner">
            <div v-for="society in pin.societies" :key="society.name">
              
              <button @click="toggleSociety(society.name)" 
                :class="['w-full flex items-center justify-between pl-10 pr-6 py-3 hover:bg-white transition-colors border-l-4',
                expandedSocieties.includes(society.name) ? 'border-blue-500 bg-white font-medium text-gray-900 shadow-sm' : 'border-transparent text-gray-600']">
                <div class="flex items-center gap-2">
                  <span class="text-lg">🏢</span>
                  <span class="text-sm">{{ society.name }}</span>
                </div>
                <svg :class="['w-3 h-3 text-gray-400 transition-transform duration-200', expandedSocieties.includes(society.name) ? 'rotate-90' : '']" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path></svg>
              </button>

              <div v-show="expandedSocieties.includes(society.name)" class="space-y-1 py-1">
                <div v-for="category in society.categories" :key="category.name">
                  
                  <button @click="toggleCategory(category.name)" 
                    :class="['w-full flex items-center justify-between pl-14 pr-6 py-2 transition-colors rounded-r-md mr-2',
                    expandedCategories.includes(category.name) ? 'text-blue-700 bg-blue-50' : 'text-gray-500 hover:text-gray-800 hover:bg-gray-100']">
                    <div class="flex items-center gap-2">
                      <span class="text-xs">📦</span>
                      <span class="text-sm font-medium">{{ category.name }}</span>
                    </div>
                    <svg :class="['w-3 h-3 text-gray-400 transition-transform duration-200', expandedCategories.includes(category.name) ? 'rotate-90' : '']" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path></svg>
                  </button>

                  <div v-show="expandedCategories.includes(category.name)" class="ml-14 pl-4 border-l border-gray-300 my-1 space-y-2 py-1">
                    <div v-for="seller in category.sellers" :key="seller.name" class="relative">
                      
                      <button @click="toggleSeller(seller.name)" 
                        :class="['w-full flex items-center justify-between py-1 pr-4 transition-colors',
                        expandedSellers.includes(seller.name) ? 'text-gray-900 font-semibold' : 'text-gray-500 hover:text-gray-700']">
                        <div class="flex items-center gap-2">
                          <div class="w-5 h-5 rounded-full bg-slate-200 flex items-center justify-center text-[10px] font-bold text-slate-600">
                            {{ seller.name.charAt(0) }}
                          </div>
                          <span class="text-sm">{{ seller.name }}</span>
                        </div>
                        <svg :class="['w-3 h-3 text-gray-300 transition-transform duration-200', expandedSellers.includes(seller.name) ? 'rotate-90 text-gray-600' : '']" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path></svg>
                      </button>

                      <div v-show="expandedSellers.includes(seller.name)" class="ml-3 mt-2 space-y-1 border-l-2 border-dashed border-gray-200 pl-3">
                        <router-link :to="{ name: 'CustomerView', query: { company: seller.name, society: society.name } }"
                           @click="isOpen = false"
                           class="flex items-center gap-2 px-3 py-2 text-xs text-blue-600 bg-blue-50 hover:bg-blue-100 rounded transition-colors font-medium">
                           <span>📄</span> View Orders
                        </router-link>
                        <div class="flex items-center gap-2 px-3 py-2 text-xs text-gray-600 hover:bg-gray-100 rounded transition-colors cursor-pointer">
                           <span>🧾</span> Invoices
                        </div>
                      </div>

                    </div>
                  </div>

                </div>
              </div>

            </div>
          </div>

        </div>

        <div class="h-32"></div>
      </div>

      <div class="p-4 border-t border-gray-200 bg-gray-50 text-center shrink-0 z-10">
        <p class="text-[10px] text-gray-400 font-medium uppercase tracking-widest">Powered by Frappe</p>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const isOpen = ref(false)

// State
const expandedPincodes = ref([])
const expandedSocieties = ref([])
const expandedCategories = ref([])
const expandedSellers = ref([])

// Toggle
const toggleItem = (arrayRef, item) => {
  if (arrayRef.value.includes(item)) {
    arrayRef.value = arrayRef.value.filter(i => i !== item)
  } else {
    arrayRef.value.push(item)
  }
}
const togglePincode = (id) => toggleItem(expandedPincodes, id)
const toggleSociety = (id) => toggleItem(expandedSocieties, id)
const toggleCategory = (id) => toggleItem(expandedCategories, id)
const toggleSeller = (id) => toggleItem(expandedSellers, id)
const collapseAll = () => {
  expandedPincodes.value = []
  expandedSocieties.value = []
  expandedCategories.value = []
  expandedSellers.value = []
}

// Data (Heavy for Scrolling)
const treeData = [
  {
    pincode: "388001",
    societies: [
      {
        name: "Gokuldham Society",
        categories: [
          { name: "Electronics", sellers: [{ name: "Gada Electronics" }, { name: "Vijay Sales" }] },
          { name: "Groceries", sellers: [{ name: "Big Basket" }, { name: "Reliance Fresh" }] }
        ]
      },
      {
        name: "Krishna Heights",
        categories: [
          { name: "Dairy", sellers: [{ name: "Amul Parlour" }] }
        ]
      }
    ]
  },
  {
    pincode: "400001",
    societies: [
      {
        name: "Lodha Park",
        categories: [
          { name: "Furniture", sellers: [{ name: "IKEA" }, { name: "Pepperfry" }] }
        ]
      }
    ]
  },
  // Extra Pincodes
  { pincode: "380015", societies: [{ name: "Satellite Towers", categories: [] }] },
  { pincode: "380054", societies: [{ name: "Thaltej Greens", categories: [] }] },
  { pincode: "390020", societies: [{ name: "Alkapuri Hts", categories: [] }] },
  { pincode: "500081", societies: [{ name: "Hitech City", categories: [] }] },
  { pincode: "560001", societies: [{ name: "MG Road Blr", categories: [] }] },
  { pincode: "110001", societies: [{ name: "Connaught Place", categories: [] }] },
  { pincode: "400050", societies: [{ name: "Bandra West", categories: [] }] },
  { pincode: "600028", societies: [{ name: "RA Puram", categories: [] }] },
]
</script>

<style scoped>
/* --- STRIP SCROLLBAR (SLIM & MODERN) --- */

/* Chrome, Edge, Safari */
.custom-scrollbar::-webkit-scrollbar {
  width: 6px; /* Patla Strip */
}

/* Track ko Invisible/Transparent bana diya */
.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent; 
}

/* Thumb (Goli) ko visible banaya */
.custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: #cbd5e1; /* Light Grey (Subtle) */
  border-radius: 20px; /* Fully Rounded */
}

/* Hover karne par thoda dark hoga */
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background-color: #94a3b8; /* Darker Grey */
}

/* Firefox */
.custom-scrollbar {
  scrollbar-width: thin;
  scrollbar-color: #cbd5e1 transparent;
}
</style>