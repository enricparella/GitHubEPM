![Cabecera](../../assets/cabecera_rag.png)

# Pipeline online y modularización

## Objetivos

- Modularizar la capa de generación sin mezclar responsabilidades.
- Conocer los módulos nuevos del proyecto S10.
- Usar `main.py --ask` para probar respuestas desde consola.

---

## 1) Módulos nuevos (Sprint 10)

| Módulo | Responsabilidad |
|--------|-----------------|
| `prompts.py` | Construir el prompt RAG |
| `generate.py` | Llamada al LLM (Gemini) |
| `validators.py` | Validación pre-LLM (pregunta / contexto) |
| `logic.py` | `responder(pregunta)` — orquestador |
| `app.py` | Streamlit (Bloque 3) |

Los módulos S8–S9 (`load` … `retriever`, `context`) **se reutilizan**.

```text
config.py, gemini_auth.py
        │
        ├── load → clean → chunk → pipeline → embed   (S8, offline)
        ├── index → retriever → context               (S9)
        └── prompts → generate → validators → logic   (S10, online)
                              ↑
                         main.py / app.py
```

---

## 2) Qué hace `logic.responder()`

```text
pregunta
   │
   ▼
validar_pregunta()
   │
   ▼
recuperar()  →  formatear_contexto()
   │
   ▼
validar_contexto()
   │
   ▼
build_rag_prompt()  →  generar_respuesta()
   │
   ▼
{ respuesta, contexto, chunks, fuentes, error }
```

Regla: `main.py` y `app.py` son **delgados**. La lógica vive en `logic.py`.

---

## 3) CLI extendida

```bash
# Offline (igual que S9)
python main.py --prepare --index

# Solo contexto (S9)
python main.py --query "¿Hay cine gratuito en verano?"

# RAG completo (S10)
python main.py --ask "¿Hay cine gratuito en verano?"
```

`--query` inspecciona retrieval. `--ask` añade generación.

---

## 4) Configuración relevante

En `config.py` (además de chunking / Chroma / `TOP_K`):

| Variable | Uso |
|----------|-----|
| `GEMINI_MODEL` | Modelo de generación |
| `GENERATION_TEMPERATURE` | Creatividad vs fidelidad |
| `TOP_K` | Cuántos chunks van al prompt |

Experimentar: cambia `TOP_K` o la temperatura y vuelve a ejecutar `--ask` con la misma pregunta.

---

## 5) Orden recomendado al explorar el código

1. `config.py` — modelos y `TOP_K`.
2. `context.py` — cómo se formatea lo que ya recuperabas en S9.
3. `prompts.py` → `generate.py` → `logic.py`.
4. `main.py` — cómo se engancha `--ask`.
5. Más adelante (Bloque 3): `app.py`.

Proyecto: [`05_proyecto_rag_aplicacion/`](../03_Interfaces_y_aplicaciones_rag/05_proyecto_rag_aplicacion/).

---

## Resumen

- S10 añade `prompts`, `generate`, `validators`, `logic` (y `app` en Bloque 3).
- `responder()` es el contrato único del backend.
- `--ask` prueba el RAG completo en consola.
- Workout: [01_del_retrieval_a_la_respuesta_rag.ipynb](../../02_Workout/01_Generacion_aumentada_con_contexto/01_del_retrieval_a_la_respuesta_rag.ipynb).
