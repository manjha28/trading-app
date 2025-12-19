import api from "./client";

export async function login(email: string, password: string) {
  const res = await api.post("/api/auth/login", {
    email,
    password,
  });
  return res.data;
}

export async function signup(name: string, email: string, password: string) {
  const res = await api.post("/api/auth/signup", {
    name,
    email,
    password,
  });
  return res.data;
}


export function startGoogleLogin() {
  window.location.href = "/api/auth/google";
}
