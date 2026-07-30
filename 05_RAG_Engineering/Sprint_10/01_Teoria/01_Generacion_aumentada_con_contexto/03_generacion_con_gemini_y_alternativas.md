![Cabecera](../../assets/cabecera_rag.png)

# Generación con Gemini y alternativas

## Objetivos

- Generar respuestas con **Gemini** (`generate_content`).
- Entender que el **proveedor del LLM** puede cambiar sin rehacer retrieval.
- Conocer una **alternativa con Hugging Face** a nivel conceptual.

---

## 1) Camino principal: Gemini

Stack del bootcamp (S4–S10):

- Misma API key que embeddings (`GEMINI_API_KEY`).
- Modelo generativo en `config.py` → `GEMINI_MODEL` (p. ej. `gemini-2.0-flash`).
- Temperatura baja (`GENERATION_TEMPERATURE ≈ 0.2`) para respuestas más fieles al contexto.

En `generate.py`:

```python
from google import genai

def generar_respuesta(prompt: str) -> str:
    configurar_gemini_api_key()
    client = genai.Client()
    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
        config={"temperature": GENERATION_TEMPERATURE},
    )
    return (response.text or "").strip()
```

Nota: el modelo de **embedding** (`gemini-embedding-2`) y el de **generación** (`gemini-2.0-flash`) son distintos. No los mezcles en la misma variable de config.

---

## 2) Misma arquitectura, otro backend

```text
contexto + pregunta  →  build_rag_prompt()  →  generar_respuesta()
                                                      ↓
                                              Gemini  |  Hugging Face
```

Lo intercambiable es la **función de generación**, no el retriever ni Chroma. Si mañana cambias el LLM, `logic.responder()` sigue siendo:

```text
validar → recuperar → formatear → prompt → generar
```

Solo cambia la implementación de `generar`.

---

## 3) Alternativa: Hugging Face

Como en embeddings (Sprint 8), HF sirve para **comparar enfoques**, no para sustituir el camino principal del sprint.

| Modo | Idea | Cuándo |
|------|------|--------|
| **Nube** (Inference API) | Envías el prompt a un modelo hospedado en HF (`HF_TOKEN`) | Probar otro LLM sin instalar pesos |
| **Local** (`transformers`) | Cargas un modelo en tu máquina | Offline / demos sin cuota de API |

Ejemplo conceptual (nube, esqueleto):

```python
# Alternativa ilustrativa — no es el camino principal del proyecto
from huggingface_hub import InferenceClient

client = InferenceClient(token=os.environ["HF_TOKEN"])
texto = client.text_generation(
    prompt,
    model="mistralai/Mistral-7B-Instruct-v0.2",  # ejemplo
    max_new_tokens=512,
)
```

En local, con `transformers` / pipelines de chat, el patrón es el mismo: **mismo prompt RAG**, distinta llamada.

### Reglas si experimentas con HF

- No mezcles el índice Gemini con embeddings HF en el mismo índice sin re-indexar (eso es tema de embeddings, no de generación).
- Para **generación**, el índice puede seguir siendo Gemini: solo cambia el LLM final.
- Marca claramente en el notebook qué celdas son «alternativa opcional».

---

## 4) Matriz de decisión (nivel bootcamp)

| Criterio | Gemini | Hugging Face |
|----------|--------|--------------|
| Continuidad del módulo | ✅ Mismo stack S4–S10 | Comparación / ampliación |
| Setup | `GEMINI_API_KEY` | `HF_TOKEN` o pesos locales |
| Workout principal | Sí | Celda opcional |
| Producción real | Depende del caso | Depende del modelo y de la infra |

Mensaje pedagógico:

> Lo importante no es el logo del proveedor: es **retrieval + prompt + generación** con un contrato claro (`generar_respuesta(prompt)`).

---

## Resumen

- Gemini es el camino canónico de S10.
- Temperatura baja ayuda al grounding.
- HF es alternativa de la capa de generación, no un segundo hilo obligatorio.
- Siguiente: [Pipeline online y modularización](./04_pipeline_online_y_modularizacion.md).
