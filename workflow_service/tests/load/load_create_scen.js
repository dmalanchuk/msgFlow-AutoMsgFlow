// import http from "k6/http";
// import { check, sleep } from "k6";
//
// // Налаштування навантаження
// export const options = {
//   vus: 1,         // кількість віртуальних користувачів
//   duration: "30s", // час тесту
// };
//
// // Список дозволених доменів для owner_email
// const DOMAINS = ["gmail.com", "ukr.net"];
//
// function randomEmail(uid) {
//   const domain = DOMAINS[Math.floor(Math.random() * DOMAINS.length)];
//   return `user${uid}@${domain}`;
// }
//
// export default function () {
//   // Унікальний ідентифікатор для генерації унікальних даних
//   const uid = `${Date.now()}-${Math.floor(Math.random() * 100000)}`;
//
//   const payload = JSON.stringify({
//     name: `scenario`,
//     chat_url: "https://t.me/testingmsgflow",
//     owner_email: randomEmail(uid),
//     event: [
//       {
//         type: "message_received",
//         source: "telegram",
//       },
//     ],
//     conditions: [
//       {
//         type: "contains_word",
//         params: {
//           word: `word-${uid}`,
//         },
//       },
//     ],
//     actions: [
//       {
//         type: "send_message",
//         params: {
//           text: `new post ${uid}`,
//         },
//       },
//     ],
//   });
//
//   const headers = {
//     "Content-Type": "application/json",
//     Accept: "application/json",
//       "Cookie": "token=<eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkYW5paWwubWFyeXN5a0BnbWFpbC5jb20iLCJleHAiOjE3NTk3ODE5ODl9.dMFNWlC7hpHdqJT_X5iTQAkKsyZdSeIOM2O-xhPV5U0>"
//   };
//
//   // Відправка POST-запиту
//   const res = http.post("http://127.0.0.1:8000/scenarios/scenario", payload, {
//     headers,
//   });
//
//   check(res, {
//     "status is 201": (r) => r.status === 201,
//   });
//
//   sleep(1);
// }






import http from "k6/http";
import { check, sleep } from "k6";

// Налаштування навантаження
export const options = {
  vus: 5,          // кількість віртуальних користувачів
  duration: "30s", // час тесту
};

// Список дозволених доменів для owner_email
const DOMAINS = ["gmail.com", "ukr.net"];

// Генерація випадкових букв
function randomLetters(length) {
  const chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
  let result = "";
  for (let i = 0; i < length; i++) {
    result += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  return result;
}

// Генерація випадкових email
function randomEmail() {
  const domain = DOMAINS[Math.floor(Math.random() * DOMAINS.length)];
  const uid = `${Date.now()}${Math.floor(Math.random() * 1000)}`;
  return `user${uid}@${domain}`;
}

// --- setup(): логін один раз ---
export function setup() {
  const loginPayload = JSON.stringify({
    email: "daniil.marysyk@gmail.com", // свій тестовий користувач
    password: "qwe123qwe"
  });

  const loginRes = http.post("http://127.0.0.1:8000/auth/login", loginPayload, {
    headers: { "Content-Type": "application/json" }
  });

  check(loginRes, { "login status is 200": (r) => r.status === 200 });

  const token = loginRes.cookies.token[0].value;
  const email = loginRes.json().email || "user@example.com";

  return { token, email };
}

// --- default function: використання токена ---
export default function (data) {
  const scenarioName = randomLetters(16); // назва 1-16 букв
  const uid = Date.now();

  const scenarioPayload = JSON.stringify({
    name: scenarioName,
    chat_url: "https://t.me/testingmsgflow",
    owner_email: data.email,
    event: [
      { type: "message_received", source: "telegram" }
    ],
    conditions: [
      { type: "contains_word", params: { word: `word-${uid}` } }
    ],
    actions: [
      { type: "send_message", params: { text: `new post ${uid}` } }
    ]
  });

  const headers = {
    "Content-Type": "application/json",
    Accept: "application/json",
    "Cookie": `token=${data.token}`
  };

  const res = http.post("http://127.0.0.1:8000/scenarios/scenario", scenarioPayload, { headers });

  check(res, {
    "status is 201": (r) => r.status === 201
  });

  sleep(1);
}
