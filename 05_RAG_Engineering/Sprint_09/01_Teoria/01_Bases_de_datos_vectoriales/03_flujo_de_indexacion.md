![Cabecera](../../assets/cabecera_rag.png)

# Flujo de indexación

## Objetivos

- Describir el pipeline **embeddings.json → ChromaDB**.
- Entender IDs, batches y reindexación.
- Relacionar `index.py` con el proyecto modular del sprint.

---

## 1) Diagrama del flujo

```text
  embeddings.json
  ├── embedding_model: "gemini-embedding-2"
  ├── dimensions: 3072
  └── items[]
        ├── text
        ├── vector[]
        └── metadata{}
              │
              ▼
         index.py
              │
              ├─► leer items
              ├─► generar ids (chunk_0, chunk_1, ...)
              ├─► sanitizar metadatas
              ├─► collection.add() en lotes
              └─► guardar en output/chroma_db/
```

La indexación **no** vuelve a llamar a Gemini si los vectores ya están en `embeddings.json`. Solo los **persiste** en Chroma. Si cambias el tamaño de los chunks (`CHUNK_SIZE`), debes regenerar chunks y embeddings antes de reindexar.

---

## 2) Pasos en `index.py`

Cuando se hace indexación, se utilizar un fichero con nombre `index.py` (puede tener otro nombre en tu proyecto), que es el que se encarga de indexar los chunks en ChromaDB. Se le pasa el archivo `embeddings.json` y se indexa en ChromaDB.

| Paso | Qué hace |
|------|----------|
| 1 | Abre `PersistentClient` en `config.CHROMA_DIR` |
| 2 | Obtiene o crea la colección `config.COLLECTION_NAME` |
| 3 | Carga `items` desde `embeddings.json` |
| 4 | Construye listas paralelas: `ids`, `embeddings`, `documents`, `metadatas` |
| 5 | Llama a `collection.add()` en lotes (`INDEX_BATCH_SIZE`) |
| 6 | Imprime `collection.count()` |

NOTA: Si se desea borrar la colección y recrearla (útil al cambiar el corpus), se puede hacer con el comando `python main.py --recreate-index`. Esto es útil para cuando se cambia el corpus o se cambia el modelo de embedding.

---

## 3) Generación de IDs

Convención del proyecto:

```python
id = f"chunk_{metadata.get('chunk_index', i)}"
```

Los IDs deben ser **estables** si quieres actualizar documentos concretos más adelante. Para este sprint, un id por `chunk_index` es suficiente.

---

## 4) Indexación por lotes

Añadir miles de vectores de una vez puede ser lento o fallar por memoria. El proyecto usa lotes (p. ej. 100 items). En el ejemplo siguiente puedes ver INDEX_BATCH_SIZE, que si tuviera valor 100, se añadirían 100 vectores a la vez.

```python
for inicio in range(0, len(ids), INDEX_BATCH_SIZE):
    fin = inicio + INDEX_BATCH_SIZE
    collection.add(
        ids=ids[inicio:fin],
        embeddings=embeddings[inicio:fin],
        documents=documents[inicio:fin],
        metadatas=metadatas[inicio:fin],
    )
```

---

## 5) Idempotencia y errores frecuentes

| Situación | Síntoma | Qué hacer |
|-----------|---------|-----------|
| Reindexar sin borrar | Error de ID duplicado | `--recreate-index` o borrar `chroma_db/` |
| Dimensiones distintas | Error al `add` | Mismo `EMBEDDING_MODEL` en todo el pipeline |
| Metadata con `None` | Error de tipo | Sanitizar en `index.py` |
| Índice vacío | `count() == 0` | Verificar `MAX_CHUNKS_EMBED` y que exista `embeddings.json` |

---

## 6) Comando de ejecución

A continuación se muestran los comandos típicos para ejecutar el index.py:

```bash
# Tras preparar embeddings (S8)
python main.py --prepare

# Solo indexar
python main.py --index

# Preparar + indexar
python main.py --prepare --index
```

Tras indexar, inspecciona:

```bash
python main.py --index   # muestra count al final
```

---

## 7) Qué sigue

Con la colección indexada, el Bloque 2 implementa **retrieval**: embeddear la pregunta del usuario y ejecutar `collection.query()`.

Todavía **no** construyes el prompt ni llamas a Gemini para responder. Ahora mismo estamos en la fase de indexación, que es la primera parte de RAG. La siguiente parte es la retrieval, que es la parte de RAG que se encarga de buscar los chunks más relevantes para la pregunta.

---

## Resumen

- Indexar = cargar vectores ya calculados en Chroma con su texto y metadata.
- Usa lotes, IDs únicos y metadatos compatibles con Chroma.
- Reindexa cuando cambies chunking, corpus o modelo de embedding.

**Workout:** [01_crear_base_vectorial_chromadb.ipynb](../../02_Workout/01_Bases_de_datos_vectoriales/01_crear_base_vectorial_chromadb.ipynb) — genera `02_Workout/output/` (autocontenido). En el proyecto modular: `index.py` / `python main.py --index`.
**Siguiente bloque:** [Bloque 2 — Retrieval](../02_Retrieval_y_busqueda_semantica/readme.md)
