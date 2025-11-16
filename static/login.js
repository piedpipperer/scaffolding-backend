import { updateUIForLoggedIn } from './ui.js';

const API_BASE_URL = "https://jd6t3c006e.execute-api.eu-west-1.amazonaws.com/prod";

export async function handleLogin(event) {
    event.preventDefault();
    const loginForm = event.target;
    const formData = new FormData(loginForm);
    const email = formData.get("email");
    const password = formData.get("password");

    const data = {
        email,
        password,
    };

    try {
        const response = await fetch(`${API_BASE_URL}/user/login`, {
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
        localStorage.setItem('accessToken', result.access_token);
        localStorage.setItem('username', result.user.name);
        localStorage.setItem('provider', result.user.provider);
        updateUIForLoggedIn(result.user.name);
    } catch (error) {
        console.error('Error:', error);
        alert(`Login failed: ${error.message}`);
    }
}
