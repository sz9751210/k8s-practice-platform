import { createRouter, createWebHistory } from "vue-router";
// 導入進度條
import NProgress from "nprogress";
import "nprogress/nprogress.css";
import Layout from "@/layout/Layout.vue";


const routes = [
  {
    path: "/",
    redirect: "/home",
  },
  {
    path: "/home",
    icon: "odometer",
    component: Layout,
    children: [
      {
        path: "/home",
        name: "Home",
        icon: "odometer",
        meta: { title: "Home", requireAuth: true },
        component: () => import("@/views/home/Home.vue"),
      },
    ],
  },
  {
    path: "/event",
    component: Layout,
    icon: "list",
    children: [
      {
        path: "/event",
        name: "Events",
        icon: "list",
        meta: { title: "Event", requireAuth: true },
        component: () => import("@/views/event/index"),
      },
    ],
  },
  {
    path: "/404",
    name: "404",
    meta: { title: "Page Not Found", requireAuth: false },
    component: () => import("@/views/common/404.vue"),
  },
  {
    path: "/:pathMatch(.*)",
    redirect: "/404",
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// 進度條配置
NProgress.inc(0.2); // 設置進度條遞增
NProgress.configure({ easing: "ease", speed: 500, showSpinner: false }); // 設置進度條顯示方式

function isTokenExpired(token){
  const payload = JSON.parse(atob(token.split(".")[1]));
  const now = Math.floor(Date.now() / 1000);
  return now > payload.exp;
}

// 路由守衛
router.beforeEach((to, from, next) => {
  // 進度條開始
  NProgress.start();
  // 設置頭部
  if (to.meta.title) {
    document.title = to.meta.title;
  } else {
    document.title = "Devops Dashboard";
  }

  // const token = localStorage.getItem("token");

  // // 使用 Array.prototype.some(), 遍歷所有record, 只要有一個record.meta.requireAuth = true, 就表示有登入權限
  // if (to.matched.some((record) => record.meta.requireAuth)) {
  //   if (!token|| isTokenExpired(token)) {
  //     localStorage.removeItem("token");
  //     next({ path: "/login", query: { redirect: to.fullPath } });
  //   } else {
  //     next();
  //   }
  // } else {
  //   next();
  // }
  next();
});

router.afterEach(() => {
  // 進度條結束
  NProgress.done();
});

export default router;
