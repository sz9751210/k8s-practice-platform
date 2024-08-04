import { createApp } from "vue";
import App from "./App.vue";

import ElementPlus from "element-plus";
import "element-plus/dist/index.css";
import * as ELIcons from "@element-plus/icons-vue";
import router from "./router";

// codemirror 編輯器
import { GlobalCmComponent } from "codemirror-editor-vue3";
// 引入主題 可以從 codemirror/theme/ 下引入多個
import "codemirror/theme/idea.css";
// 引入語言模式 可以從 codemirror/mode/ 下引入多個
import "codemirror/mode/yaml/yaml.js";

const app = createApp(App);
for (const iconName in ELIcons) {
  app.component(iconName, ELIcons[iconName]);
}
app.use(ElementPlus);
app.use(GlobalCmComponent, { componentName: "codemirror" });
app.use(router);
app.mount("#app");
