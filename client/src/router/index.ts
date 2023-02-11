import { createRouter, createWebHashHistory, RouteRecordRaw } from "vue-router";
import UploadView from "../views/UploadView.vue";
import DownloadView from "../views/DownloadView.vue";

const routes: Array<RouteRecordRaw> = [
  {
    path: "/",
    name: "upload",
    component: UploadView,
  },
  {
    path: "/",
    name: "download",
    component: DownloadView,
  },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router;
