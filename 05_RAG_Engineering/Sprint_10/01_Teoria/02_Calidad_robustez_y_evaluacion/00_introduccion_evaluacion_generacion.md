![Cabecera](../../assets/cabecera_rag.png)

# Introducción: evaluación de respuestas generadas

En el Sprint 9 evaluaste **si el retrieval devolvía buenos chunks**. En este bloque evalúas **si la respuesta final es correcta, útil y fiable**.

> Un retrieval perfecto **no garantiza** una buena respuesta: el LLM puede ignorar el contexto, mezclar ruido o inventar.

---

## Objetivos del bloque

Al terminar, deberías poder:

- Diferenciar evaluación de **retrieval** vs evaluación de **generación**.
- Aplicar criterios: exactitud, relevancia, coherencia, trazabilidad.
- Detectar alucinaciones y casos donde debe **abstenerse**.
- Proponer ajustes (prompt, top-K, chunking) según el tipo de fallo.

---

## Retrieval vs generación

| | Sprint 9 | Sprint 10 (este bloque) |
|--|----------|-------------------------|
| **Qué miras** | Chunks recuperados | Texto de la respuesta |
| **Pregunta clave** | ¿Llegó la evidencia correcta? | ¿El LLM usó bien esa evidencia? |
| **Herramienta** | `--eval`, distancias, fuentes | Rúbrica + `--ask` + `preguntas_eval.json` |
| **Fallo típico** | Top-K malo, chunking, índice incompleto | Alucinación, ruido, prompt permisivo |

Puedes tener:

- Retrieval **bueno** + respuesta **mala** (prompt flojo o modelo que inventa).
- Retrieval **malo** + respuesta «bonita» pero **incorrecta** (alucinación con estilo).

Por eso se evalúan **por separado** y después juntos.

---

## Dataset de evaluación

En `02_Workout/queries/preguntas_eval.json` (y copia en el proyecto) cada pregunta puede llevar:

| Campo | Uso |
|-------|-----|
| `fuente_esperada` | Orientativa (igual que S9) |
| `respuesta_esperada` | Criterio manual de acierto |
| `deberia_abstenerse` | `true` si no hay evidencia en el corpus |
| `notas` | Caso pedagógico |

La pregunta q5 («¿Cuál es la capital de Francia?») es el ancla de **abstención**.

---

## Salida del bloque

Un hábito de ingeniero RAG:

1. Ejecutar un set fijo de preguntas.
2. Clasificar cada respuesta (acierto / parcial / fallo / alucinación / abstención).
3. Decidir **qué capa tocar** (retrieval, prompt, validación, datos).

Lo practicarás en el [workout](../../02_Workout/02_Calidad_robustez_y_evaluacion/01_evaluar_respuestas_rag.ipynb).

---

## Resumen

- S9 midió contexto; S10 mide **respuesta**.
- Un buen chunk no basta si el prompt no obliga a grounding.
- Siguiente: [Cómo evaluar respuestas RAG](./01_como_evaluar_respuestas_rag.md).
