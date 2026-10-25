---
framework_version: 1.0.1
---

# Interview Preparation Guide - Anup Kumar Mahata

## STAR Format
Structure answers as: **Situation** (context), **Task** (your responsibility), **Action** (what you did), **Result** (outcome).
Keep answers to 1-2 minutes. Be specific with metrics.

## Ready-Made STAR Examples

### 1. Enterprise RAG Pipeline Architecture (Infosys)
- **S:** Enterprise teams required rapid, highly accurate document retrieval from diverse internal knowledge repositories with strict latency constraints.
- **T:** Lead the architectural design and deployment of an end-to-end RAG pipeline using LangChain, LangGraph, and vector databases.
- **A:** Designed chunking and embedding strategies, integrated hybrid search with FAISS and Elasticsearch, and created graph-based query expansion and reranking stages.
- **R:** Significantly improved semantic retrieval precision while keeping query latency under enterprise SLA limits.
- **Use for:** "Describe an enterprise AI system you built", "How do you handle vector search optimization and retrieval accuracy?"

### 2. Multi-Agent Orchestration with MCP Server (Infosys)
- **S:** Disparate tools and enterprise services needed seamless, secure orchestration within an autonomous AI assistant workflow.
- **T:** Architect native AI agents using the Model Context Protocol (MCP) server architecture and custom tool bindings.
- **A:** Built standardized MCP server endpoints, implemented structured tool-calling validation, and established state-aware agent communication protocols.
- **R:** Enabled modular, scalable tool integration that simplified adding new enterprise capabilities without touching agent core logic.
- **Use for:** "Have you worked with Model Context Protocol (MCP)?", "How do you design scalable tool-calling agents?"

### 3. Graph-Based Agent with Human-in-the-Loop (AI Travel Assistant)
- **S:** Automated travel booking agents risk booking errors or runaway API loops if decision boundaries are purely autonomous.
- **T:** Develop a resilient multi-agent travel planner incorporating conditional logic, retry loops, and human approval checkpoints.
- **A:** Implemented graph state management in LangGraph with branching, cyclic loops, and explicit human-in-the-loop (HITL) interrupt checkpoints before critical actions (e.g. payment/booking).
- **R:** Achieved 100% prevented erroneous bookings while maintaining an intuitive, conversational multi-agent user experience.
- **Use for:** "How do you handle safety and human-in-the-loop in agentic systems?", "Explain your experience with LangGraph."

### 4. Infosys GitHub Copilot Hackathon (Innovation Under Pressure)
- **S:** Competed against hundreds of enterprise developers to build a high-impact AI-augmented developer solution within 48 hours.
- **T:** Rapidly prototype and present a working agentic workflow solving a complex software development challenge.
- **A:** Designed modular agent components, leveraged pair programming and AI code synthesis, and conducted rigorous live demonstrations.
- **R:** Awarded 2nd Prize across the entire enterprise competition.
- **Use for:** "Tell me about a time you worked under high pressure", "Describe a technical achievement you are proud of."

## Core Technical Deep-Dives
- **RAG & Retrieval:** Dense vs sparse embeddings, chunking strategies, vector index trade-offs (HNSW in FAISS vs BM25 in Elasticsearch), reranking.
- **Agentic Architectures:** ReAct loops vs stateful graph workflows (LangGraph), deterministic guardrails, state persistence, memory.
- **System Design & Full-Stack:** Node.js event loop, RESTful API design, database indexing, caching layers, JWT authentication.
