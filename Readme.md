# Forwardly

Forwardly is a FastAPI-based web application that helps students and professionals evaluate how well their resume matches a specific job description.

It generates realistic, constructive, and encouraging analysis using LLMs — helping users improve their resume and prepare better before applying.


## 🚀 Live Demo

Deployed on Railway.

https://forwardly-production-d959.up.railway.app/


## 🧠 What Forwardly Does

Forwardly helps you:

- Upload and manage resumes
- Add job descriptions you’re targeting
- Generate AI-powered resume ↔ job match analysis
- Understand strengths and gaps
- Get constructive and encouraging feedback
- Identify what skills or experience to improve before applying

It is designed for individuals — not recruiters or bulk evaluation.


## 🧠 How It Helps You

Forwardly focuses on:

- Realistic but supportive feedback
- Clear skill gap identification
- Practical improvement suggestions
- Structured analysis output (not vague paragraphs)

The goal is simple:  
**Help you apply more confidently and more strategically.**


## 🎯 Target Users

- Students preparing for internships
- Early-career professionals
- Engineers switching domains
- Anyone who wants structured resume feedback before applying


## 🔁 Application Flow

1. User uploads resume
2. Resume is stored in database
3. Resume is parsed
4. User creates or selects a job description 
5. AI generates structured analysis
6. Analysis is rendered in UI


## 🌱 Planned Enhancements

Future iterations may include:

- 1-week preparation roadmap for a specific role
- Resume improvement recommendations
- AI-generated tailored resume version
- Skill-building guidance
- User accounts and saved history
- Tracking applications and resumes



# 🏗️ Technical Overview

Forwardly is built as a cleanly layered FastAPI application.

## Architecture

Forwardly follows a modular, domain-based architecture inspired by Django-style applications.

Each core feature is organized as an independent module with its own:

- router
- services
- models
- schemas

This keeps responsibilities grouped by domain instead of technical layer.

## 📁 Project Structure


```
app/
│
├── main.py
│
├── resumes/
│   ├── router.py
│   ├── services.py
│   ├── models.py
│   └── schemas.py
│
├── job_descriptions/
│   ├── router.py
│   ├── services.py
│   ├── models.py
│   └── schemas.py
│
├── analysis/
│   ├── router.py
│   ├── services.py
│   ├── models.py
│   └── schemas.py
│
└── webui/
    ├── router.py
    └── templates/
        ├── base.html
        ├── resumes.html
        └── analysis.html
```

## ⚙️ Tech Stack

- **Backend:** FastAPI
- **Database:** SQLite
- **ORM:** SQLModel
- **Templating:** Jinja2
- **AI Integration:** OpenAI Python SDK (Responses API)
- **Frontend:** HTML + Bootstrap + Vanilla JavaScript (AJAX)
- **Deployment:** Railway


## 📊 Database Design

Core tables:

- `Resume`
- `JobDescription`
- `Analysis`

List endpoints use selective column queries to avoid loading heavy text fields unnecessarily.


## 🧠 AI Integration

- Uses OpenAI Responses API
- Structured output via Pydantic models
- Deterministic analysis format
- Encouraging but realistic tone


## 🔁 Application Flow

1. User uploads resume
2. Resume is stored in database
3. Resume is parsed
4. User selects job description
5. AI generates structured analysis
6. Analysis is rendered in UI


## 💻 Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/forwardly.git
cd forwardly
```

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate      # Mac/Linux
venv\Scripts\activate         # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set environment variables

Create a `.env` file:

```
OPENAI_API_KEY=your_openai_key_here
```

### 5. Run the application

```bash
uvicorn app.main:app --reload
```

Visit:

```
http://127.0.0.1:8000
```


## 🚂 Deployment

Deployed using Railway:

1. Connect GitHub repository
2. Configure environment variables
3. Automatic build & deployment

Note: If using ephemeral storage, uploaded files may reset on redeploy.


## 📄 License

MIT License