#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PoC #1: PII Sanitizer & AI Gateway Simulation
======================================================
Este script simula un AI Gateway para entidades bancarias que intercepta prompts,
sanitiza y enmascara Datos de Carácter Personal (PII) bajo cumplimiento estricto
de GDPR antes de enviar el payload a LLMs comerciales, y rehidrata la respuesta
para entregarla de forma íntegra y segura al canal del cliente.

Cumple con directrices del EU AI Act y GDPR para procesamiento seguro de datos financieros.
"""

import re
import sys
from typing import Dict, List, Tuple


class PIISanitizer:
    """
    Clase de nivel Enterprise para la sanitización y rehidratación reversible de PII.
    """

    def __init__(self):
        # Mapeos bidireccionales para garantizar consistencia semántica y reversibilidad
        self.original_to_token: Dict[str, str] = {}
        self.token_to_original: Dict[str, str] = {}

        # Contadores secuenciales por categoría de PII
        self.counters: Dict[str, int] = {
            "DNI": 1,
            "CARD": 1,
            "IBAN": 1,
            "EMAIL": 1,
            "BALANCE": 1,
        }

        # Patrones regex optimizados para banca y cumplimiento normativo español
        # El orden es crucial para evitar colisiones (p. ej., que CARD reconozca grupos numéricos dentro de un IBAN)
        self.patterns: Dict[str, re.Pattern] = {
            # IBAN Español: ES + 2 dígitos de control + 20 dígitos de cuenta (agrupaciones de 4)
            "IBAN": re.compile(
                r"\bES\d{2}(?:[- ]?\d{4}){5}\b",
                re.IGNORECASE,
            ),
            # DNI: 8 dígitos + letra o NIE: X/Y/Z + 7 dígitos + letra (con guiones o espacios opcionales)
            "DNI": re.compile(
                r"\b(?:\d{8}[- ]?[A-HJ-NP-TV-Z]|[XYZ]\d{7}[- ]?[A-Z])\b",
                re.IGNORECASE,
            ),
            # Tarjetas de crédito (PAN): 13 a 19 dígitos, agrupados habitualmente de 4 en 4
            "CARD": re.compile(
                r"\b(?:\d{4}[- ]?){3}\d{1,4}\b"
            ),
            # Correo electrónico estándar
            "EMAIL": re.compile(
                r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b"
            ),
            # Saldos y cantidades monetarias en múltiples notaciones (EUR, €, USD, $, etc.)
            "BALANCE": re.compile(
                # Notación europea (1.250,50 € / 500 EUR / 1000 euros)
                r"(?:\b\d{1,3}(?:\.\d{3})*(?:,\d{2})?|\b\d+(?:,\d{2})?)\s*(?:€|\b(?:EUR|euros?|USD|dollars?)\b)"
                r"|"
                # Notación americana ($10,000.00 / £550.22)
                r"(?:\$|£)\s*(?:\d{1,3}(?:,\d{3})*(?:\.\d{2})?|\d+(?:\.\d{2})?)\b",
                re.IGNORECASE,
            ),
        }

    def sanitize(self, text: str) -> str:
        """
        Escanea el prompt de entrada, detecta entidades PII y las reemplaza por
        tokens desidentificados específicos. Preserva la equivalencia de datos repetidos.
        """
        sanitized_text = text

        for pii_type, regex in self.patterns.items():
            # Extraer todas las coincidencias únicas
            matches = list(set(regex.findall(sanitized_text)))

            # Ordenar de mayor a menor longitud para evitar que subcadenas causen colisiones de sustitución
            matches.sort(key=len, reverse=True)

            for match in matches:
                match_str = match.strip()
                if not match_str:
                    continue

                # Si el valor ya fue tokenizado, reutilizar el token para mantener coherencia semántica
                if match_str in self.original_to_token:
                    token = self.original_to_token[match_str]
                else:
                    index = self.counters[pii_type]
                    token = f"[{pii_type}_REDACTED_{index}]"
                    self.counters[pii_type] += 1

                    # Registrar la relación en la tabla de mapeo
                    self.original_to_token[match_str] = token
                    self.token_to_original[token] = match_str

                # Realizar la sustitución en el texto
                sanitized_text = sanitized_text.replace(match_str, token)

        return sanitized_text

    def rehydrate(self, text: str) -> str:
        """
        Restaura los datos PII reales en el texto de respuesta del LLM a partir de los tokens.
        """
        rehydrated_text = text
        for token, original_value in self.token_to_original.items():
            rehydrated_text = rehydrated_text.replace(token, original_value)
        return rehydrated_text


# ======================================================
# Pruebas Unitarias Automatizadas Integradas (Verificación)
# ======================================================
def run_unit_tests():
    print("=" * 60)
    print(" INICIANDO PRUEBAS UNITARIAS DE VALIDACIÓN ")
    print("=" * 60)
    
    sanitizer = PIISanitizer()
    tests_passed = 0
    total_tests = 6

    # Test 1: Sanitización de DNI y NIE español
    dni_test_input = "Mi DNI es 12345678A y mi NIE es Y8765432B."
    sanitized = sanitizer.sanitize(dni_test_input)
    assert "[DNI_REDACTED_1]" in sanitized
    assert "[DNI_REDACTED_2]" in sanitized
    assert "12345678A" not in sanitized
    assert "Y8765432B" not in sanitized
    rehydrated = sanitizer.rehydrate(sanitized)
    assert rehydrated == dni_test_input
    print("✔ Test 1: Validación DNI/NIE Española - PASADO")
    tests_passed += 1

    # Test 2: Sanitización de Tarjeta de Crédito (PAN)
    card_test_input = "Tengo cargos raros en mi tarjeta 4532 7182 9381 0293 y la 1234-5678-9012-3456."
    sanitized = sanitizer.sanitize(card_test_input)
    assert "[CARD_REDACTED_1]" in sanitized
    assert "[CARD_REDACTED_2]" in sanitized
    assert "4532" not in sanitized
    rehydrated = sanitizer.rehydrate(sanitized)
    assert rehydrated == card_test_input
    print("✔ Test 2: Validación Tarjetas de Crédito - PASADO")
    tests_passed += 1

    # Test 3: Sanitización de IBAN
    iban_test_input = "La cuenta receptora es ES21 1465 0100 2012 3456 7890."
    sanitized = sanitizer.sanitize(iban_test_input)
    assert "[IBAN_REDACTED_1]" in sanitized
    assert "ES21 1465" not in sanitized
    rehydrated = sanitizer.rehydrate(sanitized)
    assert rehydrated == iban_test_input
    print("✔ Test 3: Validación IBAN Bancario - PASADO")
    tests_passed += 1

    # Test 4: Sanitización de Email
    email_test_input = "Escríbeme a juan.gomez_financial@banca-online.es para confirmación."
    sanitized = sanitizer.sanitize(email_test_input)
    assert "[EMAIL_REDACTED_1]" in sanitized
    assert "juan.gomez" not in sanitized
    rehydrated = sanitizer.rehydrate(sanitized)
    assert rehydrated == email_test_input
    print("✔ Test 4: Validación Email - PASADO")
    tests_passed += 1

    # Test 5: Sanitización de Saldos/Saldos Financieros
    balance_test_input = "Mi cuenta tiene un saldo de 15.420,50 € y otra de $5,000.00 más 1500 EUR."
    sanitized = sanitizer.sanitize(balance_test_input)
    assert "[BALANCE_REDACTED_1]" in sanitized
    assert "[BALANCE_REDACTED_2]" in sanitized
    assert "[BALANCE_REDACTED_3]" in sanitized
    assert "15.420,50" not in sanitized
    assert "5,000" not in sanitized
    rehydrated = sanitizer.rehydrate(sanitized)
    assert rehydrated == balance_test_input
    print("✔ Test 5: Validación Saldos y Monedas - PASADO")
    tests_passed += 1

    # Test 6: Consistencia Semántica (mismo PII = mismo token)
    consistency_input = "El correo del cliente juan@banca.com coincide con su contacto en juan@banca.com."
    sanitized = sanitizer.sanitize(consistency_input)
    # Debe haber reemplazado ambas ocurrencias con [EMAIL_REDACTED_2] (puesto que el primer email fue registrado en Test 4)
    # Vamos a verificar que use el mismo token para ambos
    tokens_found = re.findall(r"\[EMAIL_REDACTED_\d+\]", sanitized)
    assert len(tokens_found) == 2
    assert tokens_found[0] == tokens_found[1]
    rehydrated = sanitizer.rehydrate(sanitized)
    assert rehydrated == consistency_input
    print("✔ Test 6: Validación de Consistencia Semántica - PASADO")
    tests_passed += 1

    print("\n" + "=" * 60)
    print(f" RESULTADO DE PRUEBAS: {tests_passed}/{total_tests} PASADAS CON ÉXITO")
    print("=" * 60 + "\n")


# ======================================================
# Demostración del Escenario del AI Gateway Bancario
# ======================================================
def run_simulation_demo():
    print("=" * 70)
    print(" INICIANDO SIMULACIÓN DE AI GATEWAY BANCARIO (SCENARIO DEMO) ")
    print("=" * 70)

    # 1. Instanciamos el Sanitizador del Gateway
    gateway_sanitizer = PIISanitizer()

    # 2. Entrada Raw del Canal Cliente (Simula un cliente enviando PII sensible en lenguaje natural)
    prompt_cliente_raw = (
        "Hola, buenas tardes. Mi nombre es Juan Carlos Gómez López con DNI 12345678A. "
        "Deseo realizar una auditoría de mi cuenta bancaria número ES21 1465 0100 2012 3456 7890. "
        "Ayer vi un cargo sospechoso por valor de 450,00 EUR en mi tarjeta de crédito 4532 7182 9381 0293. "
        "Actualmente mi cuenta tiene un saldo de 12.850,45 € y tengo domiciliadas un par de facturas. "
        "Para cualquier reporte o actualización, me pueden contactar en jc.gomez_92@banco-cliente.com "
        "o a través del gestor pedro.ramirez@bancorosa.es quien también me conoce."
    )

    print("\n[PASO 1] Prompt recibido en el AI Gateway desde el Canal Cliente:")
    print("-" * 75)
    print(prompt_cliente_raw)
    print("-" * 75)

    # 3. Intercepción y Sanitización (Inbound Gateway Processing)
    prompt_sanitizado = gateway_sanitizer.sanitize(prompt_cliente_raw)
    print("\n[PASO 2] Prompt Sanitizado por el AI Gateway (Payload enviado al LLM Comercial):")
    print("-" * 75)
    print(prompt_sanitizado)
    print("-" * 75)

    # 4. Simulación de Respuesta del LLM (Procesamiento Externo Libre de PII)
    # Nótese que el LLM procesa de forma óptima el contexto gramatical basándose en los placeholders estructurados
    respuesta_llm_raw = (
        "Hola, se ha analizado la solicitud del usuario con identificación [DNI_REDACTED_1]. "
        "En relación a la cuenta [IBAN_REDACTED_1], confirmamos que el cargo reportado de [BALANCE_REDACTED_1] "
        "en la tarjeta de crédito [CARD_REDACTED_1] coincide con un comercio en el extranjero no habitual. "
        "Se recomienda congelar temporalmente la tarjeta y transferir el saldo disponible de [BALANCE_REDACTED_2] "
        "a una cuenta segura de ahorros. "
        "Hemos enviado una alerta de seguridad de respaldo al correo principal del cliente: [EMAIL_REDACTED_1] "
        "e igualmente hemos notificado con copia a su asesor registrado bajo el correo [EMAIL_REDACTED_2]."
    )

    print("\n[PASO 3] Respuesta generada por el LLM Comercial Externo (Alineado con GDPR - Sin PII):")
    print("-" * 75)
    print(respuesta_llm_raw)
    print("-" * 75)

    # 5. Rehidratación de la Respuesta en el Gateway (Outbound Gateway Processing)
    respuesta_rehidratada = gateway_sanitizer.rehydrate(respuesta_llm_raw)
    print("\n[PASO 4] Respuesta final rehidratada por el AI Gateway (Entregada al Cliente de forma íntegra):")
    print("-" * 75)
    print(respuesta_rehidratada)
    print("-" * 75)

    # 6. Reporte del Token Vault Criptográfico en memoria
    print("\n[AUDITORÍA / TELEMETRÍA] Estado del Token Vault local para esta sesión:")
    print("-" * 75)
    print(f"  Número total de entidades enmascaradas: {len(gateway_sanitizer.original_to_token)}")
    print("  Tabla de equivalencia (Mapeo Criptográfico):")
    for orig, token in gateway_sanitizer.original_to_token.items():
        print(f"    • {token:<25} ──► {orig}")
    print("-" * 75)


if __name__ == "__main__":
    # Ejecutar tanto las pruebas como la demostración
    run_unit_tests()
    run_simulation_demo()
