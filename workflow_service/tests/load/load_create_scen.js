import http from "k6/http";
import { check, sleep } from "k6";

// Налаштування навантаження
export const options = {
  vus: 500,         // кількість віртуальних користувачів
  duration: "30s", // час тесту
};

// Список дозволених доменів для owner_email
const DOMAINS = ["gmail.com", "ukr.net"];

function randomEmail(uid) {
  const domain = DOMAINS[Math.floor(Math.random() * DOMAINS.length)];
  return `user${uid}@${domain}`;
}

export default function () {
  // Унікальний ідентифікатор для генерації унікальних даних
  const uid = `${Date.now()}-${Math.floor(Math.random() * 100000)}`;

  const payload = JSON.stringify({
    name: `scenario`,
    chat_url: "https://t.me/testingmsgflow",
    owner_email: randomEmail(uid),
    event: [
      {
        type: "message_received",
        source: "telegram",
      },
    ],
    conditions: [
      {
        type: "contains_word",
        params: {
          word: `word-${uid}`,
        },
      },
    ],
    actions: [
      {
        type: "send_message",
        params: {
          text: `new post ${uid}`,
        },
      },
    ],
  });

  const headers = {
    "Content-Type": "application/json",
    Accept: "application/json",
  };

  // Відправка POST-запиту
  const res = http.post("http://127.0.0.1:8003/scenarios/scenario", payload, {
    headers,
  });

  check(res, {
    "status is 201": (r) => r.status === 201,
  });

  sleep(1);
}
