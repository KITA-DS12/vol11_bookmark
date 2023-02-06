import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";

import ElementPlus from "element-plus"
import "element-plus/theme-chalk/index.css"
import axios from "axios"

axios.defaults.baseURL = 'http://localhost:8888'
axios.defaults.withCredentials = true

const app = createApp(App)

app.use(store)
app.use(router)
app.use(ElementPlus)

app.mount("#app");
