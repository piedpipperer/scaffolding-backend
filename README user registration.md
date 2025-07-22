You can test the API using `curl`:

 curl -i -X OPTIONS "http://127.0.0.1:8000/user/register"      -H "Origin: http://localhost:8000"      -H "Access-Control-Request-Method: POST"      -H "Access-Control-Request-Headers: Authorization, Content-Type"
 -H 'accept: text/html'


  ```bash
  curl  -X 'POST' \
    'http://127.0.0.1:8000/user/register' \
  -H 'Content-Type: application/json' \
  -d '{ "name": "jordi", "password": "1234321" }'
```
