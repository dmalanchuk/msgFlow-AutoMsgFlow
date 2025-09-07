import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
  scenarios: {
    login_logout_scenario: {
      executor: 'constant-vus',
      vus: 50,         // кількість паралельних користувачів
      duration: '30s', // загальна тривалість тесту
    },
  },
};

const usersCount = 1000;

export default function () {
  // login random user
  let i = Math.floor(Math.random() * usersCount) + 1;

  let loginPayload = JSON.stringify({
    email: `user${i}@example.com`,
    password: '111pass111'
  });

  let loginRes = http.post('http://127.0.0.1:8000/auth/login', loginPayload, {
    headers: { 'Content-Type': 'application/json', accept: 'application/json' }
  });

  check(loginRes, {
    'login success': (r) => r.status === 200
  });

  // retrieve refresh_token
  let cookies = loginRes.cookies['refresh_token'];
  if (!cookies || cookies.length === 0) {
    console.log('❌ No refresh token!');
    return;
  }
  let refreshToken = cookies[0].value;

  // logout user
  let logoutRes = http.del('http://127.0.0.1:8000/auth/logout', null, {
    headers: {
      accept: 'application/json',
      'Cookie': `refresh_token=${refreshToken}`
    }
  });

  check(logoutRes, {
    'logout success': (r) => r.status === 204
  });

  sleep(0.1); // pause
}
