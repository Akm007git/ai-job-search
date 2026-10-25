---
name: interview
description: >-
  Prepare for an upcoming interview. Builds stage-specific prep packs, company and interviewer
  research, STAR-method talking points, technical questions, and interactive mock interviews.
  Triggers on: /interview, interview, prep interview, interview prep, mock interview.
---

# /interview - Interview Preparation Pack & Mock Interview

Builds an end-to-end preparation briefing for scheduled interviews on tracked applications.

---

## Workflow

1. **Load Application Archive**:
   Reads the exact CV, cover letter, and job posting submitted from `documents/applications/<company>_<role>/`.
2. **Company & Market Research**:
   Researches company business model, recent news, engineering architecture, and leadership using WebSearch.
3. **STAR Stories Mapping**:
   Maps candidate's proven experience (e.g. Enterprise RAG, LangGraph multi-agent orchestration, MCP servers, Infosys projects) to likely behavioral and situational questions.
4. **Technical & System Design Topics**:
   Prepares deep-dive talking points on vector databases, low-latency retrieval, hallucination mitigation, human-in-the-loop flows, and scalable REST APIs.
5. **Interactive Mock Interview**:
   Offers a realistic mock interview simulating the role's interviewer, providing immediate constructive feedback.
