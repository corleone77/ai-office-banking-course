#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PoC #4: Calculadora de TCO y ROI para Proyectos de IA en Banca
==============================================================
Calcula el retorno de inversión considerando costes de inferencia,
ahorros de productividad y optimización por caché semántica (FinOps).
"""

from dataclasses import dataclass

@dataclass
class ProjectParams:
    name: str
    monthly_queries: int
    avg_tokens_in: int
    avg_tokens_out: int
    cost_per_million_tokens_llm: float # Modelo Frontier
    cost_per_million_tokens_slm: float # Modelo Local
    slm_routing_percentage: float      # % de queries enrutadas a SLM
    cache_hit_rate: float              # % de queries resueltas por caché
    fte_hours_saved_per_query: float   # Horas ahorro por query
    avg_cost_per_fte_hour: float       # Coste hora-persona
    initial_setup_cost: float          # Inversión inicial (TCO)

class ROICalculator:
    def __init__(self, params: ProjectParams):
        self.p = params

    def calculate(self):
        # 1. Costes de Inferencia Mensual
        queries_raw = self.p.monthly_queries
        cache_hits = queries_raw * self.p.cache_hit_rate
        queries_to_process = queries_raw - cache_hits
        
        slm_queries = queries_to_process * self.p.slm_routing_percentage
        llm_queries = queries_to_process * (1 - self.p.slm_routing_percentage)
        
        cost_slm = (slm_queries * (self.p.avg_tokens_in + self.p.avg_tokens_out) / 1e6) * self.p.cost_per_million_tokens_slm
        cost_llm = (llm_queries * (self.p.avg_tokens_in + self.p.avg_tokens_out) / 1e6) * self.p.cost_per_million_tokens_llm
        
        monthly_inference_cost = cost_slm + cost_llm
        
        # 2. Ahorros de Productividad Mensual
        monthly_hours_saved = queries_raw * self.p.fte_hours_saved_per_query
        monthly_savings = monthly_hours_saved * self.p.avg_cost_per_fte_hour
        
        # 3. Métricas Financieras
        net_monthly_gain = monthly_savings - monthly_inference_cost
        payback_months = self.p.initial_setup_cost / net_monthly_gain
        three_year_net_savings = (net_monthly_gain * 36) - self.p.initial_setup_cost
        
        return {
            "monthly_inference_cost": monthly_inference_cost,
            "monthly_savings": monthly_savings,
            "net_monthly_gain": net_monthly_gain,
            "payback_months": payback_months,
            "three_year_net_savings": three_year_net_savings,
            "finops_reduction": (queries_raw - queries_to_process) / queries_raw * 100
        }

def run_report(params: ProjectParams):
    calc = ROICalculator(params)
    res = calc.calculate()
    
    print(f"--- INFORME EJECUTIVO ROI: {params.name} ---")
    print(f"Inversión Inicial: ${params.initial_setup_cost:,.2f}")
    print(f"Payback: {res['payback_months']:.1f} meses")
    print(f"Ahorro Neto a 3 años: ${res['three_year_net_savings']:,.2f}")
    print(f"Reducción de Costes (FinOps/Caché): {res['finops_reduction']:.1f}%")
    print("-" * 40)

if __name__ == "__main__":
    # Configuración de simulación para automatización de análisis de riesgos
    config = ProjectParams(
        name="Automatización Riesgos Crediticios",
        monthly_queries=100000,
        avg_tokens_in=2000,
        avg_tokens_out=500,
        cost_per_million_tokens_llm=15.0, # Ejemplo GPT-4
        cost_per_million_tokens_slm=0.5,  # Ejemplo Llama 3
        slm_routing_percentage=0.7,       # 70% enrutado a SLM
        cache_hit_rate=0.3,               # 30% cache hit
        fte_hours_saved_per_query=0.005,   # 18 segundos ahorro por consulta
        avg_cost_per_fte_hour=50.0,
        initial_setup_cost=50000.0
    )
    
    run_report(config)
