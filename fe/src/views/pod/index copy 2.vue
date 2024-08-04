<template>
  <div class="terminal-wrapper">
    <div ref="terminalContainer" class="terminal-container"></div>
  </div>
</template>

<script>
import { Terminal } from 'xterm';
import { FitAddon } from 'xterm-addon-fit';
import { io } from 'socket.io-client';

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
      theme: {
        background: '#000000',
        foreground: '#ffffff',
      },
      rendererType: 'canvas', // 使用 canvas 渲染器
    });
    this.fitAddon = new FitAddon();
    this.terminal.loadAddon(this.fitAddon);
    this.terminal.open(this.$refs.terminalContainer);
    this.fitAddon.fit();
    this.terminal.focus();  // 确保终端聚焦

    console.log('Initializing terminal and WebSocket connection...');

    // 建立 WebSocket 連接
    const backendUrl = process.env.NODE_ENV === 'development' ? 'http://localhost:5000' : `http://${window.location.hostname}:5000`;
    console.log('Connecting to backend at:', backendUrl);
    this.socket = io(backendUrl, {
      transports: ['websocket']
    });

    this.socket.on('connect', () => {
      this.socket.emit('execute_command', { command: '' }); // 发送空命令以触发SSH登录
      console.log('Connected to backend server.');
    });

    this.socket.on('disconnect', () => {
      this.terminal.writeln('Disconnected from server');
      console.log('Disconnected from backend server.');
    });

    this.socket.on('response', (data) => {
      if (data.output) {
        this.terminal.write(data.output);
        console.log('Received output from backend:', data.output);
      }
    });

    // 捕捉終端輸入
    this.terminal.onData((data) => {
      this.socket.emit('input', { input: data });
      console.log('Sent input to backend:', data);
    });

    // 調整終端大小
    window.addEventListener('resize', () => {
      this.fitAddon.fit();
      this.socket.emit('resize', { cols: this.terminal.cols, rows: this.terminal.rows });
      console.log('Terminal resized to:', this.terminal.cols, 'cols and', this.terminal.rows, 'rows');
    });
  },
  beforeDestroy() {
    if (this.socket) {
      this.socket.disconnect();
    }
  },
};
</script>

<style scoped>
.terminal-wrapper {
  width: 100%;
  height: 100vh; /* 使终端占满整个可用高度 */
  display: flex;
  align-items: center;
  justify-content: center;
  background: #1e1e1e;
}
.terminal-container {
  width: 100%;
  height: 100%;
  background: #000;
}
</style>
