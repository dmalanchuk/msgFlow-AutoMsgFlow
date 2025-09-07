import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
  vus: 1,         // кількість одночасних користувачів
  duration: '60s' // час тесту
};

export default function () {
  let randomNum = Math.floor(Math.random() * 1000000);
  let payload = JSON.stringify({
    email: `daniil.marysyk@gmail.com`,
    username: `daniil`,
    password: 'qwe123qwe'
  });

  let params = {
    headers: {
      'Content-Type': 'application/json',
      'accept': 'application/json'
    }
  };

  let res = http.post('http://127.0.0.1:8000/auth/register', payload, params);

  check(res, {
    'status 201': (r) => r.status === 201
  });

  sleep(0.1); // невелика пауза між запитами
}
