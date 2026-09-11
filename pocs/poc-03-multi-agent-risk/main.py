#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PoC #3: Sistema Multi-Agente de Evaluación de Riesgos Financieros con FinOps
===========================================================================
Simula orquestación multi-agente (Extractor, Evaluador, Auditor) con 
enrutamiento inteligente (FinOps) y caché semántica.
"""

from typing import Dict, Any, Optional

# --- Capa de FinOps y Caché ---
class FinOpsCache:
    def __init__(self):
        self._cache = {}

    def get(self, query: str) -> Optional[Dict[str, Any]]:
        return self._cache.get(query)

    def set(self, query: str, result: Dict[str, Any]):
        self._cache[query] = result

class FinOpsRouter:
    """Enruta según la complejidad de la tarea."""
    def route(self, task_data: str) -> str:
        # Lógica simplificada: expedientes pequeños -> SLM, grandes -> LLM
        return "SLM" if len(task_data) < 100 else "LLM"

# --- Agentes ---
class AgenteExtractor:
    def execute(self, model: str, data: str) -> Dict[str, float]:
        print(f"  [Extractor] Procesando con {model}...")
        # Simulación: extraer números
        return {"ingresos": 3000.0, "deudas": 500.0}

class AgenteEvaluador:
    def execute(self, model: str, extracted_data: Dict[str, float]) -> Dict[str, Any]:
        print(f"  [Evaluador] Calculando ratio con {model}...")
        ratio = extracted_data["deudas"] / extracted_data["ingresos"]
        return {"ratio": ratio, "aprobado": ratio < 0.4}

class AgenteAuditor:
    def execute(self, model: str, evaluation: Dict[str, Any]) -> str:
        print(f"  [Auditor] Verificando cumplimiento con {model}...")
        return "APROBADO" if evaluation["aprobado"] else "RECHAZADO"

# --- Orquestador ---
class Orchestrator:
    def __init__(self):
        self.cache = FinOpsCache()
        self.router = FinOpsRouter()
        self.extractor = AgenteExtractor()
        self.evaluador = AgenteEvaluador()
        self.auditor = AgenteAuditor()

    def run_workflow(self, expediente: str) -> Dict[str, Any]:
        # 1. Caché
        cached = self.cache.get(expediente)
        if cached:
            print("[Info] Resultado recuperado de caché semántica.")
            return cached

        print(f"[Workflow] Iniciando análisis para: {expediente[:50]}...")
        
        # 2. Routing
        model = self.router.route(expediente)
        
        # 3. Pipeline Multi-Agente
        data = self.extractor.execute(model, expediente)
        evaluation = self.evaluador.execute(model, data)
        result = self.auditor.execute(model, evaluation)
        
        final_output = {"resultado": result, "detalles": evaluation}
        
        # 4. Cachear
        self.cache.set(expediente, final_output)
        return final_output

if __name__ == "__main__":
    orchestrator = Orchestrator()
    
    # Expediente 1
    expediente_1 = "Cliente: Juan, Ingresos: 3000, Deudas: 500"
    print(f"\nCaso 1: {orchestrator.run_workflow(expediente_1)}")
    
    # Expediente 1 (repetido - debe usar caché)
    print(f"\nCaso 1 (Caché): {orchestrator.run_workflow(expediente_1)}")
    
    # Expediente 2 (Complejo)
    expediente_2 = "Cliente: Ana, Ingresos: 10000, Deudas: 9000, " + "datos adicionales" * 10
    print(f"\nCaso 2: {orchestrator.run_workflow(expediente_2)}")
