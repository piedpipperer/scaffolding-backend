const API_BASE = "http://localhost:8000"; // adjust to your FastAPI URL

function showOutput(data) {
  document.getElementById("output").textContent = JSON.stringify(data, null, 2);
}

async function registerUser() {
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  const res = await fetch(`${API_BASE}/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      name: email.split("@")[0],
      email,
      password,
      captcha_id: "dummy",
      captcha_answer: "dummy"
    })
  });

  showOutput(await res.json());
}

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
  const res = await fetch(`${API_BASE}/auth/google`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ credential: response.credential })
  });
  showOutput(await res.json());
};
