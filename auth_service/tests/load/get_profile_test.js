import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
  scenarios: {
    login_profile_scenario: {
      executor: 'constant-vus',
      vus: 100,         // кількість паралельних користувачів
      duration: '30s', // загальна тривалість тесту
    },
  },
};

const usersCount = 1000;

export default function () {
  // 1. login random user
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

  // 2. retrieve refresh_token
  let cookies = loginRes.cookies['refresh_token'];
  if (!cookies || cookies.length === 0) {
    console.log('❌ No refresh token!');
    return;
  }
  let refreshToken = cookies[0].value;

  // 3. call get_profile with cookie
  let profileRes = http.get('http://127.0.0.1:8000/auth/profile', {
    headers: {
      accept: 'application/json',
      'Cookie': `refresh_token=${refreshToken}`
    }
  });

  check(profileRes, {
    'profile success': (r) => r.status === 200,
    'has id': (r) => r.json('id') !== undefined,
    'has email': (r) => r.json('email') !== undefined,
    'has username': (r) => r.json('username') !== undefined,
  });

  sleep(0.1); // pause
}
