response=$(curl -s https://jd6t3c006e.execute-api.eu-west-1.amazonaws.com/prod/user/captcha)
captcha_id=$(echo "$response" | jq -r .captcha_id)
echo "$response" | jq -r .image_base64 | base64 -d > captcha.png

echo "Captcha ID is: $captcha_id"
echo "Image saved to captcha.png"
