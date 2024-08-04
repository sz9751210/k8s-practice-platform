<template>
  <div class="common-layout">
    <!-- container 佈局 -->
    <el-container style="height: 100vh">
      <!-- 側邊導覽 -->
      <el-aside class="aside" :width="asideWidth">
        <el-affix class="aside-affix">
          <div class="aside-logo">
            <el-image class="logo-image" :src="logo" />
            <span :class="[isCollapse ? 'is-collapse' : '']">
              <transition name="fade" @after-enter="showText = true">
                <span class="logo-name" v-if="showText">K8s Platform</span>
              </transition>
            </span>
          </div>
        </el-affix>
        <!-- router 定義vue-router模式，菜單欄的index跟路由規則中的path綁定 -->
        <!-- default-active 默認激活的菜單欄，這裡根據打開的path來找到對應的欄 -->
        <el-menu
          class="aside-menu"
          router
          :default-active="$route.path"
          :collapse="isCollapse"
          background-color="#131b27"
          text-color="#bfcbd9"
          active-text-color="#20a0ff"
        >
          <!-- routers 就是路由規則，router/index.js 中的routes -->
          <div v-for="menu in routers" :key="menu">
            <!-- 第一種情況，children 只有一個子菜單 -->
            <el-menu-item
              class="aside-menu-item"
              v-if="menu.children && menu.children.length == 1"
              :index="menu.path"
            >
              <!-- 處理圖標和菜單欄的名字 -->
              <el-icon>
                <component :is="menu.children[0].icon" />
              </el-icon>
              <template #title>
                {{ menu.children[0].name }}
              </template>
            </el-menu-item>
            <!-- 第二種情況，children 大於一個子菜單  -->
            <!-- 注意 el-menu-item 在折疊後，title 的部分會自動消失，但 el-sub-menu 不會，需要自己控制，因此在 template title 裏面，要將 menu.name 的部分做邏輯判斷 -->
            <el-sub-menu
              class="aside-submenu"
              v-else-if="menu.children && menu.children.length > 1"
              :index="menu.path"
            >
              <!-- 處理父菜單欄 -->
              <template #title>
                <el-icon>
                  <component :is="menu.icon" />
                </el-icon>
                <span :class="[isCollapse ? 'is-collapse' : '']">
                  {{ menu.name }}
                </span>
              </template>
              <!-- 處理子菜單 -->
              <el-menu-item
                class="aside-menu-childitem"
                v-for="child in menu.children"
                :key="child"
                :index="child.path"
              >
                <template #title>
                  <el-icon>
                    <component :is="child.icon" />
                  </el-icon>
                  {{ child.name }}
                </template>
              </el-menu-item>
            </el-sub-menu>
          </div>
        </el-menu>
      </el-aside>

      <el-container>
        <el-header class="header">
          <el-row :gutter="10">
            <!-- 折疊按鈕 -->
            <el-col :span="1">
              <div class="header-collapse" @click="onCollapse">
                <el-icon>
                  <!-- isCollapse為true，表示關閉，icon顯示為展開 -->
                  <component :is="isCollapse ? 'expand' : 'fold'" />
                </el-icon>
              </div>
            </el-col>
            <!-- 麵包屑 -->
            <el-col :span="10">
              <div class="header-breadcrumb">
                <el-breadcrumb separator="/">
                  <!-- 最外層工作台，寫死 -->
                  <el-breadcrumb-item :to="{ path: '/' }"
                    >Workbench</el-breadcrumb-item
                  >
                  <!-- 循環出路由規則中的父name和子name -->
                  <template
                    v-for="(matched, m) in this.$route.matched"
                    :key="m"
                  >
                    <el-breadcrumb-item v-if="matched.name != undefined">
                      {{ matched.name }}
                    </el-breadcrumb-item>
                  </template>
                </el-breadcrumb>
              </div>
            </el-col>
            <!-- 用戶訊息 -->
            <el-col :span="13">
              <div class="header-user">
                <el-dropdown>
                  <div class="header-dropdown">
                    <!-- 用戶頭像和用戶名 -->
                    <el-image class="avator-image" :src="avator"></el-image>
                    <!-- <span>{{ username }}</span> -->
                  </div>
                  <!-- 下拉選單 -->
                  <template #dropdown>
                    <el-dropdown-menu>
                      <el-dropdown-item @click="logout">登出</el-dropdown-item>
                    </el-dropdown-menu>
                  </template>
                </el-dropdown>
              </div>
            </el-col>
          </el-row>
        </el-header>
        <el-main class="main"><router-view></router-view></el-main>
        <el-backtop target=".main"></el-backtop>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import { useRouter } from "vue-router";

