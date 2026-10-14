import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '1m', target: 50 },   // naik
    { duration: '2m', target: 50 },   // bertahan
    { duration: '30s', target: 0 },   // turun
  ],
  thresholds: {
    http_req_duration: ['p(95)<3000'], // p95 < 3 detik
    http_req_failed: ['rate<0.01'],    // galat < 1%
  },
};

const BASE = 'http://localhost:5000';

export default function () {
  const res = http.get(`${BASE}/api/mahasiswa/M001/krs`, {
    headers: { Authorization: 'Bearer token-m001' },
  });
  check(res, { 'status 200': (r) => r.status === 200 });
  sleep(1);
}
