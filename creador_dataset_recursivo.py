import os
import json

# Ruta donde están los archivos txt
ruta_txt = './libros'

# Ruta donde se guardará el dataset generado
ruta_dataset = 'dataset.jsonl'

def crear_dataset_desde_txt(ruta_txt, ruta_dataset):
    with open(ruta_dataset, 'w', encoding='utf-8') as json_file:
        # Leer cada archivo txt en la carpeta
        for archivo in os.listdir(ruta_txt):
            if archivo.endswith('.txt'):
                ruta_completa = os.path.join(ruta_txt, archivo)
                print(f"Procesando archivo: {archivo}")

                with open(ruta_completa, 'r', encoding='utf-8') as file:
                    texto = file.read().split()

                    prev_output = None
                    num_palabras = len(texto)

                    for i in range(0, num_palabras, 100):
                        input_text = prev_output if prev_output else ' '.join(texto[i:i+100])
                        output_text = ' '.join(texto[i+100:i+200])

                        if not output_text:
                            break

                        tupla = {"input": input_text, "output": output_text}
                        json_file.write(json.dumps(tupla, ensure_ascii=False) + '\n')

                        prev_output = output_text

                    # Añadir secuencia final al último output del documento
                    if prev_output:
                        tupla_final = {"input": prev_output, "output": "<final>"}
                        json_file.write(json.dumps(tupla_final, ensure_ascii=False) + '\n')

                print(f"Finalizado archivo: {archivo}")

if __name__ == "__main__":
    crear_dataset_desde_txt(ruta_txt, ruta_dataset)
    print("Dataset creado exitosamente.")