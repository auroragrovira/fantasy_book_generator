import re

def limpiar_texto(input_file="cmd_output.txt", output_file="texto_limpio.txt"):
    """Elimina saltos de línea innecesarios y la etiqueta 'assistant:' del texto."""

    with open(input_file, "r", encoding="utf-8") as f:
        contenido = f.readlines()

    # Unir líneas eliminando saltos innecesarios
    texto = " ".join([line.strip() for line in contenido])

    # Eliminar cualquier "assistant:" en el texto
    texto_limpio = re.sub(r'\bassistant:\s*', '', texto)

    # Guardar el resultado en un nuevo archivo
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(texto_limpio)

    print(f"Texto limpio guardado en '{output_file}'")

# Ejecutar la limpieza en el archivo
limpiar_texto("texto1.txt", "texto_limpio.txt")


