import { createRouter, createWebHistory } from "vue-router"
import { session } from "./data/session"

const LoginView = () => import("@/pages/Login.vue") // ✅ New Page
const CustomerView = () => import("@/pages/CustomerView.vue")
const SellerView = () => import("@/pages/SellerView.vue")

const routes = [
    // ✅ Default Route -> Login
    { path: '/', redirect: '/login' },
    { path: '/login', name: 'Login', component: LoginView },

    // --- CUSTOMER AREA ---
    { path: '/customer', name: 'Home', component: CustomerView, meta: { requiresAuth: true } },
    { path: '/customer/cart', name: 'Cart', component: CustomerView, meta: { requiresAuth: true } },
    { path: '/customer/orders', name: 'Orders', component: CustomerView, meta: { requiresAuth: true } },
    { path: '/customer/shop/:pincode', name: 'ShopPincode', component: CustomerView, meta: { requiresAuth: true } },
    { path: '/customer/shop/:pincode/:society', name: 'ShopSociety', component: CustomerView, meta: { requiresAuth: true } },
    { path: '/customer/shop/:pincode/:society/:category', name: 'ShopCategory', component: CustomerView, meta: { requiresAuth: true } },
    { path: '/customer/shop/:pincode/:society/:category/:sellerName', name: 'SellerItems', component: CustomerView, props: true, meta: { requiresAuth: true } },

    // --- SELLER AREA ---
    { 
        path: '/seller', 
        component: SellerView,
        meta: { requiresAuth: true, requiresSeller: true },
        children: [
            { path: '', name: 'SellerDashboard', component: SellerView },
            { path: 'orders', name: 'SellerOrders', component: SellerView },
            { path: 'products', name: 'SellerProducts', component: SellerView }
        ]
    },
]

const router = createRouter({
    history: createWebHistory("/frontend"),
    routes,
})

// 🔒 SECURITY GUARD
router.beforeEach(async (to, from, next) => {
    let isLoggedIn = session.isLoggedIn;

    // Refresh Role if logged in but role missing
    if (isLoggedIn && !session.role) {
        try {
            const res = await fetch('/api/method/doppio_demo.api.get_user_role_info');
            const data = await res.json();
            if (data.message) {
                session.role = data.message.role;
                session.sellerCompany = data.message.company;
            }
        } catch (e) {}
    }

    // 1. Agar User Login hai aur Login Page par ja raha hai -> Redirect
    if (to.name === 'Login' && isLoggedIn) {
        if (session.role === 'Seller') return next({ name: 'SellerDashboard' });
        return next({ name: 'Home' });
    }

    // 2. Agar Page ko Login chahiye aur User Guest hai -> Redirect to Login
    if (to.meta.requiresAuth && !isLoggedIn) {
        return next({ name: 'Login' });
    }

    // 3. Seller Protection
    if (to.matched.some(record => record.meta.requiresSeller)) {
        if (session.role !== 'Seller') return next({ name: 'Home' });
    }

    next();
})

export default router