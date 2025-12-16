const API_BASE_URL = "https://jd6t3c006e.execute-api.eu-west-1.amazonaws.com/prod";

export function updateUIForLoggedIn(username) {
    document.getElementById('registerForm').style.display = 'none';
    document.getElementById('loginForm').style.display = 'none';
    const googleSignInContainer = document.getElementById('google-signin-container');
    if (googleSignInContainer) {
        googleSignInContainer.style.display = 'none';
    }
    document.getElementById('login-status').innerText = `Logged in as: ${username}`;
    document.getElementById('logout-button').style.display = 'block';
    document.querySelector('button[onclick="fetchUsers()"]').style.display = 'block';
}

export function logout() {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('username');
    localStorage.removeItem('provider');
    document.getElementById('registerForm').style.display = 'block';
    const googleSignInContainer = document.getElementById('google-signin-container');
    if (googleSignInContainer) {
        googleSignInContainer.style.display = 'block';
    }
    document.getElementById('login-status').innerText = '';
    document.getElementById('logout-button').style.display = 'none';
    document.getElementById('user-profile').innerText = '';
    document.querySelector('button[onclick="fetchUsers()"]').style.display = 'none';
}


export async function fetchUsers() {
    const accessToken = localStorage.getItem('accessToken');
    if (!accessToken) {
        alert('You must be logged in to fetch users.');
        return;
    }

    try {
        const res = await fetch(`${API_BASE_URL}/user/users`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${accessToken}`
            }
        });

        if (!res.ok) {
            const errorData = await res.json();
            throw new Error(errorData.detail || `HTTP error! status: ${res.status}`);
        }

        const users = await res.json();
        const userProfileDiv = document.getElementById('user-profile');
        userProfileDiv.innerHTML = '<h3>Users:</h3><pre>' + JSON.stringify(users, null, 2) + '</pre>';
    } catch (error) {
        console.error('Error fetching users:', error);
        alert(`Failed to fetch users: ${error.message}`);
    }
}
