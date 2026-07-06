# 🐾 FurSure — AI-Powered Pet Insurance Backend

> An enterprise-style Pet Insurance Management System built with **FastAPI**, featuring AI-assisted insurance claim review using **LangChain**, **LangGraph**, **Retrieval-Augmented Generation (RAG)**, and **ChromaDB**.

---

# 📖 Overview

FurSure is a backend application that enables users to purchase pet insurance, manage policies, submit claims, upload supporting documents, and receive AI-generated claim recommendations before human review.

The project combines modern backend engineering practices with LLM-powered workflows to automate insurance claim analysis while keeping humans in the approval loop for uncertain cases.

---

# ✨ Features

## 🔐 Authentication

* JWT Authentication
* Google OAuth Login
* Role-Based Access Control (RBAC)

## 🐶 Pet Insurance

* Dog Insurance Plans
* Cat Insurance Plans
* Insurance Applications
* Policy Management

## 📋 Claim Management

* Submit Insurance Claims
* AI-Powered Claim Review
* Human Review Routing
* Claim Status Tracking

## 🏥 Hospital Management

* Hospital Registration
* Hospital Management APIs

## 📁 File Management

* AWS S3 Integration
* Multipart File Uploads
* Secure Document Storage

## 💳 Payment

* Payment APIs
* Policy Activation Workflow

---

# 🤖 AI Claim Review Workflow

```text
               Claim Submitted
                      │
                      ▼
            Policy Retrieval Agent
                      │
                      ▼
          Retrieve Relevant Policy
               (ChromaDB + RAG)
                      │
                      ▼
               Review Agent (LLM)
                      │
      ┌───────────────┴───────────────┐
      │                               │
      ▼                               ▼
APPROVE / REJECT               REVIEW REQUIRED
                                      │
                                      ▼
                           Human Review Agent
```

---

# 🧠 LangGraph Multi-Agent System

The AI workflow is implemented using **LangGraph**, where multiple agents collaborate to review insurance claims.

### 📄 Policy Agent

* Retrieves relevant insurance policy sections from ChromaDB.
* Performs semantic search using vector embeddings.

### 🧠 Review Agent

* Uses policy context and LLMs to analyze claims.
* Generates:

  * Recommendation
  * Reason
  * Policy Section

### 👨‍💼 Human Review Agent

* Automatically receives claims requiring manual verification.
* Keeps humans involved in uncertain decisions.

---

# 🏗 System Architecture

```text
                 Frontend
                     │
                     ▼
              FastAPI Backend
                     │
      ┌──────────────┼──────────────┐
      │              │              │
      ▼              ▼              ▼
 PostgreSQL      AWS S3        ChromaDB
      │                             │
      └──────────────┬──────────────┘
                     ▼
                 LangGraph
                     │
        ┌────────────┴────────────┐
        ▼                         ▼
 Policy Agent              Review Agent
                                   │
                                   ▼
                          Human Review Agent
```

---

# 🛠 Tech Stack

### Backend

* Python
* FastAPI
* SQLAlchemy
* Alembic

### Database

* PostgreSQL
* ChromaDB

### AI & LLM

* LangChain
* LangGraph
* Retrieval-Augmented Generation (RAG)
* Sentence Transformers
* Gemini / OpenRouter LLM

### Cloud

* AWS S3
* Docker
* Docker Compose

### Authentication

* JWT
* Google OAuth

### Tools

* Git
* Postman
* Swagger UI

---

# 📊 Key Highlights

* ✅ 20+ REST APIs
* ✅ AI-powered insurance claim review
* ✅ LangGraph Multi-Agent workflow
* ✅ Retrieval-Augmented Generation (RAG)
* ✅ ChromaDB semantic search
* ✅ PostgreSQL with SQLAlchemy ORM
* ✅ AWS S3 document storage
* ✅ Dockerized deployment
* ✅ Clean service-oriented architecture

---

# 🚀 Getting Started

Clone the repository

```bash
git clone https://github.com/<your-repository>.git
cd Group-project
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
uvicorn app.main:app --reload
```

Or using Docker

```bash
docker-compose up --build
```

---

# 📑 API Documentation

Swagger UI

```
http://localhost:8000/docs
```

---

# 🔮 Future Enhancements

* Email OTP Verification (AWS SES)
* Fraud Detection Engine
* Notification Service
* Admin Dashboard
* CI/CD Pipeline
* Monitoring & Logging

---

# 👥 Contributors

| Team Member       | Responsibility                                                           |
| ----------------- | ------------------------------------------------------------------------ |
| **Asif S Sheenu** | AI Claim Review, LangChain, LangGraph, RAG, ChromaDB, AWS S3 Integration |
| Team Members      | Authentication, Payments, Insurance, Hospital, Pet Management            |

---

# 📄 License

This project was developed for educational and portfolio purposes.
