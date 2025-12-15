import axios from "axios";

const api = axios.create({
  baseURL: "https://moonlit-spooky-goblin-65wjr75r57w35xvr-8000.app.github.dev/api",
  headers: {
    "Content-Type": "application/json",
  },
});

export default api;
