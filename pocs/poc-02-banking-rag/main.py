#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PoC #2: RAG Avanzado para Análisis de Contratos Hipotecarios
===========================================================
Simulación de motor de RAG Enterprise con búsqueda híbrida,
re-ranking y citación de fuentes para documentos bancarios.

Uso: Ejecutar como script independiente.
"""

from typing import List, Dict
import re

# Modelo de datos para un fragmento (Chunk) de documento
class DocumentChunk:
    def __init__(self, content: str, metadata: Dict[str, str]):
        self.content = content
        self.metadata = metadata
        # Simulación de un vector (en un escenario real, sería un embedding real)
        self.vector = self._simulate_embedding(content)

    def _simulate_embedding(self, content: str) -> List[float]:
        # Simulación simple: vector basado en la longitud y presencia de palabras clave
        length = len(content)
        keywords = ["interés", "amortización", "cláusula", "impago"]
        score = sum(1 for kw in keywords if kw in content.lower())
        return [float(length) / 1000.0, float(score) / 10.0]

    def __repr__(self):
        return f"Chunk(meta={self.metadata['clause']}, score_vect={self.vector[1]:.2f})"

# Motor de RAG
class BankingRAGEngine:
    def __init__(self, documents: List[DocumentChunk]):
        self.documents = documents

    def hybrid_search(self, query: str, top_k: int = 5) -> List[DocumentChunk]:
        """Búsqueda Híbrida: Combina keyword search (BM25 simulado) y similitud vectorial."""
        
        results = []
        query_terms = set(query.lower().split())
        
        for doc in self.documents:
            # 1. Simulación BM25 (Coincidencia de palabras clave)
            doc_content = doc.content.lower()
            keyword_score = 0
            for term in query_terms:
                if term in doc_content:
                    # Dar peso extra a términos críticos
                    if term == "impago":
                        keyword_score += 5
                    else:
                        keyword_score += 1
            
            # 2. Simulación Vectorial (Similitud simple)
            vector_score = doc.vector[1] # Usamos el score del simulador de vector
            
            # Puntuación combinada (Hybrid Search)
            total_score = (keyword_score * 0.7) + (vector_score * 0.3)
            results.append((doc, total_score))
            
        # Ordenar por puntuación
        results.sort(key=lambda x: x[1], reverse=True)
        return [r[0] for r in results[:top_k]]

    def re_rank(self, candidates: List[DocumentChunk], query: str) -> List[DocumentChunk]:
        """Simulación de Re-ranking (Cross-Encoder): Filtro final más estricto."""
        # En la realidad, pasaría por un modelo Cross-Encoder.
        # Aquí, simulamos una re-evaluación basada en la relevancia directa de la consulta.
        def cross_encoder_score(doc: DocumentChunk):
            # Simulación: mejorada
            q = query.lower()
            c = doc.content.lower()
            m = doc.metadata['clause'].lower()
            
            # Puntuación basada en relevancia semántica real
            score = 0
            if "pago" in q and "impago" in c: score += 10
            if "no pago" in q and "impago" in c: score += 10
            if "impago" in m: score += 5
            
            return float(score)

        scored = [(doc, cross_encoder_score(doc)) for doc in candidates]
        scored.sort(key=lambda x: x[1], reverse=True)
        return [s[0] for s in scored[:3]] # Retorna los 3 mejores

    def generate_answer(self, query: str, top_chunks: List[DocumentChunk]) -> str:
        """Generación con citación obligatoria."""
        if not top_chunks:
            return "No se encontró información relevante en el contrato."
        
        # Generación simulada
        best_chunk = top_chunks[0]
        answer = f"Según la {best_chunk.metadata['clause']} (pág. {best_chunk.metadata['page']}): {best_chunk.content}"
        return answer

# ======================================================
# Ejecución del escenario
# ======================================================
if __name__ == "__main__":
    # 1. Ingesta simulada
    contract_chunks = [
        DocumentChunk("El tipo de interés aplicable será el Euribor más un diferencial del 1%.", {"clause": "Cláusula 1: Tipo de Interés", "page": "1"}),
        DocumentChunk("La amortización se realizará mensualmente mediante el sistema francés.", {"clause": "Cláusula 2: Amortización", "page": "2"}),
        DocumentChunk("En caso de impago, el banco aplicará un interés de demora del 5%.", {"clause": "Cláusula 3: Impago", "page": "3"}),
        DocumentChunk("El contrato tiene una duración máxima de 30 años.", {"clause": "Cláusula 4: Duración", "page": "1"}),
    ]
    
    engine = BankingRAGEngine(contract_chunks)
    
    # 2. Query de usuario
    query = "qué pasa si no pago la hipoteca"
    print(f"Query: {query}\n")
    
    # 3. Pipeline
    candidates = engine.hybrid_search(query)
    reranked = engine.re_rank(candidates, query)
    answer = engine.generate_answer(query, reranked)
    
    # 4. Resultado
    print(f"Respuesta generada:\n{answer}")
