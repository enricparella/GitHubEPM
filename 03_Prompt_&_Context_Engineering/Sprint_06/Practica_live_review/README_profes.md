# Guion profes — Live Review Sprint 06

**Proyecto:** `01_tutor_bootcamp`  
**Sesiones:** 2 × 2 h  
**Referencia:** `01_tutor_bootcamp_SOLUTION/`  
**Publicar a alumnos:** solo la carpeta **base** (no la SOLUTION).

---

## Objetivo pedagógico

Que el alumno **estructure** un asistente mantenible (U1) y lo **endurezca** con defensas en capas (U2).

**No** es repetir el Sprint 5 (clasificación JSON, chat desde cero). El código de FAQ e historial básico viene **dado**.

Evaluar:

- Separación `config` / `state` / `prompts` / `logic` / `validators` / `main`
- Perfiles distintos con la misma pregunta
- Memoria de sesión sin LLM (`actualizar_perfil_desde_mensaje`)
- Validación **antes** de llamar al modelo (inyección, dominio)
- Prompt seguro con delimitadores + JSON validado en Python

---

## Sesión 1 (2 h) — Fase 1: Arquitectura

### 0:00–0:15 — Arranque

- Mensaje clave: *“No otro chatbot; estructurar el sistema.”*
- Tour de archivos (tabla README + sección «Código dado»).
- Ejecutar `python main.py` en común: demo 0 OK, `[PENDIENTE — arquitectura]`.

### 0:15–0:30 — Código dado

- Explicar en pizarra `seleccionar_faq` y `ultimos_n` (10 min, **sin reimplementar**).
- Pregunta: ¿por qué no metemos todo el FAQ en el prompt?

### 0:30–0:50 — `state.py`

**Archivo:** `actualizar_perfil_desde_mensaje`

- Extracción sin LLM; enlace con demo 2 (“¿cómo me llamo?”).
- Criterio: tras turno 1, `user_profile["nombre"] == "Ana"`.

### 0:50–1:25 — `prompts.py`

**Archivos:** `build_faq_block`, `build_history_block`, `build_assistant_prompt`

- Rol del perfil vs instrucciones fijas.
- Ensamblar bloques; no hardcodear FAQ entero.
- Probar mentalmente con `perfil_activo="junior"` vs `"senior"`.

### 1:25–1:50 — `logic.py`

**Archivo:** `procesar_turno` (helpers `crear_estado_demo` y `demo_seleccion_faq` ya vienen en la base)

- Orden: Gemini OK → **después** actualizar state.
- `respuesta_ok` / `respuesta_error` ya existen.

### 1:50–2:00 — Cierre Fase 1

- Checklist Fase 1 del README.
- Demos 1–3 sin `[PENDIENTE — arquitectura]`.

**Errores frecuentes:**

- Historial actualizado antes de saber si Gemini respondió
- Olvidar `assistant_config` distinto en demo perfiles
- `print` en logic en lugar de devolver dict

---

## Sesión 2 (2 h) — Fase 2: Robustez y seguridad

### 0:00–0:15 — Repaso arquitectura

- Repaso general de la práctica.
- Recordar: `logic` devuelve dict, `main` imprime.

### 0:15–0:45 — `validators.py`

**Archivos:** `validate_input`, `parece_dominio_python`, `rechazo_fuera_de_dominio`

- Pregunta central: ¿por qué rechazamos **sin** llamar a Gemini?
- Probar inyección y fútbol en consola Python antes del pipeline completo.

### 0:45–1:10 — `prompts.py` (seguridad)

**Archivos:** `build_vulnerable_prompt`, `build_secure_prompt`

- Anti-patrón vs delimitadores + SYSTEM fijo.
- Enlace con notebook U2 si lo vieron.

### 1:10–1:45 — `logic.py` (seguridad)

**Archivos:** `parsear_respuesta_tutor`, `procesar_turno_vulnerable`, `procesar_turno_seguro`

- Demo 4 lado a lado.
- Inyección → `[ERROR]` seguro, **sin** `metricas`.
- Fútbol → seguro, `metricas: None`.

### 1:45–2:00 — Cierre sprint

- Tabla “qué archivo tocar para X”.
- Stretch: `validate_input` al inicio de `procesar_turno`.

**Errores frecuentes:**

- Llamar a Gemini antes de `validate_input`
- Dominio omitido → gasta tokens en fútbol
- Confiar solo en JSON del modelo sin `parsear_respuesta_tutor`

---

## Rúbrica rápida (pass / revisar)

| Criterio | Pass |
|----------|------|
| Capas separadas | config / state / prompts / logic / validators |
| Perfiles | Misma pregunta, respuesta distinta por perfil |
| Memoria | Recuerda nombre y tema en turno 3 |
| FAQ | 1 entrada en demo 3, no todo el JSON |
| Validación pre-LLM | Inyección rechazada sin métricas |
| Dominio | Fuera de Python/bootcamp sin llamada |
| Modularidad | Sin lógica de negocio en `main` |

---

## Si van muy justos de tiempo

**Priorizar Fase 1:** `build_assistant_prompt` → `procesar_turno` → demo perfiles + memoria.  
**Priorizar Fase 2:** `validate_input` → `procesar_turno_seguro` → demo 4 solo caso inyección.

**Recortar:** demo FAQ (3), tercer perfil en demo 1, caso fútbol en demo 4.

---

## Si van muy rápidos

- Unir Fase 1+2: `validate_input` al inicio de `procesar_turno`.
- Nuevo perfil en `PERFILES` + caso en `CASOS_SEGURIDAD`.
- Comentar `validate_input` en seguro y repetir ataque (efecto didáctico).



Tiempo estimado alumno (teoría + workouts hechos): **2–3 h** + 2 sesiones live.
