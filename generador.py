import os
import json
import google.generativeai as genai
import time
import random

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    exit(1)

genai.configure(api_key=api_key)

def limpiar(t):
    if not t: return ""
    return t.lower().strip().replace('á','a').replace('é','e').replace('í','i').replace('ó','o').replace('ú','u').replace('ü','u')

def generar_rosco_ia():
    model = genai.GenerativeModel('gemini-1.5-flash')
    letras = "ABCDEFGHIJLMNOPQRSTUVXYZ"
    rosco_final = []

    # BANCO SEGURO (Plan B) - Cada uno TIENE su letra
    banco = {
        "A": {"letra":"A", "pregunta":"Aeronave que vuela.", "respuesta":"avion", "tipo":"CON LA"},
        "B": {"letra":"B", "pregunta":"Mamifero marino gigante.", "respuesta":"ballena", "tipo":"CON LA"},
        "C": {"letra":"C", "pregunta":"Lugar donde vives.", "respuesta":"casa", "tipo":"CON LA"},
        "D": {"letra":"D", "pregunta":"Cubo para jugar.", "respuesta":"dado", "tipo":"CON LA"},
        "E": {"letra":"E", "pregunta":"Animal con trompa.", "respuesta":"elefante", "tipo":"CON LA"},
        "F": {"letra":"F", "pregunta":"Torre con luz en el mar.", "respuesta":"faro", "tipo":"CON LA"},
        "G": {"letra":"G", "pregunta":"Animal que maulla.", "respuesta":"gato", "tipo":"CON LA"},
        "H": {"letra":"H", "pregunta":"Agua helada.", "respuesta":"hielo", "tipo":"CON LA"},
        "I": {"letra":"I", "pregunta":"Tierra en el mar.", "respuesta":"isla", "tipo":"CON LA"},
        "J": {"letra":"J", "pregunta":"Cuello muy largo.", "respuesta":"jirafa", "tipo":"CON LA"},
        "L": {"letra":"L", "pregunta":"Brilla de noche.", "respuesta":"luna", "tipo":"CON LA"},
        "M": {"letra":"M", "pregunta":"Fruta roja.", "respuesta":"manzana", "tipo":"CON LA"},
        "N": {"letra":"N", "pregunta":"Color de la noche.", "respuesta":"negro", "tipo":"CON LA"},
        "O": {"letra":"O", "pregunta":"Para escuchar.", "respuesta":"oido", "tipo":"CON LA"},
        "P": {"letra":"P", "pregunta":"Animal que ladra.", "respuesta":"perro", "tipo":"CON LA"},
        "Q": {"letra":"Q", "pregunta":"Comida de leche.", "respuesta":"queso", "tipo":"CON LA"},
        "R": {"letra":"R", "pregunta":"Marca las horas.", "respuesta":"reloj", "tipo":"CON LA"},
        "S": {"letra":"S", "pregunta":"Estrella caliente.", "respuesta":"sol", "tipo":"CON LA"},
        "T": {"letra":"T", "pregunta":"Va por railes.", "respuesta":"tren", "tipo":"CON LA"},
        "U": {"letra":"U", "pregunta":"Fruta del vino.", "respuesta":"uva", "tipo":"CON LA"},
        "V": {"letra":"V", "pregunta":"Hace calor.", "respuesta":"verano", "tipo":"CON LA"},
        "X": {"letra":"X", "pregunta":"Instrumento de madera.", "respuesta":"xilofono", "tipo":"CON LA"},
        "Y": {"letra":"Y", "pregunta":"Amarillo del huevo.", "respuesta":"yema", "tipo":"CON LA"},
        "Z": {"letra":"Z", "pregunta":"Protege el pie.", "respuesta":"zapato", "tipo":"CON LA"}
    }

    for l in letras:
        exito = False
        try:
            prompt = f"Pregunta Pasapalabra letra {l}. JSON: {{\"letra\":\"{l}\", \"pregunta\":\"...\", \"respuesta\":\"...\", \"tipo\":\"CON LA\"}}"
            res = model.generate_content(prompt)
            data = json.loads(res.text.replace("```json", "").replace("```", "").strip())
            # Validamos que la respuesta contenga la letra
            resp_limpia = limpiar(data['respuesta'])
            if (data['tipo'] == "CON LA" and resp_limpia.startswith(l.lower())) or (l.lower() in resp_limpia):
                rosco_final.append(data)
                exito = True
        except: pass
        
        if not exito:
            rosco_final.append(banco[l])

    with open('preguntas.json', 'w', encoding='utf-8') as f:
        json.dump(rosco_final, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    generar_rosco_ia()
