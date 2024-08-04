<template>
  <div>
    <!-- header -->
    <div class="header">
      <el-button type="warning" icon="refresh" @click="resetK8sEnvironment"
        >重置 K8s 環境</el-button
      >
    </div>
    <div ref="terminalContainer" class="terminal-container"></div>
  </div>
</template>

<script>
import { resetK8s } from "@/api/k8s";
import { ElMessage } from "element-plus";
import { io } from "socket.io-client";
import { Terminal } from "xterm";
import { FitAddon } from "xterm-addon-fit";

export default {
  data() {
    return {
      socket: null,
      terminal: null,
      fitAddon: null,
    };
  },
  mounted() {
    // 初始化 xterm 終端
    this.terminal = new Terminal({
      cursorBlink: true,
      rows: 24,
      cols: 80,
      theme: {
        background: "#000000",
        foreground: "#ffffff",
      },
    });
    this.fitAddon = new FitAddon();
    this.terminal.loadAddon(this.fitAddon);
    this.terminal.open(this.$refs.terminalContainer);
    this.fitAddon.fit();

    // 建立 WebSocket 連接
    this.socket = io("http://backend:5000"); // 在 Docker Compose 內部網絡中使用服務名稱

    this.socket.on("connect", () => {
      this.terminal.writeln("Connected to server");
    });

    this.socket.on("disconnect", () => {
      this.terminal.writeln("Disconnected from server");
    });

    this.socket.on("response", (data) => {
      if (data.output) {
        this.terminal.write(data.output);
      }
    });

    // 捕捉終端輸入
    this.terminal.onData((data) => {
      this.socket.emit("input", { input: data });
    });

    // 調整終端大小
    window.addEventListener("resize", () => {
      this.fitAddon.fit();
      this.socket.emit("resize", {
        cols: this.terminal.cols,
        rows: this.terminal.rows,
      });
    });
  },
  methods: {
    async resetK8sEnvironment() {
      try {
        await resetK8s();
        ElMessage({
          message: "K8s 環境重置成功",
          type: "success",
          duration: 5 * 1000,
        });
      } catch (error) {
        console.error("Error resetting K8s environment:", error);
        ElMessage({
          message: "K8s 環境重置失敗",
          type: "error",
          duration: 5 * 1000,
        });
      }
    },
  },
  beforeDestroy() {
    if (this.socket) {
      this.socket.disconnect();
    }
  },
};
</script>

<style scoped>
.header {
  display: flex;
  justify-content: flex-start;
  margin-bottom: 20px;
}
.terminal-container {
  width: 100%;
  height: 500px;
  background: #000;
}
</style>
