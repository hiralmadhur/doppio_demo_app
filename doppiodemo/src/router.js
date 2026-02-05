import { createRouter, createWebHistory } from "vue-router"
import { session } from "./data/session"
import { userResource } from "@/data/user"

const routes = [
    {
        name: "Login",
        path: "/account/login",
        component: () => import("@/pages/Login.vue"),
    },
    {
        path: '/',
        component: () => import("@/pages/CustomerView.vue"),
        children: [

            {
                path: '',
                name: 'Home',
                component: () => import("@/pages/CustomerView.vue"),
            },

            {
                path: 'cart',
                name: 'Cart',
                component: () => import("@/pages/CustomerView.vue"),
            },
            {
                path: 'orders',
                name: 'Orders',
                component: () => import("@/pages/CustomerView.vue"),
            },

            {
                path: ':pincode',
                name: 'ShopPincode',
                component: () => import("@/pages/CustomerView.vue"),
            },
            {
                path: ':pincode/:society',
                name: 'ShopSociety',
                component: () => import("@/pages/CustomerView.vue"),
            },
            {
                path: ':pincode/:society/:category',
                name: 'ShopCategory',
                component: () => import("@/pages/CustomerView.vue"),
            },
            {
                path: ':pincode/:society/:category/:sellerName',
                name: 'SellerItems',
                component: () => import("@/pages/CustomerView.vue"),
                props: true
            }
        ]
    }
]

const router = createRouter({
    history: createWebHistory("/customer"),
    routes,
})

router.beforeEach(async (to, from, next) => {
    let isLoggedIn = session.isLoggedIn
    try { await userResource.promise } catch (error) { isLoggedIn = false }

    if (to.name === "Login" && isLoggedIn) {
        next({ name: "Home" }) // 
    } else if (to.name !== "Login" && !isLoggedIn) {
        next({ name: "Login" })
    } else {
        next()
    }
})

export default router