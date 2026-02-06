import { reactive, computed } from "vue"
import { createResource } from "frappe-ui"
import { userResource } from "./user"
import router from "@/router"

export function sessionUser() {
    const cookies = new URLSearchParams(document.cookie.split("; ").join("&"))
    let _sessionUser = cookies.get("user_id")
    if (_sessionUser === "Guest") _sessionUser = null
    return _sessionUser
}

export const session = reactive({
    user: sessionUser(),
    isLoggedIn: computed(() => !!session.user),

    // ✅ YE STANDARD FRAPPE LOGIN HAI
    login: createResource({
        url: "login", // Standard endpoint
        makeParams({ email, password }) {
            return { usr: email, pwd: password }
        },
        onSuccess(data) {
            userResource.reload()
            session.user = sessionUser()
            // Login ke baad kya karna hai wo component decide karega
        },
    }),

    logout: createResource({
        url: "doppio_demo.api.logout", // Hamara custom fix wala logout
        onSuccess() {
            userResource.reset()
            session.user = null
            window.location.reload() // Page refresh to clear state
        },
    }),
})