You can test the API using `curl`:

 curl -i -X OPTIONS "http://127.0.0.1:8000/user/register"      -H "Origin: http://localhost:8000"      -H "Access-Control-Request-Method: POST"      -H "Access-Control-Request-Headers: Authorization, Content-Type"
 -H 'accept: text/html'

(local)
 curl -i -X OPTIONS "https://jd6t3c006e.execute-api.eu-west-1.amazonaws.com/prod/user/register"      -H "Origin: http://localhost:8000"      -H "Access-Control-Request-Method: POST"      -H "Access-Control-Request-Headers: Authorization, Content-Type"  -H 'accept: text/html'




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

aws ec2 describe-network-interfaces \
  --filters "Name=description,Values=*relappmidos2*" \
  --query "NetworkInterfaces[*].{ENI:NetworkInterfaceId,Subnet:SubnetId,PrivateIp:PrivateIpAddress,Status:Status}" \
  --profile jrojo


# enabl logs in api gateway:
aws logs create-log-group \
  --log-group-name /aws/apigateway/relappmidos-prod \
  --profile jrojo

aws apigatewayv2 update-stage \
  --api-id d63ojp7jad \
  --stage-name prod \
  --access-log-settings '{
      "DestinationArn": "arn:aws:logs:eu-west-1:617961504899:log-group:/aws/apigateway/relappmidos-prod",
      "Format": "$context.requestId $context.httpMethod $context.path $context.status $context.error.message"
  }' \
  --profile jrojo

aws apigatewayv2 update-stage \
  --api-id d63ojp7jad \
  --stage-name prod \
  --access-log-settings '{
    "DestinationArn": "arn:aws:logs:eu-west-1:617961504899:log-group:/aws/apigateway/relappmidos-prod",
    "Format": "{\"requestId\":\"$context.requestId\",\"ip\":\"$context.identity.sourceIp\",\"httpMethod\":\"$context.httpMethod\",\"routeKey\":\"$context.routeKey\",\"path\":\"$context.path\",\"status\":\"$context.status\",\"integrationError\":\"$context.integrationErrorMessage\",\"error\":\"$context.error.message\",\"errorResponseType\":\"$context.error.responseType\"}"
  }' \
  --profile jrojo


# very important thing for the google auth internet:
aws ec2 authorize-security-group-ingress \
  --group-id sg-17995864 \
  --protocol tcp \
  --port 0-65535 \
  --source-group sg-17995864 \
  --profile jrojo

# add permission
aws lambda add-permission \
  --function-name relappmidos2 \
  --statement-id apigateway-prod \
  --action lambda:InvokeFunction \
  --principal apigateway.amazonaws.com \
  --source-arn "arn:aws:execute-api:eu-west-1:617961504899:7klega2ek2/prod/*/*" \
  --profile jrojo

  aws iam attach-role-policy \
  --role-name persones_endpoint-role-ev4upc5k \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole \
  --profile jrojo


# check the api gateway integration:
aws apigateway get-method \
  --rest-api-id 7klega2ek2 \
  --resource-id 9lpenbdzzf \
  --http-method  user/captcha \
  --profile jrojo

# for the captcha!

curl -i -X OPTIONS  

user/captcha   -H "Origin: http://localhost:5501"      -H "Access-Control-Request-Method: GET"      -H "Access-Control-Request-Headers: Authorization, Content-Type"
 -H 'accept: text/html'


curl -s https://jd6t3c006e.execute-api.eu-west-1.amazonaws.com/prod/user/captcha | jq -r .image_base64 | base64 -d > captcha.png  -D headers.txt

# get headers to capture captcha id:
cat headers.txt | grep X-captcha-ID

  52eb2b0f-8431-49a2-ab13-698b3eae2021

same with image: captcha.png -> 7479


# CURL THE USER CREATION
curl -X POST https://jd6t3c006e.execute-api.eu-west-1.amazonaws.com/prod/user/register \
  -H "Content-Type: application/json" \
  -d '{
        "name": "dsgsadga",
        "password": "#2ldsKjañsajf1234",
        "email": "test3@hotmail.com",
        "captcha_id": "808555c1-b34a-402a-8342-1ebbed713fb1",
        "captcha_answer": "8253"
      }'


Google authentication forced us to employ env variables, we configured t hem in the aws lambda manualy.



# now we also login, only if we have not registered:
curl -X POST  https://jd6t3c006e.execute-api.eu-west-1.amazonaws.com/prod/user/login \
  -H "Content-Type: application/json" \
  -d '{
        "email": "test@hotmail.com",
        "password": "#2ldskjañsajf1234",
        "captcha_id": "55677fc7-2f72-4ed6-b017-e68ffeab1703",
        "captcha_answer": "0757"
      }'


after login/registering, we will get a token, to which we can continue using the user/users endpoint:


# former way of getting:
  curl -X GET "http://127.0.0.1:8000/user/former_users"  \
  -u "jobbedgasdgad@gmail.com:shfshs" \
  -H "Origin: http://localhost:8000"  \
  -H "Content-Type: application/json"

# authorization bearer:
  curl -X GET \
  https://jd6t3c006e.execute-api.eu-west-1.amazonaws.com/prod/user/users \
  -H "Origin: http://localhost:8000"  \
  -H "accept: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2OTQiLCJlbWFpbCI6InRlc3QyQGhvdG1haWwuY29tIiwibmFtZSI6ImRzZ3NhZGdhIiwiZXhwIjoxNzYyNzcxNjg3fQ.A5rw70QBck0uqrX0sLlOrHom6eJBhk22R9jhJOABq8k"


# authorization bearer got from google:
  curl -X GET \
  http://127.0.0.1:8000/user/users \
  -H "Origin: http://localhost:8000"  \
  -H "accept: application/json" \
  -H "Authorization: Bearer gdagagadg"


# now we also login, only if we have not registered:
curl -X POST https://jd6t3c006e.execute-api.eu-west-1.amazonaws.com/prod/user/login \
  -H "Content-Type: application/json" \
  -d '{
        "password": "#2ldsKjañsajf1234",
        "email": "test3@hotmail.com",
        "captcha_id": "a26bad8a-8a7c-4a79-9527-b7c24a4867b2",
        "captcha_answer": "4029"
      }'


# options
 curl -i -X OPTIONS "https://jd6t3c006e.execute-api.eu-west-1.amazonaws.com/prod/user/login"      -H "Origin: http://localhost:8000"      -H "Access-Control-Request-Method: POST"      -H "Access-Control-Request-Headers: Authorization, Content-Type"
 -H 'accept: text/html'



# now we also login, only if we have not registered:
curl -X POST https://jd6t3c006e.execute-api.eu-west-1.amazonaws.com/prod/user/login \
  -H "Content-Type: application/json" \
  -d '{
        "email": "test@test.com",
        "password": "1234"

      }'



## google

 curl -i -X OPTIONS "https://jd6t3c006e.execute-api.eu-west-1.amazonaws.com/prod/google/auth"      -H "Origin: http://localhost:8000"      -H "Access-Control-Request-Method: POST"      -H "Access-Control-Request-Headers: Authorization, Content-Type"
 -H 'accept: text/html'


curl -X POST https://jd6t3c006e.execute-api.eu-west-1.amazonaws.com/prod/google/auth \
  -H "Content-Type: application/json" \
  -d '{
        "credential": "test"
      }'
