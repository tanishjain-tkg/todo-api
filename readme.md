# Todo API

A full stack Todo application built with FastAPI, SQLModel, and vanilla JavaScript.

## Tech Stack

**Backend**
- FastAPI
- SQLModel
- SQLite
- JWT Authentication

**Frontend**
- HTML, CSS, JavaScript (vanilla)

## Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/todo-api.git
cd todo-api
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/Scripts/activate
```

### 3. Install dependencies
```bash
pip install fastapi uvicorn sqlmodel python-dotenv python-jose[cryptography] passlib[bcrypt]==4.0.1 python-multipart
```

### 4. Set up environment variables
```bash
cp .env.example .env
```
Edit `.env` with your values.

### 5. Run the server
```bash
uvicorn app.main:app --reload
```

API will be running at `http://127.0.0.1:8000`
Interactive docs at `http://127.0.0.1:8000/docs`

## API Endpoints

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| POST | /auth/register | Register a new user | No |
| POST | /auth/login | Login and get token | No |
| GET | /todos | Get all your todos | Yes |
| POST | /todos | Create a todo | Yes |
| PUT | /todos/{id} | Update a todo | Yes |
| DELETE | /todos/{id} | Delete a todo | Yes |