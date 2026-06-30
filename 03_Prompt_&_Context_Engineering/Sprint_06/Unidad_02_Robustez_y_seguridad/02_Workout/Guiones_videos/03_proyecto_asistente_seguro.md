# Guión — Proyecto Asistente Seguro (Robustez y Seguridad)

**Material:** repositorio [Sprint06_Unidad02_Asistentes_Robustez_y_Seguridad](https://github.com/aie-online-tb/Sprint06_Unidad02_Asistentes_Robustez_y_Seguridad) (VS Code o Codespaces)

**Duración total aproximada:** ~14 min

> **Rol del vídeo:** orientar, ejecutar la comparativa y dar el mapa de las cinco capas. El **README del repo** es la guía en profundidad.
>
> **Inicio de la grabación:** VS Code ya abierto con el proyecto clonado (no se graba el `git clone`).

---

## Apertura y dominio (~1,5 min)

- Workout: un **tutor Python** que compara lado a lado un pipeline **vulnerable** y uno **seguro** con los mismos tres mensajes de prueba.
- **Prerrequisito (solo mencionar):** clonar desde `https://github.com/aie-online-tb/Sprint06_Unidad02_Asistentes_Robustez_y_Seguridad` o abrir con el **launcher Codespaces** del campus.
- Concepto central: **defensa en capas** — rechazar, acotar y estructurar **antes** del modelo, validar la salida **después**. Si una capa detiene el flujo, las siguientes no se ejecutan.
- *"README = profundidad; vídeo = situar y ejecutar."*
- Muestra el explorador con el proyecto cargado.

---

## Preparar el entorno (~1,5 min)

**Contexto:** terminal en la raíz del repo (donde está `main.py`).

1. `python -m venv .venv` → activar (PowerShell / Bash).
2. `pip install -r requirements.txt` (`google-genai`, `python-dotenv`).
3. `cp .env.example .env` y editar la API key, **o** dejar `getpass` al ejecutar.
4. Intérprete `.venv` en VS Code.

---

## Ejecutar primero (~2 min)

- `python main.py`.
- Comenta la salida **sin abrir código** todavía. Para cada uno de los tres casos, señala solo la diferencia clave:
  - **Caso 1 (pregunta legítima):** ambos modos responden, pero el seguro devuelve JSON con `in_scope`, `category` y `answer`.
  - **Caso 2 (fuera de dominio — mundial):** el modo vulnerable contesta de fútbol; el seguro devuelve rechazo **sin llamar a Gemini** (`metricas: None`).
  - **Caso 3 (inyección — "Ignora instrucciones"):** el modo vulnerable puede salir del rol; el seguro rechaza **antes del modelo** con lista de patrones detectados.
- Frase ancla: *"Fíjate sobre todo en qué capa detiene el flujo, no solo en si la respuesta es correcta."*

---

## README del repo (~1 min)

- Abre `README.md` y señala el diagrama de las **cinco capas** (`validate_input` → dominio → prompt seguro → Gemini → parseo de salida).
- Señala la tabla "Dos modos: vulnerable vs seguro" y la sección de experimentos.
- *"Profundidad en el README. Aquí solo el mapa."*

---

## Tour de código — 3 paradas (~6 min)

### Parada A — `config.py` + `validators.py` (~2 min)

- Abre `config.py`: señala `SYSTEM_PROMPT`, `DOMINIO_KEYWORDS`, `PATRONES_SOSPECHOSOS` y `MAX_INPUT_CHARS`. Una frase: *"Todo lo que define qué está permitido vive aquí, en constantes que el usuario no puede tocar."*
- Abre `validators.py`:
  - `validate_input()`: comprueba vacío, longitud y patrones sospechosos. Devuelve **lista de errores** (vacía = OK). Enlaza con el Caso 3 del terminal: "Ignora instrucciones" disparó esta función antes de llegar al modelo.
  - `parece_dominio_python()`: una línea. Enlaza con el Caso 2: el mundial no pasó este filtro.
  - Una frase: *"Estas son las capas 1 y 2. Si fallan, no se llama a Gemini."*

### Parada B — `prompts.py` + `gemini_client.py` (~2 min)

- Abre `prompts.py`: contrasta `build_vulnerable_prompt` (todo mezclado) y `build_secure_prompt` (`SYSTEM_PROMPT` + hint JSON + delimitadores). Muestra los delimitadores en pantalla. Esto es la **capa 3**.
- Abre `gemini_client.py`: señala `llamar_gemini` (texto libre, modo vulnerable) y `llamar_gemini_json` (`response_mime_type="application/json"`, modo seguro). Menciona `safe_generate`: cuenta tokens antes de llamar; si supera `MAX_TOKENS_INPUT`, rechaza sin gastar tokens. Esto es la **capa 4**.

### Parada C — `logic.py` + `main.py` (~2 min)

- Abre `logic.py` y scroll por los dos pipelines:
  - `procesar_turno_vulnerable`: solo rechaza vacío → prompt mezclado → texto libre → sin validación de salida.
  - `procesar_turno_seguro`: `validate_input` → dominio → prompt seguro → `safe_generate` json → `parsear_respuesta_tutor` exige claves (`in_scope`, `category`, `answer`). Esto es la **capa 5**.
  - Una frase: *"La diferencia no es el modelo; es el pipeline que lo rodea."*
- Scroll rápido por `main.py`: tres casos definidos en `CASOS`, misma función `imprimir_resultado` para ambos modos. No leas caso por caso.

---

## Demo: añadir patrón sospechoso (~1 min)

- En `config.py`, añade `"actúa como"` a `PATRONES_SOSPECHOSOS` si no está, o añade una cadena nueva (p. ej. `"sin límites"`).
- En `main.py`, añade un cuarto caso con ese patrón en el mensaje.
- Reejecuta `python main.py` y muestra que el modo seguro lo rechaza en la capa 1 **sin llamar al modelo**.
- *"Endurecer el filtro es tocar una lista en `config.py`."*

---

## Cierre (~1 min)

- Resume las cinco capas de memoria: validate → dominio → prompt → Gemini → parseo.
- Idea clave: **no confiar** en que el LLM "se portará bien" por sí solo; las defensas van en el código que lo rodea.
- Menciona las limitaciones del README: filtros por keywords tienen falsos positivos; esto es material de bootcamp, no un sistema de producción.
- Invita al README completo y a los experimentos (comentar `validate_input`, cambiar delimitadores, romper el JSON).
