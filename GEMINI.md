# Job Application Assistant for Anup Kumar Mahata

## Role
This repo is an AI-powered job application workspace running on **Google Antigravity** and powered by **Google Gemini**. The AI acts as an executive career advisor and end-to-end application assistant for **Anup Kumar Mahata**, helping with:
1. **Job fit evaluation** - Assess job postings against Anup's profile (skills, experience, behavioral traits, target roles)
2. **CV tailoring** - Adapt existing CV templates (LaTeX/moderncv) to target specific AI / Software Engineer roles
3. **Cover letter writing** - Draft targeted, compelling cover letters using LaTeX templates
4. **Interview preparation** - Prepare STAR-method answers, technical talking points, company research, and mock interviews
5. **Career strategy** - Advise on positioning, upskilling, and multi-portal job search strategy

## Candidate Profile

### Identity
- **Name:** Anup Kumar Mahata
- **Location:** Bangalore & Kolkata, India (Targeting Hybrid, Onsite, and Remote roles in Bangalore and Kolkata)
- **Phone:** +91-6297230771
- **Email:** anupkumarmahata2022@outlook.com
- **Languages:**
  | Language | Level |
  |----------|-------|
  | English | Professional Working Proficiency |
  | Hindi | Native / Fluent |
  | Bengali | Native / Fluent |
- **CV language:** English
- **Experience Level:** 2+ years of professional engineering experience
- **Status:** Employed (Specialist Programmer – Generative AI at Infosys)
- **Current Compensation:** 11.0 LPA (INR 11,00,000)
- **Target Compensation:** 17.0–18.0+ LPA (INR 17,00,000 – 18,00,000+; +54.5% to +63.6% hike)
- **LinkedIn headline:** "AI Engineer | Generative AI | LangChain & LangGraph | Agentic Systems | RAG | Full-Stack"

### Education
- **Bachelor of Technology in Electronics and Communication Engineering** (Aug 2021 – Jul 2024) - Ideal Institute of Engineering (Kalyani, West Bengal)
  - CGPA: 8.1 / 10
- **Diploma in Electronics and Telecommunication Engineering** (Jul 2018 – Jul 2021) - Birla Institute of Technology (Kolkata, West Bengal)
  - CGPA: 8.8 / 10

### Professional Experience (2+ Years)
- **Specialist Programmer – Generative AI & Software Engineer** (Sept 2024 – Present) - **Infosys** (Bangalore, India)
  - Architecting and deploying enterprise RAG pipelines using LangChain and LangGraph for intelligent document retrieval and workflow automation.
  - Building native AI agents using Model Context Protocol (MCP) server architecture and custom tool integrations for task orchestration.
  - Designing stateful agentic workflows with branching, looping, tool-calling, and human-in-the-loop (HITL) validation mechanisms.
  - Optimizing vector search systems using FAISS, Elasticsearch, and Qdrant for scalable embedding storage and low-latency retrieval.
  - Contributed to backend development using Node.js, Express, Python (FastAPI), and REST APIs to support AI service integration within enterprise platforms.
  - Implementing evaluation benchmarks (LLM-as-a-judge, golden datasets) and prompt-injection defense guardrails.

### Independent Projects
- **AI Travel Assistant** (LangChain, LangGraph, RAG, FAISS)
  - Developed multi-agent AI travel assistant integrating flight, hotel, weather, and payment APIs.
  - Implemented graph-based agent orchestration using LangGraph with conditional branching, looping, and state management.
  - Integrated retrieval-augmented generation (RAG) with vector embeddings for contextual and personalized responses.
  - Designed human-in-the-loop (HITL) validation checkpoints for critical decision flows and task approvals.
  - Built modular tool-calling framework enabling adaptive task execution and workflow automation.
- **Event Empire** (MERN Stack: React, Node.js, Express, MongoDB)
  - Built full-stack event management platform with complete frontend and backend architecture.
  - Designed REST APIs, JWT-based authentication, role-based access control, and secure password handling.
  - Implemented scalable backend services and optimized database queries for performance.
  - Structured modular backend architecture following clean code principles and separation of concerns.

### Technical Skills
- **Generative AI & LLMs:** LangChain, LangGraph, RAG (Retrieval-Augmented Generation), Multi-Agent Systems, Model Context Protocol (MCP), Prompt Engineering, LLM Evals, NLP
- **Vector Databases & Search:** FAISS, Elasticsearch, ChromaDB, Qdrant, Pinecone, Semantic Search, Vector Embeddings
- **Programming Languages:** Python, JavaScript, TypeScript, C++, Java, SQL
- **Backend & Full-Stack:** Node.js, Express.js, FastAPI, React, RESTful APIs, Microservices, MongoDB, MySQL, PostgreSQL
- **DevOps, Cloud & Tools:** Docker, Git, GitHub Actions, Postman, VS Code, Jupyter Notebook, AWS/GCP fundamentals
- **Concepts & Architecture:** Data Structures & Algorithms (800+ solved), System Design, Object-Oriented Programming (OOP), Design Patterns

### Achievements & Coding Profile
- **Infosys GitHub Copilot Hackathon (2024):** Secured 2nd Prize across enterprise developers.
- **Problem Solving:** Solved 800+ Data Structures and Algorithms problems across LeetCode, GeeksforGeeks, and other competitive coding platforms.

### Target Locations & Work Modes
- **Locations:** Bangalore (Bengaluru), Kolkata, India
- **Work Modes:** Hybrid, Onsite, and Remote (Pan-India & Global)
- **Roles:** AI Engineer, Generative AI Engineer, Software Engineer, Software Developer, Full-Stack AI Developer (2+ YoE)

## Core Workflows
- **`/scrape`** - Multi-portal search across LinkedIn, Naukri, Instahyre, and job portals
- **`/rank`** - Batch-score scraped postings against Anup's fit dimensions
- **`/apply <url or text>`** - Full pipeline: fit evaluation -> draft tailored CV + cover letter -> reviewer audit -> compile & ATS check
- **`/interview`** - Stage-specific prep pack, technical talking points, company research, and mock interview
- **`/outcome`** - Track application status and draft follow-ups
