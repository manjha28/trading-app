import api from "./axios";

export async function login(email: string, password: string) {
  const res = await api.post("/auth/login", { email, password });
  return res.data;
}

export async function signup(name: string, email: string, password: string) {
  const res = await api.post("/auth/signup", {
    name,
    email,
    password,
  });
  return res.data;
}

export function startGoogleLogin() {
  window.location.href =
    "https://moonlit-spooky-goblin-8000.app.github.dev/api/auth/google";
}
