import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
  vus: 100,         // кількість одночасних користувачів
  duration: '20s' // час тесту
};


const users = 1000;

export default function () {
    let i = Math.floor(Math.random() * users) + 1;

    let payload = JSON.stringify({
    email: `user${i}@example.com`,
    password: '111pass111'
  });


  let params = {
    headers: {
      'Content-Type': 'application/json',
      'accept': 'application/json'
    }
  };

  let res = http.post('http://127.0.0.1:8000/auth/login', payload, params);

  check(res, {
    'status 200': (r) => r.status === 200
  });

  sleep(0.1); // невелика пауза між запитами
}