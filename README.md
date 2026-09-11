# AI Office & Enterprise AI Architecture for Banking

> **Programa Avanzado de Arquitectura de IA, Gobernanza y PoCs para el Sector Financiero**  
> *Enfoque: Solutions Architecture, EU AI Act, RAG Avanzado, Multi-Agente, LLMOps & FinOps.*

---

## 📌 Objetivo del Repositorio

Este repositorio contiene la documentación técnica completa, diagramas de arquitectura, análisis normativos y Pruebas de Concepto (PoCs) de código funcional orientados al diseño e implementación de una **AI Office** en una entidad bancaria líder.

---

## 🗺️ Estructura del Proyecto

### 📄 Documentación Técnica
- `docs/01-governance-eu-ai-act.md`: Marco de gobernanza, EU AI Act y sanitización PII.
- `docs/02-enterprise-rag-architecture.md`: Arquitectura RAG híbrida y re-ranking.
- `docs/03-multi-agent-llmops-finops.md`: Sistemas multi-agente, LLMOps y optimización FinOps.
- `docs/04-ai-office-roadmap-roi.md`: Estrategia C-Level, ROI y roadmap de 12 meses.

### 🛠️ Pruebas de Concepto (PoCs)
- `pocs/poc-01-pii-sanitizer/`: Simulación de AI Gateway con enmascaramiento PII reversible.
- `pocs/poc-02-banking-rag/`: Motor RAG avanzado con búsqueda híbrida y citación de fuentes.
- `pocs/poc-03-multi-agent-risk/`: Sistema multi-agente de riesgo con enrutamiento FinOps.
- `pocs/poc-04-roi-calculator/`: Calculadora de TCO y ROI para proyectos de IA.

### 🏗️ Arquitectura y Presentaciones
- `arquitectura/diagrama/ai-office-architecture.svg`: Diagrama esquemático de la arquitectura integral.
- `slides/executive-ai-office-pitch.md`: Pitch ejecutivo (10 diapositivas).

### 🚀 Validación
- `validate_pocs.py`: Script para verificar la integridad operativa de todas las PoCs.

---

## ⚙️ Cómo ejecutar las pruebas
Para validar todos los componentes funcionales, ejecute:
```bash
python3 validate_pocs.py
```
