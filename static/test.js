// const API_BASE = "http://localhost:8000"; // adjust to your FastAPI URL

const API_BASE_URL = "https://d8ml27eov6.execute-api.eu-west-1.amazonaws.com/prod";

export async function fetchAndDisplayCaptcha(captchaImage) {
    try {
        const response = await fetch(`${API_BASE_URL}/user/captcha`);
        if (!response.ok) {
            throw new Error(`Failed to fetch captcha: ${response.statusText}`);
        }
        const data = await response.json();

        captchaImage.src = `data:image/png;base64,${data.image_base64}`;
        captchaImage.alt = "CAPTCHA Image";
        return data.captcha_id;
    } catch (error) {
        console.error("Error fetching CAPTCHA:", error);
        captchaImage.alt = "Failed to load CAPTCHA. Please refresh.";
        return null;
    }
}

export async function handleRegistration(event, captchaId) {
    event.preventDefault();
    const registerForm = event.target;
    const formData = new FormData(registerForm);
    const name = formData.get("name");
    const email = formData.get("email");
    const password = formData.get("password");
    const captchaAnswer = formData.get("captcha_answer");

    const data = {
        name,
        email,
        password,
        captcha_id: captchaId,
        captcha_answer: captchaAnswer
    };

    try {
        const response = await fetch(`${API_BASE_URL}/user/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        console.log('Success:', result);
        alert('Registration successful!');
        // Redirect or update UI
    } catch (error) {
        console.error('Error:', error);
        alert(`Registration failed: ${error.message}`);
    }
}
