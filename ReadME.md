# 🔍 Multi-Agent Research Assistant

An AI-powered research platform that leverages multiple specialized agents to generate high-quality research reports from user queries. The system combines web search, agent collaboration, critique, and report generation into a single workflow.

## 🚀 Features

- 🔐 JWT Authentication
- 🤖 Multi-Agent Architecture
- 🌐 Real-time Web Research using Tavily
- 📝 Automated Report Generation
- 🎯 Research Validation & Critique
- 📊 Report History Dashboard
- 💾 Database Persistence
- 📄 PDF Export Support
- ⚡ FastAPI Backend
- 🎨 Streamlit Frontend

---

## 🏗️ System Architecture

```text
User Query
     │
     ▼
Coordinator Agent
     │
     ├─────────────► Research Agent
     │                    │
     │                    ▼
     │              Tavily Search
     │                    │
     ▼                    ▼
Critic Agent ◄──── Research Results
     │
     ▼
Writer Agent
     │
     ▼
Summarizer Agent
     │
     ▼
Final Research Report
```

---

## 🧠 Agent Responsibilities

### Coordinator Agent
- Manages workflow execution
- Delegates tasks to specialized agents
- Combines outputs into a final report

### Research Agent
- Searches the web using Tavily
- Collects relevant information
- Extracts key insights from sources

### Critic Agent
- Reviews research quality
- Detects missing information
- Suggests improvements

### Writer Agent
- Creates structured research reports
- Organizes findings professionally
- Maintains clarity and coherence

### Summarizer Agent
- Generates concise summaries
- Highlights key takeaways
- Produces executive overviews

---

## 🛠️ Tech Stack

### Backend
- FastAPI
- SQLAlchemy
- JWT Authentication
- SQLite / PostgreSQL

### AI Layer
- OpenAI GPT Models
- Tavily Search API

### Frontend
- Streamlit

### Database
- SQLite
- PostgreSQL (Optional)

---

## 📂 Project Structure

```bash
Multi-Agent-Research-Assistant/
│
├── agents/
│   ├── coordinator_agent.py
│   ├── research_agent.py
│   ├── critic_agent.py
│   ├── writer_agent.py
│   ├── summarizer_agent.py
│   └── llm.py
│
├── backend/
│   ├── routes/
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── main.py
│
├── frontend/
│   ├── pages/
│   └── app.py
│
├── requirements.txt
├── app.py
└── README.md
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/madhavzer0oo0/Multi-Agent-Research-Assistant.git

cd Multi-Agent-Research-Assistant
```

### Create Virtual Environment

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the root directory:

```env
OPENAI_API_KEY=your_openai_key

TAVILY_API_KEY=your_tavily_key

SECRET_KEY=your_secret_key

DATABASE_URL=sqlite:///research.db
```

---

## ▶️ Running the Application

### Start Backend

```bash
uvicorn backend.main:app --reload
```

Backend:

```text
http://localhost:8000
```

Swagger Docs:

```text
http://localhost:8000/docs
```

---

### Start Frontend

```bash
streamlit run frontend/app.py
```

Frontend:

```text
http://localhost:8501
```

---


## 🔄 Research Workflow

1. User submits a research topic.
2. Coordinator Agent initiates workflow.
3. Research Agent searches the web using Tavily.
4. Critic Agent reviews gathered information.
5. Writer Agent generates a detailed report.
6. Summarizer Agent creates an executive summary.
7. Final report is stored and displayed.

---

## 📈 Future Improvements

- RAG with PDF Uploads
- Vector Database Integration
- Semantic Search
- Streaming Agent Responses
- LangGraph Workflow Visualization
- Multi-modal Research (PDFs, Images, Videos)
- Docker Deployment
- CI/CD Pipeline

---

## 🎯 Why This Project?

This project demonstrates:

- Multi-Agent AI Systems
- LLM Orchestration
- FastAPI Development
- Authentication & Authorization
- Database Design
- Tool Calling
- Web Search Integration
- Full-Stack AI Development

---

## 👨‍💻 Author

**Madhav Dembla**

- GitHub: https://github.com/madhavzer0oo0
---

## ⭐ Support

If you found this project useful, consider giving it a star on GitHub!
