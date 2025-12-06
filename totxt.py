import os
from PyPDF2 import PdfReader
import docx
import re

def read_pdf(file_path):
    """Convierte un archivo PDF a texto."""
    try:
        reader = PdfReader(file_path)
        text = "".join(page.extract_text() for page in reader.pages if page.extract_text())
        return text
    except Exception as e:
        print(f"Error al leer PDF {file_path}: {e}")
        return None

def read_docx(file_path):
    """Convierte un archivo DOCX a texto."""
    try:
        doc = docx.Document(file_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs if paragraph.text])
        return text
    except Exception as e:
        print(f"Error al leer DOCX {file_path}: {e}")
        return None

def convert_to_txt_and_cleanup(folder_path):
    """Convierte archivos PDF y DOCX en una carpeta a archivos TXT y elimina los originales."""
    if not os.path.exists(folder_path):
        print(f"La carpeta {folder_path} no existe.")
        return

    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            if file_name.endswith(".pdf"):
                text = read_pdf(file_path)
            elif file_name.endswith(".docx"):
                text = read_docx(file_path)
            else:
                continue

            if text:
                txt_file_name = os.path.splitext(file_name)[0] + ".txt"
                txt_file_path = os.path.join(folder_path, txt_file_name)
                try:
                    with open(txt_file_path, "w", encoding="utf-8") as txt_file:
                        txt_file.write(text)
                    print(f"Archivo convertido: {txt_file_path}")
                    # Eliminar el archivo original
                    os.remove(file_path)
                    print(f"Archivo original eliminado: {file_path}")
                except Exception as e:
                    print(f"Error al escribir el archivo TXT {txt_file_name}: {e}")

def clean_text(text):
    # Reemplazar múltiples tabulaciones y espacios por un solo espacio
    cleaned_text = re.sub(r'\s+', ' ', text)
    
    # Restaurar saltos de línea después de títulos y párrafos
    cleaned_text = re.sub(r'(\bIntroducción\b)', '\n\n\1', cleaned_text)
    
    return cleaned_text.strip()

def process_books(folder_path):
    output_folder = "./libros"
    os.makedirs(output_folder, exist_ok=True)
    
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            input_path = os.path.join(folder_path, filename)
            output_path = os.path.join(output_folder, filename)
            
            with open(input_path, "r", encoding="utf-8") as f:
                raw_text = f.read()
            
            formatted_text = clean_text(raw_text)
            
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(formatted_text)
            
            print(f"Texto formateado guardado en {output_path}")



if __name__ == "__main__":
    folder_path = "./libros"
    for folder in [folder_path]:
        convert_to_txt_and_cleanup(folder)
        process_books(folder)
