# Project Plan: EasyQuery

## 1. Project Overview

EasyQuery will be a user-friendly application that enables users to interact with their databases using natural language, through both text and speech. The core of the project is to leverage a Large Language Model (LLM) to translate these natural language queries into SQL, execute them, and return the results. The application will feature a simple web-based UI, a robust FastAPI backend, and will be containerized with Docker for easy deployment and scalability.

## 2. Core Features & Implementation Details

### 2.1. Natural Language & Speech Interface

- **Text Input**: A chat-style interface in the UI for users to type their database queries in plain English.
- **Speech Input**:
  - The UI will include controls to record the user's voice.
  - We will use the `speech_recognition` library in the backend to convert the captured audio into text.

### 2.2. Database Connection Management

- **Secure Connection**: The UI will provide a form for users to enter connection details for their local or remote databases (e.g., host, port, username, password, database name). These credentials will be securely handled by the backend.
- **DB Compatibility**: We will start by supporting popular relational databases like PostgreSQL, MySQL, and SQLite.
- **Robust Handling**: The backend will use a library like SQLAlchemy to abstract database connections, manage connection pooling, and handle different SQL dialects.

### 2.3. LLM-Powered SQL Generation

- **LLM Integration**: The backend will integrate with an LLM (e.g., via OpenAI's API or a self-hosted model) to perform the natural-language-to-SQL translation.
- **Context-Aware Prompts**: To improve accuracy, the backend will first fetch the database schema and include it in the prompt sent to the LLM. This gives the model the necessary context about tables, columns, and relationships.
- **Query Execution & Visualization**: The LLM-generated SQL query will be executed against the user's database. The results will be fetched and displayed in a clean, tabular format in the UI.
concurrecy management, robust db handler engine

### 2.4. Backend (FastAPI)

- **API Endpoints**:
  - `POST /api/connect`: To establish and test a database connection.
  - `POST /api/query`: To process a text-based natural language query.
  - `POST /api/speech-query`: To process an audio file, convert it to text, and then to SQL.
  - `GET /api/schema`: To retrieve the schema of the currently connected database.
- **Technology Stack**:
  - Python 3.10+
  - FastAPI
  - SQLAlchemy
  - `speech_recognition`
  - `uvicorn` (as the ASGI server)

### 2.5. Frontend (HTML/CSS/JS)

- **Simple & Intuitive UI**: A single-page application with:
  - A database connection modal/form.
  - A main view with a chat interface for queries and a display area for results.
  - Microphone button for speech input.
- **Technology Stack**:
  - Vanilla HTML5, CSS3, and JavaScript.
  - No complex frameworks are necessary to keep it lightweight.
  - JavaScript's `fetch` API for communicating with the backend.

## 3. Architecture & Deployment

### 3.1. Dockerization

- **`backend/Dockerfile`**: A Dockerfile to create an image for the FastAPI application. It will copy the source code and install Python dependencies.
- **`frontend/Dockerfile`**: A Dockerfile that uses a lightweight Nginx image to serve the static frontend files (HTML, CSS, JS).
- **`docker-compose.yml`**: A Docker Compose file to define and orchestrate the `backend` and `frontend` services. This will simplify local development and deployment.

### 3.2. Nginx as a Reverse Proxy

- The Nginx container (running the frontend) will be configured to act as a reverse proxy. All requests to `/api/*` will be forwarded to the FastAPI backend service. This setup avoids Cross-Origin Resource Sharing (CORS) issues and streamlines the architecture.

## 4. Documentation

- **`README.md`**: A comprehensive README file will be created with:
  - A detailed project description.
  - Instructions on how to set up and run the project locally using Docker Compose.
  - API documentation for the backend endpoints.
  - An explanation of the project's architecture.
- **Inline Documentation**: Code will be well-commented to ensure clarity and maintainability.

## 5. Project Structure

A clear and organized directory structure will be maintained:

```
EasyQuery/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py         # FastAPI app definition
│   │   ├── models.py       # Pydantic models
│   │   └── services.py     # Business logic (DB connection, LLM calls)
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   ├── style.css
│   ├── script.js
│   ├── Dockerfile
│   └── nginx.conf
├── .dockerignore
├── .gitignore
├── docker-compose.yml
├── LICENSE
├── plan.md
└── README.md
```
