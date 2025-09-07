import http from "k6/http";
import { check, sleep } from "k6";
import { decode as base64Decode } from "k6/encoding";

export const options = {
  vus: 100,
  duration: "30s",
};

// --- Підстав свій refresh токен сюди ---
const REFRESH_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkYW5paWwubWFyeXN5a0BnbWFpbC5jb20iLCJleHAiOjE3NTk3ODE5ODl9.dMFNWlC7hpHdqJT_X5iTQAkKsyZdSeIOM2O-xhPV5U0";


// --- Безпечне парсування JWT ---
function parseJwt(token) {
  try {
    const parts = token.split(".");
    if (parts.length !== 3) return { sub: "daniil.marysyk@gmail.com" };

    const base64Url = parts[1];
    const jsonPayload = base64Decode(base64Url, "base64");
    if (!jsonPayload) return { sub: "daniil.marysyk@gmail.com" };

    const obj = JSON.parse(jsonPayload);
    return obj && obj.sub ? obj : { sub: "daniil.marysyk@gmail.com" };
  } catch (e) {
    return { sub: "daniil.marysyk@gmail.com" };
  }
}

const email = parseJwt(REFRESH_TOKEN).sub;

// --- Генерація випадкових назв ---
function randomLetters(length) {
  const chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
  let result = "";
  for (let i = 0; i < length; i++) {
    result += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  return result;
}

// --- Створення payload для сценарію ---
function createScenarioPayload() {
  const uid = Date.now();
  const name = randomLetters(Math.floor(Math.random() * 16) + 1);

  return JSON.stringify({
    name: name,
    chat_url: "https://t.me/testingmsgflow",
    owner_email: email,
    event: [{ type: "message_received", source: "telegram" }],
    conditions: [{ type: "contains_word", params: { word: `word-${uid}` } }],
    actions: [{ type: "send_message", params: { text: `new post ${uid}` } }],
  });
}

// --- Основна функція k6 ---
export default function () {
  const payload = createScenarioPayload();

  const headers = {
    "Content-Type": "application/json",
    Accept: "application/json",
    "Cookie": `refresh_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkYW5paWwubWFyeXN5a0BnbWFpbC5jb20iLCJleHAiOjE3NTk3ODE5ODl9.dMFNWlC7hpHdqJT_X5iTQAkKsyZdSeIOM2O-xhPV5U0`,
  };

  const res = http.post("http://127.0.0.1:8000/scenarios/scenario", payload, { headers });

  check(res, { "status is 201": (r) => r.status === 201 });

  sleep(1);
}
