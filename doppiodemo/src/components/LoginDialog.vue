<template>
    <Dialog v-model="show" :options="{ size: 'md' }">
        <template #body-content>
            <div class="p-6 bg-white rounded-lg">
                <div class="text-center mb-6">
                    <div class="text-4xl mb-2">🔐</div>
                    <h2 class="text-2xl font-bold text-gray-900">Sign In</h2>
                    <p class="text-gray-500 text-sm">Seller & Customer Login</p>
                </div>

                <form @submit.prevent="handleLogin" class="space-y-4">
                    <FormControl type="email" label="Email" v-model="email" placeholder="seller@example.com"
                        :disabled="loading" />
                    <FormControl type="password" label="Password" v-model="password" placeholder="••••••••"
                        :disabled="loading" />

                    <div v-if="error" class="text-red-600 text-xs bg-red-50 p-2 rounded font-bold text-center">
                        {{ error }}
                    </div>

                    <Button variant="solid" theme="gray" size="lg" class="w-full justify-center" type="submit"
                        :loading="loading">
                        Login
                    </Button>
                </form>
            </div>
        </template>
    </Dialog>
</template>

<script setup>
import { ref, computed } from 'vue'
import { Dialog, FormControl, Button } from 'frappe-ui'
import { session } from '../data/session'
import { useRouter } from 'vue-router'

const props = defineProps(['modelValue'])
const emit = defineEmits(['update:modelValue', 'success'])
const router = useRouter()

const show = computed({
    get: () => props.modelValue,
    set: (val) => emit('update:modelValue', val)
})

const email = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')



const handleLogin = async () => {
    loading.value = true
    error.value = ''
    try {
        // 1. Login API Call
        await session.login.submit({ email: email.value, password: password.value })

        // 2. Turant Role Pucho
        const res = await fetch('/api/method/doppio_demo.api.get_user_role_info')
        const data = await res.json()

        if (data.message) {
            // Session update karo
            session.role = data.message.role
            session.sellerCompany = data.message.company

            // 3. Strict Redirection
            if (data.message.role === 'Seller') {
                show.value = false
                router.push({ name: 'SellerDashboard' }) // ✅ Force Seller View
            } else {
                show.value = false
                emit('success')
                // Customer wahi rahega jaha wo tha
            }
        }
    } catch (e) {
        error.value = "Invalid Credentials"
    } finally {
        loading.value = false
    }
}
</script>