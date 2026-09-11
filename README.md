# AI Office & Enterprise AI Architecture for Banking

> **Programa Avanzado de Arquitectura de IA, Gobernanza y PoCs para el Sector Financiero**  
> *Enfoque: Solutions Architecture, EU AI Act, RAG Avanzado, Multi-Agente, LLMOps & FinOps.*

---

## 📌 Objetivo del Repositorio

Este repositorio contiene la documentación técnica, diagramas de arquitectura C4, análisis normativos y Pruebas de Concepto (PoCs) de código funcional orientados al diseño e implementación de una **AI Office** en una entidad bancaria líder.

Diseñado para demostrar solvencia en la intersección entre **Estrategia de Negocio Financiero**, **Cumplimiento Regulatorio (EU AI Act/GDPR)** y **Patrones Avanzados de Ingeniería de Software/IA**.

---

## 🗺️ Estructura del Curso y Plan de Estudio

```text
ai-office-banking-course/
├── README.md                          <-- Índice general y Guía de Estudio
├── docs/                              <-- Temario teórico extenso (Markdown)
│   ├── 01-governance-eu-ai-act.md
│   ├── 02-enterprise-rag-architecture.md
│   ├── 03-multi-agent-llmops-finops.md
│   └── 04-ai-office-roadmap-roi.md
├── architecture/                      <-- Diagramas C4 y Flujos de Seguridad
│   ├── diagrams/                      <-- Renderizados visuales
│   └── code/                          <-- Diagramas en Mermaid.js
└── pocs/                              <-- Pruebas de Concepto (PoCs) en Python
    ├── poc-01-pii-sanitizer/          <-- Enmascaramiento PII + Guardrails
    ├── poc-02-banking-rag/            <-- Asistente de Análisis Documental
    └── poc-03-multi-agent-risk/       <-- Evaluación Multi-Agente de Riesgos

📚 Módulos del Programa
1. Gobernanza, EU AI Act y Seguridad de Datos en Banca
⚬	Enfoque: Clasificación de sistemas de alto riesgo según el EU AI Act, sanitización de PII (Datos de Carácter Personal), Landing Zones privadas (AWS/Azure) y auditoría.
⚬	Entregable: Docs Módulo 1 | PoC #1: PII Sanitizer & AI Gateway
2. Arquitectura RAG Avanzada e Integración Core Bancario
⚬	Enfoque: Búsqueda híbrida (Vector DBs + Búsqueda Léxica), Re-ranking, compresión contextual e integración con Core Legacy/APIs bancarias mediante eventos (Kafka/REST).
⚬	Entregable: Docs Módulo 2 | PoC #2: Banking RAG Document Analysis
3. Sistemas Multi-Agente, LLMOps y FinOps
⚬	Enfoque: Orquestación determinista de agentes (LangGraph), prevención de alucinaciones (Guardrails), monitorización de deriva (Drift) y optimización de costes de inferencia (Caché Semántica + Routing SLMs/LLMs).
⚬	Entregable: Docs Módulo 3 | PoC #3: Multi-Agent Credit Risk Analysis
4. Roadmap de la AI Office, ROI y Presentación Executive (C-Level)
⚬	Enfoque: Selección y priorización de casos de uso por impacto/coste, estructura organizativa de la AI Office, métricas de éxito (ROI) y negociación de riesgos con Compliance.
⚬	Entregable: Docs Módulo 4
🛠️ Tech Stack Utilizado en las PoCs
⚬	Lenguaje & Core: Python 3.11+, Pydantic v2
⚬	Frameworks de IA: LangChain, LangGraph, LlamaIndex
⚬	Bases de Datos Vectoriales: Qdrant / pgvector (PostgreSQL)
⚬	Seguridad & Guardrails: Presidio Analyzer, NeMo Guardrails
⚬	UI de Demostración: Streamlit / FastHTML
⚬	Diagramado: Mermaid.js, Structurizr C4
