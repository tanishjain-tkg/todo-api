const API = "http://127.0.0.1:8000"

// ─── Helpers ───────────────────────────────────────────

function getToken() {
    return localStorage.getItem("token")
}

function setToken(token) {
    localStorage.setItem("token", token)
}

function removeToken() {
    localStorage.removeItem("token")
}

function showMessage(elementId, message, isError = false) {
    const el = document.getElementById(elementId)
    el.textContent = message
    el.style.color = isError ? "#ff6b6b" : "#a855f7"
}

// ─── Auth UI Switchers ──────────────────────────────────

function showRegister() {
    document.getElementById("login-form").style.display = "none"
    document.getElementById("register-form").style.display = "block"
    document.getElementById("auth-message").textContent = ""
}

function showLogin() {
    document.getElementById("register-form").style.display = "none"
    document.getElementById("login-form").style.display = "block"
    document.getElementById("auth-message").textContent = ""
}

function showTodos() {
    document.getElementById("auth-container").style.display = "none"
    document.getElementById("todo-container").style.display = "block"
    loadTodos()
}

function showAuth() {
    document.getElementById("todo-container").style.display = "none"
    document.getElementById("auth-container").style.display = "block"
}

// ─── Auth Functions ─────────────────────────────────────

async function register() {
    const email = document.getElementById("register-email").value
    const password = document.getElementById("register-password").value

    if (!email || !password) {
        showMessage("auth-message", "Please fill in all fields", true)
        return
    }

    const response = await fetch(`${API}/auth/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
    })

    const data = await response.json()

    if (response.ok) {
        showMessage("auth-message", "Registered successfully. Please login.")
        showLogin()
    } else {
        showMessage("auth-message", data.detail, true)
    }
}

async function login() {
    const email = document.getElementById("login-email").value
    const password = document.getElementById("login-password").value

    if (!email || !password) {
        showMessage("auth-message", "Please fill in all fields", true)
        return
    }

    const formData = new FormData()
    formData.append("username", email)
    formData.append("password", password)

    const response = await fetch(`${API}/auth/login`, {
        method: "POST",
        body: formData
    })

    const data = await response.json()

    if (response.ok) {
        setToken(data.access_token)
        showTodos()
    } else {
        showMessage("auth-message", data.detail, true)
    }
}

function logout() {
    removeToken()
    showAuth()
}

// ─── Todo Functions ─────────────────────────────────────

async function loadTodos() {
    const response = await fetch(`${API}/todos`, {
        headers: { "Authorization": `Bearer ${getToken()}` }
    })

    const todos = await response.json()
    renderTodos(todos)
}

async function createTodo() {
    const title = document.getElementById("todo-title").value
    const description = document.getElementById("todo-description").value

    if (!title) {
        showMessage("todo-message", "Title is required", true)
        return
    }

    const response = await fetch(`${API}/todos`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${getToken()}`
        },
        body: JSON.stringify({ title, description, completed: false })
    })

    if (response.ok) {
        document.getElementById("todo-title").value = ""
        document.getElementById("todo-description").value = ""
        showMessage("todo-message", "Todo added!")
        loadTodos()
    } else {
        showMessage("todo-message", "Failed to create todo", true)
    }
}

async function toggleComplete(id, currentStatus) {
    const todo = await fetch(`${API}/todos/${id}`, {
        headers: { "Authorization": `Bearer ${getToken()}` }
    })
    const data = await todo.json()

    await fetch(`${API}/todos/${id}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${getToken()}`
        },
        body: JSON.stringify({ ...data, completed: !currentStatus })
    })

    loadTodos()
}

async function deleteTodo(id) {
    await fetch(`${API}/todos/${id}`, {
        method: "DELETE",
        headers: { "Authorization": `Bearer ${getToken()}` }
    })

    loadTodos()
}

// ─── Render Todos ───────────────────────────────────────

function renderTodos(todos) {
    const list = document.getElementById("todo-list")

    if (todos.length === 0) {
        list.innerHTML = `<p style="text-align:center; color:rgba(255,255,255,0.3); margin-top:40px;">No todos yet. Add one above!</p>`
        return
    }

    list.innerHTML = todos.map(todo => `
        <div class="todo-item ${todo.completed ? 'completed' : ''}">
            <div class="todo-content">
                <div class="todo-title">${todo.title}</div>
                ${todo.description ? `<div class="todo-description">${todo.description}</div>` : ""}
            </div>
            <div class="todo-actions">
                <button class="complete-btn" onclick="toggleComplete(${todo.id}, ${todo.completed})">
                    ${todo.completed ? "Undo" : "Done"}
                </button>
                <button class="delete-btn" onclick="deleteTodo(${todo.id})">
                    Delete
                </button>
            </div>
        </div>
    `).join("")
}

// ─── On Page Load ───────────────────────────────────────

window.onload = function () {
    if (getToken()) {
        showTodos()
    } else {
        showAuth()
    }
}