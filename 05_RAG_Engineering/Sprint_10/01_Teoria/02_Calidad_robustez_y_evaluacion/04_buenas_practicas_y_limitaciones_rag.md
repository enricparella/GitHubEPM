![Cabecera](../../assets/cabecera_rag.png)

# Buenas prácticas y limitaciones de un RAG

## Objetivos

- Resumir buenas prácticas de sistemas RAG (nivel bootcamp).
- Enumerar limitaciones reales: corpus, chunking, top-K, modelo, latencia.
- Dejar claro qué se mejora en la UI (Bloque 3) y qué llegará con agentes (Sprint 11+).

---

## 1) Buenas prácticas

| Práctica | Por qué |
|----------|---------|
| Evaluar **retrieval y generación** por separado | Sabes qué capa falló |
| Centralizar config (`TOP_K`, modelos, temperatura) | Experimentar sin tocar lógica |
| Prompt con **grounding** y abstención | Menos alucinaciones |
| Validar **antes** del LLM | Menos coste y más robustez |
| Mostrar **fuentes** al usuario | Confianza y depuración |
| Loguear / inspeccionar contexto en desarrollo | `--query` antes de confiar en `--ask` |
| Set fijo de preguntas | Comparar cambios de config |

---

## 2) Limitaciones (hay que conocerlas)

| Limitación | Ejemplo |
|------------|---------|
| **Corpus incompleto** | Pregunta sobre un evento no indexado |
| **Chunking** | La respuesta está partida entre dos chunks y K=1 no basta |
| **Top-K bajo** | Falta evidencia; K alto → ruido |
| **Índice parcial** | `MAX_CHUNKS_EMBED = 5` en demo → cobertura pobre |
| **Modelo** | Resume mal, ignora instrucciones o inventa |
| **Latencia / coste** | Cada consulta = embed + generate (+ UI) |
| **No es un buscador perfecto** | Semántica ≠ verdad absoluta |

Un RAG **no** sustituye:

- bases de datos transaccionales en tiempo real,
- reglas de negocio críticas sin validación,
- un experto humano en dominios sensibles.

---

## 3) Checklist pre-demo

Antes de enseñar el sistema:

- [ ] Corpus en `data/` e índice construido (`--prepare --index`)
- [ ] `--ask` funciona en 2–3 preguntas «fáciles»
- [ ] q5 (fuera de corpus) **abstiene** o falla de forma controlada
- [ ] Fuentes visibles en consola o UI
- [ ] Sabes explicar un fallo conocido (p. ej. K bajo)

---

## 4) Puente al Bloque 3 y a Sprint 11

Hasta ahora el sistema vive en **consola**. El Bloque 3 añade **Streamlit** sin rehacer el backend: misma `responder(pregunta)`.

Más adelante (agentes):

```text
Ahora (S10)              Después (S11+)
───────────              ──────────────
Streamlit                Streamlit
   ↓                        ↓
RAG directo              Agente → tools → RAG
```

La interfaz puede mantenerse; cambia la **inteligencia** del backend.

---

## Resumen

- Buenas prácticas = evaluar por capas, grounding, validar, citar.
- Las limitaciones son del corpus, del chunking, del K y del modelo — no «magia del LLM».
- Workout: [01_evaluar_respuestas_rag.ipynb](../../02_Workout/02_Calidad_robustez_y_evaluacion/01_evaluar_respuestas_rag.ipynb).
- Siguiente bloque: [Interfaces y aplicaciones](../03_Interfaces_y_aplicaciones_rag/readme.md).
