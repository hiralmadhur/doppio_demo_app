<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-100">
    <div class="bg-white p-8 rounded-xl shadow-lg w-full max-w-sm">
      <h2 class="text-2xl font-bold mb-6 text-center text-gray-800">Login</h2>
      <form @submit.prevent="login" class="space-y-4">
        <div>
          <label class="block text-gray-700 text-sm font-bold mb-2">Email</label>
          <input v-model="email" type="text" class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:border-blue-500" required>
        </div>
        <div>
          <label class="block text-gray-700 text-sm font-bold mb-2">Password</label>
          <input v-model="password" type="password" class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:border-blue-500" required>
        </div>
        <button type="submit" class="w-full bg-black text-white font-bold py-2 rounded-lg hover:bg-gray-800 transition">
          {{ loading ? 'Checking...' : 'Login' }}
        </button>
      </form>
      <p v-if="error" class="text-red-500 text-sm mt-4 text-center">{{ error }}</p>
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
const error = ref('')
const loading = ref(false)

const login = async () => {
    loading.value = true
    error.value = ''
    try {
        const res = await fetch('/api/method/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ usr: email.value, pwd: password.value })
        })
        const data = await res.json()

        if (data.message === 'Logged In') {
            session.isLoggedIn = true
            session.user = email.value
            
            // Check Role
            const roleRes = await fetch('/api/method/doppio_demo.api.get_user_role_info')
            const roleData = await roleRes.json()

            if (roleData.message) {
                session.role = roleData.message.role
                
                if (roleData.message.role === 'Seller') {
                    session.sellerCompany = roleData.message.company
                    router.push({ name: 'SellerDashboard' })
                } else {
                    router.push({ name: 'Home' })
                }
            }
        } else {
            error.value = data.message || "Invalid Login"
        }
    } catch (e) {
        error.value = "Error: " + e.message
    } finally {
        loading.value = false
    }
}
</script>