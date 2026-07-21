![Cabecera](../../assets/cabecera_rag.png)

# 📘 Sprint 09 · Bloque 01

## Bases de datos vectoriales

En el Sprint 8 generaste **embeddings** y los guardaste en `embeddings.json`. Ahora aprendes a **persistirlos en una base vectorial** para buscar por similitud a escala.

> **¿Cómo almaceno conocimiento de forma que pueda recuperarse por similitud semántica?**

Salida de este bloque: una **colección ChromaDB** indexada con el corpus de la agenda cultural de Madrid.

---

## 📂 Contenido de la teoría (orden de lectura)

### 🧭 0. Introducción

🔗 [Abrir](./00_introduccion_bases_vectoriales.md)

* Puente desde Sprint 8
* Objetivo del bloque y artefactos de salida

---

### 🗄️ 1. BD vectorial vs tradicional

🔗 [Abrir](./01_bd_vectorial_vs_tradicional.md)

* Qué es una base de datos vectorial
* Por qué no basta SQL / búsqueda por keywords

---

### 💾 2. ChromaDB: persistencia y colecciones

🔗 [Abrir](./02_chromadb_persistencia_y_colecciones.md)

* Cliente persistente, colecciones
* Almacenamiento de embeddings, documentos y metadatos

---

### 📥 3. Flujo de indexación

🔗 [Abrir](./03_flujo_de_indexacion.md)

* De `embeddings.json` a `collection.add()`
* IDs, batches e idempotencia

---

## Workout (vídeo guiado)

| Recurso | Cubre |
|---------|--------|
| [01_crear_base_vectorial_chromadb.ipynb](../../02_Workout/01_Bases_de_datos_vectoriales/01_crear_base_vectorial_chromadb.ipynb) | ChromaDB + indexación |

El **proyecto modular** completo está en el [Bloque 3 — Evaluación del retrieval](../03_Evaluacion_del_retrieval/readme.md).
