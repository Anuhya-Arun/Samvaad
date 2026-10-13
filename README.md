# Samvaad — Sanskrit Learning Chatbot

**Samvaad (संवाद)** is a rule-based chatbot designed to help users explore Sanskrit through interactive conversations. It provides bilingual responses in Sanskrit and English, supports free-text questions, and suggests follow-up questions to encourage continued learning.

## Features

- Bilingual Sanskrit and English responses
- Rule-based response generation using Python
- Interactive chat interface
- Suggested questions and contextual follow-ups
- Sanskrit vocabulary and phrase assistance
- Responsive frontend with a Sanskrit-inspired design
- REST API built with Flask
- Automated build and testing through Jenkins CI/CD

## Technology Stack

| Component | Technology |
|---|---|
| Frontend | React, Vite, CSS |
| Backend | Python, Flask |
| API communication | HTTP and JSON |
| Cross-origin requests | Flask-CORS |
| Version control | Git and GitHub |
| CI/CD | Jenkins |

## Project Structure

```text
Samvaad/
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.css
│   │   └── main.jsx
│   └── package.json
├── backend/
│   ├── app.py
│   ├── chatbot.py
│   └── requirements.txt
├── .gitignore
├── README.md
└── Jenkinsfile
```

*The Jenkinsfile will be added when the CI/CD pipeline is configured.*

## Prerequisites

- Python 3
- Node.js and npm
- Git

## Running the Application

### 1. Start the backend

Open a terminal in the project root:

```bash
cd backend
python -m venv .venv
```

Activate the virtual environment on Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies and start Flask:

```bash
pip install -r requirements.txt
python app.py
```

The backend runs at `http://127.0.0.1:5000`.

### 2. Start the frontend

Open a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the local URL displayed by Vite in your terminal.

## How It Works

1. The user enters a question through the React interface.
2. The frontend sends the message to the Flask API.
3. The Python chatbot matches the input against its predefined rules and vocabulary.
4. The backend returns the response in JSON format.
5. The frontend displays the Sanskrit and English responses with suggested follow-up questions.

## CI/CD

Jenkins will be configured to retrieve the source code from GitHub, install the required dependencies, and run automated checks whenever changes are submitted.

## Project Scope

Samvaad is an educational, rule-based chatbot. It does not rely on external generative AI APIs. Its responses depend on the rules, phrases, and vocabulary implemented in the application.
