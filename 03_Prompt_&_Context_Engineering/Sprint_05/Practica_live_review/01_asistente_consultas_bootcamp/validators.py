"""validators.py — Validación de consultas en Python (Fase 1).

Qué hace este módulo:
  - Comprueba nombre, email y mensaje antes de llamar a Gemini.
  - Devuelve una lista de errores (vacía = consulta válida).

Para qué sirve:
  - Ahorrar tokens y evitar llamadas a la API con datos mal formados.
  - Es el primer paso del flujo en `clasificar_consulta()` (logic.py).

Función a implementar:
  - `validar_consulta(datos)` — ver README FASE 1, Tarea 1.
"""

from config import (
    MAX_CHARS_MENSAJE,
    MIN_CHARS_MENSAJE,
    PATRON_EMAIL,
)


def validar_consulta(datos: dict) -> list[str]:
    errores = []

    if not isinstance(datos, dict):
      errores.append("La consulta debe tener un formato dict.")

    nombre = str(datos.get("nombre", "")).strip()
    if not nombre:
      errores.append("Nombre inválido: ...")

    email = str(datos.get("email", "")).strip()
    if not email:
      errores.append("Email inválido: ...")
    elif PATRON_EMAIL.fullmatch(email) is None:
      errores.append("Email inválido: formato incorrecto.")

    mensaje = str(datos.get("mensaje", "")).strip()
    if len(mensaje) < MIN_CHARS_MENSAJE:
      errores.append(f"Mensaje demasiado corto ...")
    elif len(mensaje) > MAX_CHARS_MENSAJE:
      errores.append(f"Mensaje demasiado largo ...")

    return errores