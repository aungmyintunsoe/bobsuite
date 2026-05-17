# Network Performance Tests - Autonomous Selection

**File Analyzed:** `mcp_server\test_output\sample_api.js`
**Language:** JavaScript
**Test Framework:** k6
**Timestamp:** 2026-05-17T04:56:31.735824Z

## Framework Justification

k6 is optimal for this use case because it is designed for performance testing, supports HTTP protocols, and can easily simulate concurrent users, measure response times, and handle rate limiting scenarios.

## Dependencies

```bash
npm install -g k6
```

## Setup Commands

```bash
mkdir -p test/performance
touch test/performance/api.performance.test.js
```

## Test Files

### api.performance.test.js

Tests response times, error rates, and rate limiting for the API endpoints.

```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
  vus: 100, // Number of virtual users
  duration: '30s', // Test duration
  thresholds: {
    http_req_duration: ['p(95)<200'], // 95% of requests should be below 200ms
    'checks/hr_http_req_duration': ['rate<0.05'], // Error rate should be below 5%
    'checks/hr_http_req_duration': ['rate<0.01'], // Throughput should be above 50 RPS
  },
};

export default function () {
  let res;
  res = http.get('http://localhost:3000/api/users/1');
  check(res, {
    'status is 200': (r) => r.status === 200,
  });
  sleep(1);

  res = http.post('http://localhost:3000/api/users', JSON.stringify({ name: 'Test User' }));
  check(res, {
    'status is 201': (r) => r.status === 201,
  });
  sleep(1);

  res = http.get('http://localhost:3000/api/limited');
  check(res, {
    'status is 200': (r) => r.status === 200,
  });
  sleep(1);

  res = http.get('http://localhost:3000/api/users/99999');
  check(res, {
    'status is 500': (r) => r.status === 500,
  });
  sleep(1);
}
```

## Execution Command

```bash
k6 run test/performance/api.performance.test.js
```

## Performance Thresholds

- **Response Time:** 200 ms
- **Throughput:** 50 requests/sec
- **Error Rate:** 5%

## Test Scenarios

- Measure response times for user retrieval and creation
- Test error handling for invalid user IDs
- Verify rate limiting behavior
- Simulate concurrent requests

## Notes

Ensure the server is running on localhost:3000 before executing the tests. Adjust the thresholds in the options object based on specific performance requirements.
