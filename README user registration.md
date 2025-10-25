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
        "email": "your_email@hotmail.com",
        "captcha_id": "fa094ddd-d13d-40e6-97f3-c41506a76adc",
        "captcha_answer": "6985"
      }'


Google authentication forced us to employ env variables, we configured t hem in the aws lambda manualy.



# now we also login, only if we have not registered:
curl -X POST http://127.0.0.1:8000/user/login \
  -H "Content-Type: application/json" \
  -d '{
        "email": "jobbedgasdgad@gmail.com",
        "password": "hfdshsh"
      }'


after login/registering, we will get a token, to which we can continue using the user/users endpoint:


# former way of getting:
  curl -X GET "http://127.0.0.1:8000/user/former_users"  \
  -u "jobbedgasdgad@gmail.com:shfshs" \
  -H "Origin: http://localhost:8000"  \
  -H "Content-Type: application/json"

# authorization bearer:
  curl -X GET \
  http://127.0.0.1:8000/user/users \
  -H "Origin: http://localhost:8000"  \
  -H "accept: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI4IiwiZW1haWwiOiJqb2JiaW5nLjMxNEBnbWFpbC5jb20iLCJuYW1lIjoiam9yZGkiLCJleHAiOjE3NjA5ODA3MDB9.PeBZqluB1hemx_Qjsdu21enCxwoFYZWfPedGnyhVEQ4"


# authorization bearer got from google:
  curl -X GET \
  http://127.0.0.1:8000/user/users \
  -H "Origin: http://localhost:8000"  \
  -H "accept: application/json" \
  -H "Authorization: Bearer gdagagadg"
