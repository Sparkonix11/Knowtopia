import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router/router.js'
import store from './stores/store.js'
import '@material/web/all.js'
import './theme/light.css'


const app = createApp(App)
app.use(store)
app.use(router)
app.mount('#app')
