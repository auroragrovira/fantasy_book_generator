import os
import time
import requests
import json
import random

def query_llm(llm_url, model, prompt, temp=0.7):
    """Realiza una consulta al modelo de lenguaje con manejo de errores."""
    print(f"Consultando modelo {model}...")
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "options": {"temperature": temp},
        "stream": True
    }
    try:
        response = requests.post(llm_url, json=payload, stream=True)
        response.raise_for_status()
        
        output = ""
        for line in response.iter_lines():
            if line:
                try:
                    body = json.loads(line.decode('utf-8'))
                    if "error" in body:
                        raise RuntimeError(f"Error del servidor: {body['error']}")
                    if "message" in body:
                        content = body["message"].get("content", "")
                        output += content + " \n"
                    if body.get("done", False):
                        break
                except json.JSONDecodeError:
                    print("Error al decodificar la respuesta JSON del servidor.")
        return format_text(output)
    except requests.RequestException as e:
        print(f"Error en la consulta al LLM: {e}")
        return ""

def format_text(text):
    lines = text.split("\n")
    result = []
    current_word = ""

    for line in lines:
        if line.startswith(" "):
            if current_word:
                result.append(current_word)
            current_word = line.strip()
        else:
            current_word += line.strip()

    if current_word:
        result.append(current_word)
    return " ".join(result)

def save_text(filename, text):
    """Guarda el texto en un archivo."""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(text)

def load_text(filename):
    """Carga el texto desde un archivo."""
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()

def split_text_into_chunks(text, chunk_size=150):
    """Divide el texto en fragmentos de tamaño determinado."""
    words = text.split()
    return [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

def refine_chunks(chunks, llm_url, models):
    """Reescribe cada fragmento usando dos modelos elegidos aleatoriamente y contexto adicional."""
    refined_chunks = []
    model = random.choice(models)  # Escoge 2 modelos al azar
    print(f"Modelo seleccionado para refinamiento: {model}")

    for i, chunk in enumerate(chunks):
        context_prev = chunks[i-1] if i > 0 else ""
        prompt = "Redacta mejor este texto: " + chunk + "teniendo en cuenta que venimos de aquí: " + context_prev + ". Devuelve unicamente el texto refinado directamente, devuelvelo como texto plano para copiar en un txt"

        print(f"Refinando trozo {i+1}/{len(chunks)} con {model}...")
        new_chunk = query_llm(llm_url, model, prompt, temp=0.3)
        if new_chunk:
            chunk = new_chunk  # Reemplaza con la versión refinada

        refined_chunks.append(format_text(chunk))
        save_text(f"chunk_{i}.txt", chunk)  # Guarda cada fragmento en un archivo temporal

    return refined_chunks


def expand_chunks(chunks, llm_url, models):
    """Expande cada fragmento para triplicar su tamaño con contexto adicional."""
    expanded_chunks = []
    for i, chunk in enumerate(chunks):
        model = random.choice(models)  # Escoge 2 modelos al azar
        print(f"Modelo seleccionado para expandir: {model}")
        context_prev = load_text(f"chunk_{i-1}.txt") if i > 0 else ""
        context_next = load_text(f"chunk_{i+1}.txt") if i < len(chunks)-1 else ""
        
        if i % 31 == 0:
            prompt_type = "Revela un evento impactante y crucial para la historia y expande el texto"
        elif i % 19 == 0:
            prompt_type = "Introduce un evento disruptivo que cambie la dirección de la historia expandiendo el texto"
        elif i % 2 == 0:
            prompt_type = " Progresa con la historia aumentando el texto"
        else:
            prompt_type = "Redacta mejor y alarga la siguiente siguiente historia"

        prompt = f"{prompt_type} hasta 750 palabras:\n\n[CON TEXTO ADICIONAL]\n{context_prev}\n[ACTUAL]\n{chunk}\n[SIGUIENTE]\n{context_next}"
        
        print(f"Expandiendo trozo {i+1}/{len(chunks)} con {model}...")
        expanded_chunk = query_llm(llm_url, model, prompt, temp=0.7)
        if expanded_chunk:
            expanded_chunks.append(format_text(expanded_chunk))
        else:
            expanded_chunks.append(chunk)  # En caso de error, conservar el original
        save_text(f"chunk_{i}.txt", expanded_chunks[-1])  # Guardar fragmentos expandidos en archivos
    return expanded_chunks

def main():
    llm_url = "http://127.0.0.1:11434/api/chat"
    models = ["llama3.2", "hdnh2006/salamandra-2b-instruct", ]
    filename = "fantasy_book-4.txt"
    
    if not os.path.exists(filename):
        print("Generando texto inicial...")
        model = random.choice(models)  # Escoge 2 modelos al azar
        print(f"Modelo seleccionado para generacion inicial: {model}")
        initial_text = query_llm(llm_url, model, "Escribe una historia de fantasía sobre Aria, una aprendiz de hechicera")
        if initial_text:
            save_text(filename, format_text(initial_text))
            print("Texto inicial guardado.")
        else:
            print("Error: No se pudo generar el texto inicial.")
            return
    
    while os.path.getsize(filename) < 300000:
        print("Cargando texto actual...")
        text = load_text(filename)
        if not text.strip():
            print("Error: El archivo de texto está vacío.")
            break
        
        print("Dividiendo texto en fragmentos...")
        chunks = split_text_into_chunks(text)
        print(f"{len(chunks)} fragmentos generados.")
        
        refined_chunks = refine_chunks(chunks, llm_url, models)
        print("Refinamiento completado.")

        save_text(filename, "\n".join(refined_chunks))
        print(f"Texto actualizado guardado en {filename}.")

        print("Dividiendo texto en fragmentos...")
        chunks = split_text_into_chunks(text)
        print(f"{len(chunks)} fragmentos generados.")
        
        expanded_chunks = expand_chunks(chunks, llm_url, models)
        print("Expansión completada.")
        
        save_text(filename, "\n".join(expanded_chunks))
        print(f"Texto actualizado guardado en {filename}.")
        
        time.sleep(2)  # Evita sobrecargar el servidor

if __name__ == "__main__":
    main()
