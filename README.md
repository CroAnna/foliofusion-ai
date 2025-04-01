# FolioFusion AI server

This is an AI server for the FolioFusion web app.

Built using FastAPI & Groq with Python 3.12.3.

[![My Skills](https://go-skill-icons.vercel.app/api/icons?i=python,fastapi,groq)](https://skillicons.dev)

## How to start?

### 1. Prerequisites

A valid Groq API key.

### 2. Clone the repository

```
git clone https://github.com/yourusername/foliofusion-ai.git
cd foliofusion-ai
```

### 3. Create a virtual environment and activate it.

```
python -m venv venv
source venv/bin/activate
```

### 4. Install dependencies

```
pip install -r requirements.txt
```

### 5. Start the server on port 8000

```
uvicorn app.main:app --reload
```

documentation is available on `http://127.0.0.1:8000/docs`