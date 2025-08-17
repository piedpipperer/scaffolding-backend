You can test the API using `curl`:

 curl -i -X OPTIONS "http://127.0.0.1:8000/user/register"      -H "Origin: http://localhost:8000"      -H "Access-Control-Request-Method: POST"      -H "Access-Control-Request-Headers: Authorization, Content-Type"
 -H 'accept: text/html'

(local)
 curl -i -X OPTIONS "https://d63ojp7jad.execute-api.eu-west-1.amazonaws.com/prod/user/register"      -H "Origin: http://localhost:8000"      -H "Access-Control-Request-Method: POST"      -H "Access-Control-Request-Headers: Authorization, Content-Type"  -H 'accept: text/html'


  ```bash
  curl  -X 'POST' \
    'http://127.0.0.1:8000/user/register' \
  -H 'Content-Type: application/json' \
  -d '{ "name": "jordi", "password": "1234321" }'
```


  curl  -X 'POST' \
    'http://127.0.0.1:8000/user/register' \
  -H 'Content-Type: application/json' \
  -d '{ "name": "jordi", "password": "1234321" }'
https://d63ojp7jad.execute-api.eu-west-1.amazonaws.com/prod

# for the captcha!

curl -i -X OPTIONS https://d63ojp7jad.execute-api.eu-west-1.amazonaws.com/prod/user/captcha   -H "Origin: http://localhost:8000"      -H "Access-Control-Request-Method: GET"      -H "Access-Control-Request-Headers: Authorization, Content-Type"
 -H 'accept: text/html'

curl -v -X GET http://127.0.0.1:8000/user/captcha \
  -o captcha.png \
  -D headers.txt


curl -v -X GET https://d63ojp7jad.execute-api.eu-west-1.amazonaws.com/prod/user/captcha \
  -o captcha.png \
  -D headers.txt

# get headers to capture captcha id:
cat headers.txt | grep X-captcha-ID

  52eb2b0f-8431-49a2-ab13-698b3eae2021

same with image: captcha.png -> 7479


# CURL THE USER CREATION
curl -X POST http://127.0.0.1:8000/user/register \
  -H "Content-Type: application/json" \
  -d '{
        "name": "helene",
        "password": "1234321",
        "captcha_id": "197b17b1-ed0c-48a3-9f3f-7c7181e961f7",
        "captcha_answer": "0506"
      }'
