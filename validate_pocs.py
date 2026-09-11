#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de validación centralizada de PoCs del Proyecto AI Office.
Ejecuta secuencialmente todos los scripts de prueba y genera un reporte.
"""

import subprocess
import os

def run_poc(directory: str) -> bool:
    path = os.path.join("ai-office-banking-course", "pocs", directory, "main.py")
    print(f"--- Validando: {directory} ---")
    
    try:
        # Ejecuta el script capturando salida
        result = subprocess.run(
            ["python3", path],
            capture_output=True,
            text=True,
            check=False
        )
        
        if result.returncode == 0:
            print(f"Estado: PASS")
            return True
        else:
            print(f"Estado: FAIL (Exit Code: {result.returncode})")
            print("Detalles de error:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"Estado: FAIL (Excepción: {e})")
        return False

def main():
    pocs = [
        "poc-01-pii-sanitizer",
        "poc-02-banking-rag",
        "poc-03-multi-agent-risk",
        "poc-04-roi-calculator"
    ]
    
    results = {}
    
    print("Iniciando suite de validación de PoCs...\n")
    
    for poc in pocs:
        results[poc] = run_poc(poc)
        print("-" * 30 + "\n")
        
    print("=== RESUMEN FINAL DE VALIDACIÓN ===")
    for poc, passed in results.items():
        status = "PASS" if passed else "FAIL"
        print(f"[{status}] {poc}")

if __name__ == "__main__":
    main()
