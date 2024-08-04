<template>
  <div class="container">
    <div class="sidebar">
      <div class="sidebar-header">Task</div>

      <!-- 確保當前問題索引小於問題數量時顯示問題 -->
      <div
        class="score-display"
        v-if="currentQuestionIndex >= questions.length"
      >
        <p>Final Score: {{ score }}</p>
        <p>Quiz completed!</p>
      </div>

      <div class="question-container" v-else>
        <!-- 根據題目類型渲染 -->
        <p>{{ questions[currentQuestionIndex]?.question }}</p>

        <!-- 選擇題 -->
        <ul
          v-if="questions[currentQuestionIndex]?.type === 'multiple-choice'"
          class="option-list"
        >
          <li
            v-for="(option, index) in questions[currentQuestionIndex]?.options"
            :key="index"
            @click="handleOptionClick(index)"
          >
            {{ option }}
          </li>
        </ul>

        <!-- 確認題 -->
        <div
          v-else-if="questions[currentQuestionIndex]?.type === 'confirmation'"
        >
          <p>{{ questions[currentQuestionIndex]?.checkInstructions }}</p>
          <button @click="handleCheck()">Check</button>
        </div>
      </div>
    </div>
    <div class="terminal-wrapper">
      <div ref="terminalContainer" class="terminal-container"></div>
    </div>
  </div>
</template>

<script>
import { fetchQuestions, checkAnswer } from "@/api/questions";
import { Terminal } from "xterm";
import { FitAddon } from "xterm-addon-fit";
import { io } from "socket.io-client";
import "xterm/css/xterm.css";
import { ElMessage } from "element-plus";

export default {
  data() {
    return {
      socket: null,
      terminal: null,
      fitAddon: null,
      currentQuestionIndex: 0,
      isAnswerCorrect: false,
      questions: [],
      score: 0,
      pointsPerQuestion: 0, // 每道題的分數
    };
  },
  mounted() {
    this.loadQuestions();
    this.initializeTerminal();
    this.initializeWebSocket();
    window.addEventListener("resize", this.handleResize);
  },
  beforeDestroy() {
    if (this.socket) {
      this.socket.disconnect();
    }
    window.removeEventListener("resize", this.handleResize);
  },
  methods: {
    async loadQuestions() {
      try {
        const data = await fetchQuestions();
        console.log("fetch quetsion", data);
        if (data && data.length > 0) {
          this.questions = data; // 獲取的題目資料
          this.pointsPerQuestion = 100 / this.questions.length; // 計算每道題的分數
        } else {
          console.error("No questions found.");
        }
      } catch (error) {
        console.error("Failed to fetch questions:", error);
      }
    },
    initializeTerminal() {
      // if (this.$refs.terminalContainer) {
      this.terminal = new Terminal({
        cursorBlink: true,
        theme: {
          background: "#000000",
          foreground: "#ffffff",
        },
        rendererType: "canvas",
      });
      this.fitAddon = new FitAddon();
      this.terminal.loadAddon(this.fitAddon);
      this.terminal.open(this.$refs.terminalContainer);
      this.fitAddon.fit();
      this.terminal.focus();

      this.terminal.onData(this.handleTerminalInput);
      // } else {
      //   console.error("Terminal container not found.");
      // }
    },
    initializeWebSocket() {
      const backendUrl =
        process.env.NODE_ENV === "development"
          ? "http://localhost:5000"
          : `http://${window.location.hostname}:5000`;
      this.socket = io(backendUrl, {
        transports: ["websocket"],
      });

      this.socket.on("connect", this.handleSocketConnect);
      this.socket.on("disconnect", this.handleSocketDisconnect);
      this.socket.on("response", this.handleSocketResponse);
    },
    handleTerminalInput(data) {
      this.socket.emit("input", { input: data });
    },
    handleSocketConnect() {
      this.socket.emit("execute_command", { command: "" });
      this.terminal.writeln("Connected to backend server.");
    },
    handleSocketDisconnect() {
      this.terminal.writeln("Disconnected from backend server.");
    },
    handleSocketResponse(data) {
      if (data.output) {
        this.terminal.write(data.output);
      }
    },
    handleResize() {
      if (this.fitAddon) {
        this.fitAddon.fit();
        this.socket.emit("resize", {
          cols: this.terminal.cols,
          rows: this.terminal.rows,
        });
      }
    },
    async handleOptionClick(index) {
      const questionId = this.questions[this.currentQuestionIndex]._id; // 獲取問題 ID
      const checkType = this.questions[this.currentQuestionIndex].type;
      try {
        const { isCorrect } = await checkAnswer({
          questionId: questionId,
          selectedOption: index,
          checkType: checkType,
        });
        if (isCorrect) {
          ElMessage.success("Correct answer!");
          this.isAnswerCorrect = true;
          this.score += this.pointsPerQuestion; // 增加分數
        } else {
          ElMessage.error("Incorrect answer. Try again.");
          this.isAnswerCorrect = false;
        }
      } catch (error) {
        console.error("Error checking answer:", error);
        ElMessage.error("An error occurred while checking the answer.");
      } finally {
        this.nextQuestion();
      }
    },
    async handleCheck() {
      const questionId = this.questions[this.currentQuestionIndex]._id; // 獲取問題 ID
      const checkType = this.questions[this.currentQuestionIndex].type;
      try {
        // 發送檢查請求到後端
        const { isCorrect } = await checkAnswer({
          questionId: questionId,
          checkType: checkType,
        });
        if (isCorrect) {
          ElMessage.success("Correct! Well done!");
          this.score += this.pointsPerQuestion; // 增加分數
        } else {
          ElMessage.error("Incorrect! Try again.");
        }
      } catch (error) {
        console.error("Error checking answer:", error);
        ElMessage.error("An error occurred while checking the answer.");
      } finally {
        this.nextQuestion();
      }
    },
    nextQuestion() {
      if (
        // this.isAnswerCorrect &&
        this.currentQuestionIndex <
        this.questions.length - 1
      ) {
        this.currentQuestionIndex++;
        // this.isAnswerCorrect = false;
      } else {
        // ElMessage.info("You have completed all the questions.");
        ElMessage.info("Quiz completed!");
        this.currentQuestionIndex = this.questions.length;
      }
      this.isAnswerCorrect = false;
    },
  },
};
</script>

<style scoped>
.container {
  display: flex;
  height: 100vh;
  background: #1e1e1e;
}
.sidebar {
  width: 30%;
  background: #2e2e2e;
  color: #fff;
  padding: 1rem;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}
.sidebar-header {
  font-size: 1.5rem;
  margin-bottom: 1rem;
}
.score-display {
  font-size: 1.25rem;
  margin-bottom: 1rem;
}
.question-container {
  flex: 1;
}
.option-list {
  list-style: none;
  padding: 0;
}
.option-list li {
  padding: 0.5rem;
  margin-bottom: 0.5rem;
  background: #3e3e3e;
  cursor: pointer;
  transition: background 0.3s;
}
.option-list li:hover {
  background: #5e5e5e;
}
.navigation {
  display: flex;
  justify-content: flex-end;
}
.navigation button {
  padding: 0.5rem 1rem;
  background: #5e5e5e;
  border: none;
  color: white;
  cursor: pointer;
}
.navigation button:disabled {
  background: #3e3e3e;
  cursor: not-allowed;
}
.terminal-wrapper {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}
.terminal-container {
  width: 100%;
  height: 100%;
  background: #000;
}
</style>
