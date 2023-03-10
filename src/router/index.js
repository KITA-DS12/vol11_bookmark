import Vue from 'vue'
import VueRouter from 'vue-router'
import UploadView from '../views/UploadView.vue'
import DownloadView from '../views/DownloadView.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'upload',
    component: UploadView,
    props: true
  },
  {
    path: '/download',
    name: 'download',
    component: DownloadView,
    props: true
  },
]

const router = new VueRouter({
  base: process.env.BASE_URL,
  routes
})

export default router
