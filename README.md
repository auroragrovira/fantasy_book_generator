# Generador de Libros de Fantasía Recursivo

Este proyecto contiene un conjunto de herramientas para generar historias infinitas y crear datasets de entrenamiento utilizando modelos de lenguaje locales (LLMs) vía Ollama.

## 🔮 Funcionalidades

### 1. Escritura Infinita (`libro_fantasy.py`)
Un guionista automático que nunca se detiene.
- Generación Recursiva: Crea una historia, la divide en fragmentos, refina cada párrafo y luego lo expande añadiendo nuevos eventos.
- Ciclo Infinito: El script está diseñado para escribir indefinidamente, aumentando el tamaño del libro hasta alcanzar un límite (300KB por defecto).
- Modelos Locales: Usa Ollama (por defecto `llama3.2` o `salamandra`) corriendo en `localhost:11434`.

### 2. Creación de Datasets
Herramientas para convertir libros en datos de entrenamiento para IAs.
- `totxt.py`: Convierte PDFs y DOCX a texto plano limpio.
- `creador_dataset_recursivo.py`: Lee los libros y genera pares `input` -> `output` en formato `.jsonl`, ideal para hacer *fine-tuning* de modelos.

### 3. Limpieza
- `recoge_llm_infinito.py`: Limpia la "basura" que a veces dejan los modelos (como etiquetas `assistant:`) del texto final.

## 🛠️ Requisitos

- Ollama: Debe estar instalado y ejecutándose en tu máquina.
  ```bash
  ollama serve
  ```
- Modelos: Debes tener descargados los modelos que usa el script (ej. `ollama pull llama3.2`).
- Python: Librerías `requests`, `PyPDF2`, `python-docx`.

## 📂 Uso Básico

1. Generar un libro:
   ```bash
   python libro_fantasy.py
   ```
2. Crear dataset de entrenamiento:
   Coloca tus libros `.txt` en la carpeta `libros/` y ejecuta:
   ```bash
   python creador_dataset_recursivo.py
   ```
