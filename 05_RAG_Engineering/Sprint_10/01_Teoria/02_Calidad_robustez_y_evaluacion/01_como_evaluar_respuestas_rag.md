![Cabecera](../../assets/cabecera_rag.png)

# Cómo evaluar respuestas RAG

## Objetivos

- Definir criterios prácticos para juzgar respuestas.
- Usar `preguntas_eval.json` con campos de generación.
- Documentar resultados sin automatizar demasiado al inicio.

---

## 1) Criterios prácticos

| Criterio | Pregunta que te haces |
|----------|------------------------|
| **Exactitud** | ¿Lo dicho está en el contexto / corpus? |
| **Relevancia** | ¿Responde a la pregunta formulada? |
| **Coherencia** | ¿Está bien redactado y es consistente? |
| **Trazabilidad** | ¿Puedes vincular afirmaciones a una fuente? |
| **Formato** *(si pides JSON)* | ¿Parsea? ¿Respeta el esquema? |

Un JSON **válido** no implica respuesta correcta: puede parsear y aun así alucinar. Evalúa formato y contenido por separado.

No necesitas LLM-as-judge ni métricas académicas para empezar. Sí necesitas **rigor manual** con un set fijo de preguntas.

---

## 2) Rúbrica orientativa

Para cada pregunta, marca un veredicto:

| Símbolo | Significado |
|---------|-------------|
| ✅ | Acierto: correcta y basada en el contexto |
| ⚠️ | Parcial: algo útil pero incompleto o ruidoso |
| ❌ | Fallo: no responde bien (sin inventar necesariamente) |
| 🛑 | Alucinación: inventa hechos no presentes |
| ⏸️ | Debería abstenerse (y lo hace, o debería) |

Ejemplo con el JSON del sprint:

| id | Pregunta | Qué esperas |
|----|----------|-------------|
| q1 | ¿Qué significa GRATUITO? | Explicación FAQ (1 vs 0) |
| q2 | ¿Hay cine gratuito en verano? | Eventos del CSV, con fuentes |
| q3 | ¿Actividades en el Retiro? | Eventos RETIRO / Retiro |
| q4 | ¿Para qué sirve el PDF? | Documentación, no listado de eventos |
| q5 | ¿Capital de Francia? | Abstención (`deberia_abstenerse: true`) |

---

## 3) Procedimiento recomendado

1. Indexa el corpus (`--prepare --index`) con el mismo `MAX_CHUNKS_EMBED` / config que uses en demo.
2. Para cada pregunta: `python main.py --ask "…"` (o el notebook).
3. Anota: veredicto, fuentes mostradas, si el contexto recuperado era bueno.
4. Si falla, **separa capas**:
   - ¿El contexto ya era malo? → vuelve a S9 (K, chunking, índice).
   - ¿El contexto era bueno y la respuesta mala? → prompt / temperatura / validación.

---

## 4) Tabla de resultados (plantilla)

| id | Veredicto | ¿Contexto OK? | ¿Fuentes OK? | Acción |
|----|-----------|---------------|--------------|--------|
| q1 | ✅ | Sí | Sí | — |
| q2 | ⚠️ | Sí | Parcial | Subir K o mejorar prompt de citas |
| q5 | 🛑 | Irrelevante | — | Endurecer prompt / abstención |

Guarda esta tabla en tus notas o en el notebook: es tu **baseline** antes de tocar parámetros.

---

## Resumen

- Criterios: exactitud, relevancia, coherencia, trazabilidad.
- Rúbrica manual + set fijo de preguntas.
- Separa fallos de retrieval y fallos de generación.
- Siguiente: [Alucinaciones y grounding](./02_hallucinations_y_grounding.md).
