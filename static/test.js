const API_BASE = "http://localhost:8000"; // adjust to your FastAPI URL


const loadCaptcha = async () => {
    try {
        const response = await fetch(`${API_BASE}/user/captcha`);
        captchaId = response.headers.get("x-captcha-id");
        const blob = await response.blob();
        const captchaImage = document.getElementById("captchaImage");
        if (captchaImage.src && captchaImage.src.startsWith("blob:")) {
            URL.revokeObjectURL(captchaImage.src);
        }
        captchaImage.src = URL.createObjectURL(blob);
    } catch (error) {
        console.error("Error loading captcha:", error);
    }
}

loadCaptcha();

document.getElementById("registerForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const registrationData = {
        email: formData.get("email").trim().toLowerCase(),
        name: formData.get("username").trim().toLowerCase(),
        password: formData.get("password"),
        captcha_id: captchaId,
        captcha_answer: formData.get("captcha"),
    };
    try {
        const response = await fetch(`${API_BASE}/user/register`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(registrationData),
        });

        if (!response.ok) {
            let errorData;
            try {
                errorData = await response.json();
            } catch {
                errorData = {};
            }
            let alertMessage;
            if (response.status === 400) {
                if (errorData.detail) {
                    if (typeof errorData.detail === "string") {
                        alertMessage = errorData.detail;
                    }
                } else {
                    alertMessage = "Registration failed. Please check your input and try again.";
                }
            } else {
                alertMessage = "Something went wrong. Please try again later.";
            }
            alert(alertMessage);
            return;
        } else {
            alert("SUCCESS!");
        };
    } catch (error) {
        console.error('Network / Fetch error :', error);
        alert("Error -> check console");
    };
});

async function loginUser() {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const res = await fetch(`${API_BASE}/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
    });

    showOutput(await res.json());
}

// Google callback (must be global)
window.handleGoogleLogin = async (response) => {
    const res = await fetch(`${API_BASE}/google/auth`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ credential: response.credential })
    });
    showOutput(await res.json());
};
