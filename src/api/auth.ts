import axios from "axios";

const origin = window.location.origin;

let apiOrigin: string;

if (origin.includes("-3000.app.github.dev")) {
  apiOrigin = origin.replace("-3000.app.github.dev", "-8000.app.github.dev");
} else {
  apiOrigin = "http://localhost:8000"; // local dev fallback
}

const API_URL = `${apiOrigin}/api`;

export async function login(email: string, password: string) {
  const res = await axios.post(`${API_URL}/auth/login`, { email, password });
  return res.data;
}

export async function signup(name: string, email: string, password: string) {
  const res = await axios.post(`${API_URL}/auth/signup`, {
    name,
    email,
    password,
  });
  return res.data;
}

export function startGoogleLogin() {
  window.location.href = `${API_URL}/auth/google`;
}
