![Cabecera](../../assets/cabecera_rag.png)

# Del retrieval a la respuesta

## Objetivos

- Entender qué aporta la capa de generación respecto al retriever.
- Definir el contrato `responder(pregunta) → dict`.
- Ver el flujo end-to-end de inferencia RAG.

---

## 1) Retrieval ≠ respuesta

El retriever devuelve **fragmentos** ordenados por similitud. Eso **no** es una respuesta para el usuario final: son candidatos de evidencia.

| Salida | Para quién | Ejemplo |
|--------|------------|---------|
| Chunks + distance | Desarrollador / depuración | «Fragmento 1 (FAQ): GRATUITO=1 significa…» |
| Respuesta redactada | Usuario final | «Según la FAQ, el campo GRATUITO vale 1 si el evento es gratuito y 0 si no lo es.» |

La generación **sintetiza** esos fragmentos en lenguaje natural, respetando (idealmente) el corpus.

Error frecuente: mostrar al usuario el contexto crudo y llamar a eso «chatbot». El RAG completo **redacta**.

---

## 2) Flujo completo

```text
Pregunta
   ↓
Retriever (embed + Chroma)     ← Sprint 9
   ↓
Contexto formateado            ← context.py
   ↓
Prompt (instrucciones + contexto + pregunta)
   ↓
LLM (Gemini)
   ↓
Respuesta (+ fuentes)
```

En código, ese flujo se encapsula en una sola función:

```python
resultado = responder("¿Hay cine gratuito en verano?")
# resultado["respuesta"]  → texto para el usuario
# resultado["fuentes"]    → archivos citados
# resultado["contexto"]   → para depurar
# resultado["error"]      → None o mensaje
```

`main.py --ask` y Streamlit (`app.py`) **solo** llaman a `responder()`. No reimplementan retrieval ni generación.

---

## 3) Analogía con Sprint 5

En Prompt & Context Engineering ya montaste un asistente:

```text
S5 (manual)                    RAG (automático)
───────────                    ────────────────
consulta                       consulta
   │                              │
   ▼                              ▼
seleccionar_faq()              retriever (embeddings)
   │                              │
   ▼                              ▼
build_chat_prompt()            build_rag_prompt()
   │                              │
   ▼                              ▼
Gemini                         Gemini
```

La diferencia no es el LLM final: es **cómo eliges el contexto**. Keywords + FAQ fija → **recuperación semántica** sobre muchos chunks.

---

## 4) Anti-patrones

| Anti-patrón | Problema |
|-------------|----------|
| Mezclar `collection.query()` y `generate_content` en un solo script sin módulos | Difícil depurar y reutilizar |
| Pasar al LLM los chunks sin instrucciones de grounding | Alucinaciones y respuestas fuera de corpus |
| Ignorar `metadata.source` | No puedes citar fuentes ni depurar |
| Reescribir el pipeline dentro de Streamlit | Duplicas lógica; la UI se vuelve frágil |

---

## Resumen

- El retrieval selecciona evidencia; la generación **redacta**.
- El contrato del backend es `responder(pregunta)`.
- Misma idea que S5, con contexto recuperado automáticamente.
- Siguiente: [Prompt con contexto recuperado](./02_prompt_con_contexto_recuperado.md).
