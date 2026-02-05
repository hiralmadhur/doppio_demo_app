<template>
  <div class="h-full overflow-y-auto bg-gray-50 p-4 sm:p-8 custom-scrollbar">
    
    <div class="max-w-5xl mx-auto">
      <div class="bg-white rounded-2xl p-8 shadow-sm border border-gray-100 mb-8 flex flex-col md:flex-row items-center justify-between gap-6">
        <div>
          <h1 class="text-3xl font-bold text-gray-800 mb-2">
            Welcome back, <span class="text-orange-600">{{ getUserName() }}</span>! 👋
          </h1>
          <p class="text-gray-500 text-lg">
            Ready to order something fresh today? Select your location from the sidebar to get started.
          </p>
          <button @click="$router.push('/shop')" 
            class="mt-6 bg-gray-900 text-white px-8 py-3 rounded-lg text-sm font-bold uppercase tracking-wide hover:bg-black shadow-lg transition-transform active:scale-95">
            Start Shopping ➔
          </button>
        </div>
        <div class="text-[80px] leading-none opacity-90 select-none animate-bounce-slow">
          🛒
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
        
        <div @click="$router.push('/shop')" 
          class="bg-white p-6 rounded-xl border border-gray-200 shadow-sm hover:shadow-md hover:border-orange-300 cursor-pointer transition-all group">
          <div class="w-12 h-12 bg-orange-50 rounded-lg flex items-center justify-center text-2xl mb-4 group-hover:scale-110 transition-transform">
            🏪
          </div>
          <h3 class="text-lg font-bold text-gray-800">Browse Shops</h3>
          <p class="text-sm text-gray-500 mt-1">Explore sellers near you and find the best deals.</p>
        </div>

        <div @click="$router.push('/shop/orders')"
          class="bg-white p-6 rounded-xl border border-gray-200 shadow-sm hover:shadow-md hover:border-blue-300 cursor-pointer transition-all group">
          <div class="w-12 h-12 bg-blue-50 rounded-lg flex items-center justify-center text-2xl mb-4 group-hover:scale-110 transition-transform">
            📦
          </div>
          <h3 class="text-lg font-bold text-gray-800">My Orders</h3>
          <p class="text-sm text-gray-500 mt-1">Track active orders and view your purchase history.</p>
        </div>

        <div class="bg-white p-6 rounded-xl border border-gray-200 shadow-sm hover:shadow-md hover:border-green-300 cursor-pointer transition-all group">
          <div class="w-12 h-12 bg-green-50 rounded-lg flex items-center justify-center text-2xl mb-4 group-hover:scale-110 transition-transform">
            🎧
          </div>
          <h3 class="text-lg font-bold text-gray-800">Help & Support</h3>
          <p class="text-sm text-gray-500 mt-1">Need help with an order? Contact our support team.</p>
        </div>
      </div>

      <div class="bg-gradient-to-r from-indigo-600 to-purple-700 rounded-2xl p-8 text-white shadow-lg flex flex-col sm:flex-row items-center justify-between gap-6 relative overflow-hidden">
        <div class="absolute -right-10 -top-10 w-40 h-40 bg-white opacity-10 rounded-full blur-2xl"></div>
        <div class="absolute left-10 bottom-0 w-20 h-20 bg-white opacity-10 rounded-full blur-xl"></div>
        
        <div class="relative z-10">
          <span class="bg-white/20 text-xs font-bold px-2 py-1 rounded uppercase tracking-wider mb-2 inline-block">New Offer</span>
          <h2 class="text-2xl font-bold mb-1">Free Delivery on First Order!</h2>
          <p class="text-white/80 text-sm">Use code <span class="font-mono font-bold bg-white/20 px-1 rounded">HYPERNEW</span> at checkout.</p>
        </div>
        <button class="relative z-10 bg-white text-indigo-700 px-6 py-2 rounded-full text-xs font-bold uppercase hover:bg-gray-100 shadow-md">
          Claim Now
        </button>
      </div>

    </div>
  </div>
</template>

<script setup>
import { session } from '../data/session'

// User ka naam nikaalne ke liye simple logic
const getUserName = () => {
  if (session.user) {
    // Agar email hai (e.g. demo@gmail.com) to sirf "demo" dikhayenge
    return session.user.split('@')[0]
  }
  return 'Guest'
}
</script>

<style scoped>
/* Optional: Slight bounce animation for the shopping cart emoji */
@keyframes bounce-slow {
  0%, 100% { transform: translateY(-5%); }
  50% { transform: translateY(5%); }
}
.animate-bounce-slow {
  animation: bounce-slow 3s infinite ease-in-out;
}
</style>