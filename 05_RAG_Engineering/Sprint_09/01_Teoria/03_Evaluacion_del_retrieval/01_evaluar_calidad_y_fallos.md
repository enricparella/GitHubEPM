![Cabecera](../../assets/cabecera_rag.png)

# Evaluar calidad del contexto y casos de fallo

## Objetivos

- Evaluar retrieval de forma **cualitativa** con preguntas de prueba.
- Reconocer **síntomas** y causas probables.
- Usar distancias como ayuda, no como verdad absoluta.

---

## 1) Cómo evaluar la calidad del contexto recuperado

No necesitas métricas académicas (MRR, nDCG) para empezar. Sí necesitas **rigor manual**:

1. Define 5–10 preguntas representativas.
2. Ejecuta el [Workout 3](../../../02_Workout/03_Evaluacion_del_retrieval/01_evaluar_y_ajustar_retrieval.ipynb) o tu script / `python main.py --eval` en el proyecto modular.
3. Para cada pregunta, marca:
   - ¿El chunk #1 es relevante?
   - ¿Algún chunk del top-K contiene la respuesta?
   - ¿La fuente (`metadata.source`) es la esperada?

Ejemplo en `02_Workout/queries/preguntas_eval.json` (y copia equivalente en el proyecto modular).

| id | pregunta | fuente esperada (orientativa) |
|----|----------|----------------------------|
| q1 | ¿Qué significa GRATUITO? | FAQ |
| q2 | ¿Hay cine gratuito? | CSV eventos |
| q3 | ¿Qué hay en El Retiro? | CSV / eventos RETIRO |
| q4 | ¿Qué hay en Hortaleza? | CSV / eventos HORTALEZA |
| q5 | ¿Qué significan los campos de la agenda cultural? | FAQ |

---

## 2) Calidad del contexto recuperado

Preguntas que hacerte al inspeccionar el contexto:

- **Cobertura:** ¿Aparece la información necesaria en algún fragmento?
- **Precisión:** ¿El primer resultado es el más útil o hay ruido?
- **Redundancia:** ¿Varios chunks repiten lo mismo sin aportar?
- **Trazabilidad:** ¿Puedes citar `source` y `chunk_index`?

Contexto **bueno** para Sprint 10: fragmentos que contienen hechos del corpus, ordenados por relevancia, con fuentes claras. Esto es importante para que el LLM pueda entender el contexto y responder la pregunta.

---

## 3) Casos donde falla el retrieval

| Síntoma | Causa probable | Capa a tocar |
|---------|----------------|--------------|
| Respuesta partida entre chunks | `CHUNK_SIZE` pequeño o corte malo | chunking |
| Pregunta con sinónimos no recupera | Índice pequeño (`MAX_CHUNKS_EMBED`) o K bajo | config + K |
| Devuelve FAQ cuando querías eventos | Ambigüedad semántica; K alto mezcla fuentes | K, pregunta más específica |
| Nada relevante | Pregunta fuera de corpus o índice incompleto | datos / cobertura |
| Distancia muy similar en todos | Chunks genéricos o embed poco discriminativo | chunking / corpus |

---

## 4) Distancias: qué mirar

- Compara **orden relativo** entre chunks, no el valor absoluto.
- Si el primer chunk y el segundo chunk están muy cerca, puede haber **empate** semántico: revisa ambos.
- Si todas las distancias son altas, la pregunta puede estar **lejos del corpus**.

---

## 5) Preguntas «trampa» útiles

- «¿Cuál es la capital de Francia?» → no está en agenda Madrid; deberías ver chunks irrelevantes (prueba de humildad del sistema).
- «cine» (una palabra) → demasiado vaga; observa la dispersión de resultados.
- Pregunta en inglés sobre dataset en español → prueba límites del embedding multilingüe.

---

## Resumen

- Evalúa con preguntas fijas y revisión manual del contexto.
- Clasifica fallos por capa: chunking, K, índice, pregunta.
- Las distancias ayudan a ordenar; la relevancia la juzgas tú con el texto.
