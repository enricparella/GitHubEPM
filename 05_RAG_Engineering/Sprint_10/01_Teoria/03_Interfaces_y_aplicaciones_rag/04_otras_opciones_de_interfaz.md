![Cabecera](../../assets/cabecera_rag.png)

# Otras opciones de interfaz

## Objetivos

- Conocer alternativas a Streamlit sin implementarlas todas.
- Entender por qué Streamlit es la opción del bootcamp en este sprint.
- Ver el puente hacia backends más elaborados (p. ej. agentes en Sprint 11+) con la misma UI.

---

## 1) Panorama

| Opción | Cuándo tiene sentido | En este sprint |
|--------|----------------------|----------------|
| **Streamlit** | Demo rápida, POC, herramientas internas | ✅ Implementamos |
| **Gradio** | Demos ML / Hugging Face, widgets mínimos | Solo mención |
| **API + cliente** | Producto con HTTP y front/móvil separados | Solo mención |
| **Notebook interactivo** | Exploración, no producto | Ya lo usas en workouts |

### Gradio (idea)

Similar a Streamlit: Python → UI. Muy habitual en demos de modelos. El patrón sigue siendo «una función, una interfaz»:

```python
# Conceptual
gr.Interface(fn=lambda q: responder(q)["respuesta"], inputs="text", outputs="text")
```

### FastAPI (idea)

Expone `POST /ask` (u otro endpoint) que llama a la misma función de negocio. El frontend (React, etc.) o cualquier cliente HTTP es **otro** proyecto. Más trabajo, más control: típico de **producto**, no de la primera demo del módulo.

---

## 2) Por qué Streamlit aquí

- Encaja con el stack Python del bootcamp.
- Pocas líneas hasta una URL usable en local.
- Suficiente para enseñar **UI vs lógica**.
- Encaja con el objetivo del sprint: MVP demostrable sobre un sistema ya construido.

No es «la única opción del mercado»: es la **decisión pedagógica** de este bloque.

---

## 3) Evolución del backend (Sprint 11+)

```text
Sprint 10                     Sprint 11+
─────────                     ──────────
Streamlit                     Streamlit (puede quedar)
   ↓                             ↓
logic.responder()             Agente (u otro orquestador)
   ↓                             ↓
RAG directo                   Tools (RAG, búsqueda, APIs…)
```

La interfaz no tiene por qué cambiar: cambia **quién** decide cuándo llamar al retrieval y con qué herramientas.

Por eso importa el contrato limpio (`responder()`, `agent.run()`, etc.): la UI no se acopla al detalle interno.

---

## 4) Qué practicar en el workout

1. Notebook / guía: montar o entender `app.py`.
2. Lanzar `streamlit run app.py` con el sistema listo en consola.
3. Probar una pregunta «buena» y un caso de abstención (q5).
4. Abrir el expander de contexto y relacionarlo con el retrieval (S9).

Proyecto y repo: [02_proyecto_rag_aplicacion.md](../../02_Workout/03_Interfaces_y_aplicaciones_rag/02_proyecto_rag_aplicacion.md).

---

## Resumen

- Streamlit = protagonista; Gradio / API + cliente = panorama.
- Misma UI puede sobrevivir cuando el backend pase a agente u otro orquestador.
- Workout: [01_crear_interfaz_streamlit_rag.ipynb](../../02_Workout/03_Interfaces_y_aplicaciones_rag/01_crear_interfaz_streamlit_rag.ipynb).
