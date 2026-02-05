import { createRouter, createWebHistory } from "vue-router"
import { session } from "./data/session"
import { userResource } from "@/data/user"

// Components Lazy Load
const Login = () => import("@/pages/Login.vue")
const CustomerView = () => import("@/pages/CustomerView.vue")
const SellerView = () => import("@/pages/SellerView.vue")

const routes = [
    {
        path: "/account/login",
        name: "Login",
        component: Login,
    },
    // --- CUSTOMER ROUTES ---
    {
        path: '/',
        component: CustomerView, // ✅ Loads MarketSidebar
        children: [
            { path: '', name: 'Home', component: CustomerView },
            { path: 'cart', name: 'Cart', component: CustomerView },
            { path: 'orders', name: 'Orders', component: CustomerView },
            { path: ':pincode', name: 'ShopPincode', component: CustomerView },
            { path: ':pincode/:society', name: 'ShopSociety', component: CustomerView },
            { path: ':pincode/:society/:category', name: 'ShopCategory', component: CustomerView },
            { path: ':pincode/:society/:category/:sellerName', name: 'SellerItems', component: CustomerView, props: true }
        ]
    },
    // --- SELLER ROUTES ---
    {
        path: '/seller',
        component: SellerView, // ✅ Loads SellerSidebar
        children: [
            { path: '', name: 'SellerDashboard', component: SellerView },
            { path: 'orders', name: 'SellerOrders', component: SellerView },
            { path: 'products', name: 'SellerProducts', component: SellerView }
        ]
    }
]

const router = createRouter({
    history: createWebHistory("/frontend"),
    routes,
})

// --- SECURITY GUARD ---
router.beforeEach(async (to, from, next) => {
    let isLoggedIn = session.isLoggedIn
    try { await userResource.promise } catch (error) { isLoggedIn = false }

    // Role Refresh Logic
    if (isLoggedIn && !session.role) {
        try {
            const res = await fetch('/api/method/doppio_demo.api.get_user_role_info')
            const data = await res.json()
            if (data.message) {
                session.role = data.message.role
                session.sellerCompany = data.message.company
            }
        } catch (e) { console.error(e) }
    }

    if (to.name !== "Login" && !isLoggedIn) {
        next({ name: "Login" })
    } 
    else if (to.name === "Login" && isLoggedIn) {
        next(session.role === 'Seller' ? { name: 'SellerDashboard' } : { name: 'Home' })
    }
    else if (to.path.startsWith('/seller') && session.role !== 'Seller') {
        next({ name: 'Home' }) // Customer ko wapas bhej do
    } 
    else {
        next()
    }
})

export default router