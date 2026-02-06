<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 px-4">
    <div class="max-w-md w-full bg-white rounded-2xl shadow-xl p-8 border border-gray-100">
      
      <div class="text-center mb-8">
        <div class="text-6xl mb-4">🛒</div>
        <h2 class="text-3xl font-extrabold text-gray-900">Welcome Back</h2>
        <p class="text-sm text-gray-500 mt-2">Sign in to access your dashboard</p>
      </div>

      <form @submit.prevent="handleLogin" class="space-y-6">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Email Address</label>
          <input v-model="email" type="email" required 
            class="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-orange-500 focus:border-orange-500 outline-none transition-all"
            placeholder="user@example.com" />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Password</label>
          <input v-model="password" type="password" required 
            class="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-orange-500 focus:border-orange-500 outline-none transition-all"
            placeholder="••••••••" />
        </div>

        <div v-if="errorMessage" class="text-red-500 text-sm text-center font-bold bg-red-50 p-2 rounded">
          {{ errorMessage }}
        </div>

        <button type="submit" :disabled="loading"
          class="w-full bg-gray-900 text-white py-3.5 rounded-xl font-bold text-lg hover:bg-black transition-all shadow-lg active:scale-95 flex justify-center items-center gap-2">
          <span v-if="loading" class="w-5 h-5 border-2 border-white/50 border-t-white rounded-full animate-spin"></span>
          <span>{{ loading ? 'Signing In...' : 'Login' }}</span>
        </button>
      </form>

      <div class="mt-6 text-center">
        <p class="text-xs text-gray-400">By logging in, you agree to our Terms & Conditions.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { session } from '../data/session'

const router = useRouter()
const email = ref('')
const password = ref('')
const errorMessage = ref('')
const loading = ref(false)

const handleLogin = async () => {
  loading.value = true
  errorMessage.value = ''
  
  try {
    // 1. Login Call
    await session.login.submit({ email: email.value, password: password.value })
    
    // 2. Fetch Role Info
    const res = await fetch('/api/method/doppio_demo.api.get_user_role_info')
    const data = await res.json()
    
    if (data.message) {
        session.role = data.message.role
        session.sellerCompany = data.message.company
        
        // 3. Redirect Based on Role
        if (data.message.role === 'Seller') {
            router.push({ name: 'SellerDashboard' })
        } else {
            router.push({ name: 'Home' })
        }
    }
  } catch (e) {
    errorMessage.value = "Invalid Email or Password"
    console.error(e)
  } finally {
    loading.value = false
  }
}
</script>