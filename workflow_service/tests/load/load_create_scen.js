import http from "k6/http";
import { check, sleep } from "k6";

// Налаштування навантаження
export const options = {
  vus: 80,         // кількість віртуальних користувачів
  duration: "30s", // час тесту
};

export default function () {
  // Робимо унікальність через timestamp + випадкове число
  const uid = `${Date.now()}-${Math.floor(Math.random() * 100000)}`;

  const payload = JSON.stringify({
    name: `scenario-${uid}`,
    chat_url: "https://t.me/testingmsgflow",
    owner_email: "example@gmail.com",
    event: {
      type: "message_received",
      source: "telegram",
    },
    condition: {
      type: "contains_word",
      params: {
        word: `word-${uid}`,
      },
    },
    action: {
      type: "send_message",
      params: {
        text: `new post ${uid}`,
      },
    },
  });

  const headers = {
    "Content-Type": "application/json",
    Accept: "application/json",
  };

  const res = http.post("http://127.0.0.1:8003/scenarios", payload, {
    headers,
  });

  check(res, {
    "status is 201": (r) => r.status === 201,
  });

  sleep(1);
}
