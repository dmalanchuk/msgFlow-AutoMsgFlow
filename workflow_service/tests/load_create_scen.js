// import http from 'k6/http';
// import { check, sleep } from 'k6';
//
// export let options = {
//     vus: 10, // кількість одночасних користувачів
//     duration: '30s', // тривалість тесту
// };
//
// export default function () {
//     let url = 'http://127.0.0.1:8000/scenarios/create';
//     let payload = JSON.stringify({
//         name: "string",
//         chat_url: "https://t.me/testingmsgflow",
//         event: {
//             type: "message_received",
//             source: "telegram"
//         },
//         condition: {
//             type: "contains_word",
//             params: { word: "sa" }
//         },
//         action: {
//             type: "send_message",
//             params: { text: "as" }
//         }
//     });
//
//     let params = {
//         headers: {
//             'accept': 'application/json',
//             'Content-Type': 'application/json',
//         },
//     };
//
//     let res = http.post(url, payload, params);
//
//     check(res, {
//         'status is 200': (r) => r.status === 200,
//     });
//
//     sleep(0.1); // затримка між запитами
// }


import http from 'k6/http';
import { check, sleep } from 'k6';

// Налаштування тесту
export let options = {
    vus: 5,         // кількість одночасних віртуальних користувачів
    duration: '20s' // тривалість тесту
};

export default function () {
    // 1. Логін
    const loginPayload = JSON.stringify({
        email: 'daniil.marysyk@gmail.com',
        password: 'qwe123qwe'
    });

    const loginParams = {
        headers: { 'Content-Type': 'application/json' },
    };

    let loginRes = http.post('http://127.0.0.1:8000/auth/login', loginPayload, loginParams);

    check(loginRes, {
        'login status 200': (r) => r.status === 200
    });

    // 2. Беремо кукі з відповіді і зберігаємо в cookieJar
    let jar = http.cookieJar();
    // Якщо бекенд ставить owner_email у cookie
    if (loginRes.cookies['owner_email']) {
        jar.set('http://127.0.0.1:8000', 'owner_email', loginRes.cookies['owner_email'][0].value);
    }

    // 3. Створення сценарію
    const scenarioPayload = JSON.stringify({
        name: "string",
        chat_url: "https://t.me/testingmsgflow",
        event: { type: "message_received", source: "telegram" },
        condition: { type: "contains_word", params: { word: "sa" } },
        action: { type: "send_message", params: { text: "as" } }
    });

    const scenarioParams = {
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        // кукі автоматично підставляються через jar
    };

    let scenarioRes = http.post('http://127.0.0.1:8000/scenarios/create', scenarioPayload, scenarioParams);

    check(scenarioRes, {
        'scenario created': (r) => r.status === 200
    });

    sleep(1); // невелика пауза між ітераціями
}