export default {
  data() {
    return {
      logo: require("@/assets/logo.png"),
      avator: require("@/assets/avator.gif"),
      asideWidth: "220px",
      isCollapse: false,
      showText: true,
      routers: [],
    };
  },
  methods: {
    onCollapse() {
      // 當前狀態是折疊的，點擊後展開
      // 如果是折疊狀態，就要執行展開的動作
      if (this.isCollapse) {
        // 展開後寬度調整為220px
        this.asideWidth = "220px";
        // 將狀態改為false，代表狀態是展開
        this.isCollapse = false;
        // 等待過渡結束後顯示文本
        setTimeout(() => {
          this.showText = true;
        }, 300); // 500 毫秒是 transition 時間
      } else {
        // 當前狀態是展開的，點擊後折疊
        this.asideWidth = "64px";
        this.isCollapse = true;
        this.showText = false;
      }
    },
    logout() {
      localStorage.removeItem("token");
      this.$router.push({ name: "Login" });
    },
  },
  beforeMount() {
    this.routers = useRouter().options.routes;

    console.log(this.routers);
  },
};
</script>

<style scoped>
/* 側邊欄折疊速度，背景色 */
.aside {
  transition: all 0.5s;
  background-color: #131b27;
}
.aside-logo {
  background-color: #131b27;
  height: 60px;
  color: white;
}
.logo-image {
  width: 40px;
  height: 40px;
  top: 14px;
  padding-left: 12px;
}
.logo-name {
  font-size: 20px;
  font-weight: bold;
  padding: 10px;
}
.is-collapse {
  display: none;
}
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active in <2.1.8 */ {
  opacity: 0;
}
/* 菜單欄滾軸不顯示 */
.aside::-webkit-scrollbar {
  display: none;
}
.aside-affix {
  border-bottom-width: 0;
}
/* 右邊邊框寬度 */
.aside-menu {
  border-right-width: 0;
}

/* 菜单栏的位置以及颜色 */
/* 內邊距左邊的距離 */
/* .aside-menu-item {
  padding-left: 20px !important;
} */
.aside-menu-item.is-active {
  background-color: #1f2a3a;
}
/* 鼠標移過去的背景色變化 */
.aside-menu-item:hover {
  background-color: #142c4e;
}

.aside-submenu {
  padding-left: 0px !important;
}

.aside-menu-childitem {
  padding-left: 40px !important;
}
.aside-menu-childitem.is-active {
  background-color: #1f2a3a;
}
.aside-menu-childitem:hover {
  background-color: #142c4e;
}

/* header */
.header {
  z-index: 1200;
  line-height: 60px;
  font-size: 24px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.12), 0 0 6px rgba(0, 0, 0, 0.04);
}
.header-collapse {
  cursor: pointer;
}

.header-breadcrumb {
  /* margin-top: 20px; */
  padding-top: 0.9em;
}
/* 用戶訊息 */
.avator-image {
  top: 12px;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 8px;
  cursor: pointer; /* 確保指針變為手型 */
  border: none;
  box-shadow: none;
}
/* header */
.header-user {
  text-align: right;
  /* float: right; */
}
/* main */
.main {
  padding: 10px;
}
</style>
