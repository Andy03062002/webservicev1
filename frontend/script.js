// URL base del backend (ajusta si usas otro puerto)
const API_URL = "http://127.0.0.1:8000";

// REGISTRO
const registerForm = document.getElementById("registerForm");
if (registerForm) {
    registerForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        const data = {
            nombre: document.getElementById("nombre").value,
            correo: document.getElementById("correo").value,
            password: document.getElementById("password").value
        };

        const res = await fetch(`${API_URL}/register`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });

        const result = await res.json();
        alert(result.message || "Registro exitoso");
        if (res.ok) window.location.href = "login.html";
    });
}

// LOGIN
const loginForm = document.getElementById("loginForm");
if (loginForm) {
    loginForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        const data = {
            correo: document.getElementById("correo").value,
            password: document.getElementById("password").value
        };

        const res = await fetch(`${API_URL}/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });

        const result = await res.json();
        if (res.ok) {
            alert("Inicio de sesión exitoso");
            localStorage.setItem("usuario", JSON.stringify(result));
            window.location.href = "dashboard.html"; // Página principal luego del login
        } else {
            alert(result.detail || "Credenciales incorrectas");
        }
    });
}
