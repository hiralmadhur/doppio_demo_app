import { createApp } from "vue"
import { setConfig, frappeRequest, resourcesPlugin, pageMetaPlugin } from 'frappe-ui'
import App from "./App.vue"
import router from "./router"
import { initSocket } from "./socket"
import './index.css'

// Global Components (Optional: Add common components here if needed)
import {
    Button,
    Input,
    TextInput,
    FormControl,
    ErrorMessage,
    Dialog,
    Alert,
    Badge,
} from "frappe-ui"

const app = createApp(App)

// Frappe UI Config
setConfig('resourceFetcher', frappeRequest)

// Register Plugins
app.use(router)
app.use(resourcesPlugin)
app.use(pageMetaPlugin)

// Register Global Components
app.component('Button', Button)
app.component('TextInput', TextInput)
app.component('Input', Input)
app.component('FormControl', FormControl)
app.component('ErrorMessage', ErrorMessage)
app.component('Dialog', Dialog)
app.component('Alert', Alert)
app.component('Badge', Badge)

// Socket Setup
const socket = initSocket()
app.config.globalProperties.$socket = socket

// Mount
app.mount('#app')