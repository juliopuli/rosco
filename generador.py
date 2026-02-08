import os
import json
import google.generativeai as genai
import time
import random
from datetime import datetime

# Configuración de seguridad
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("❌ ERROR: Falta la API KEY en los secretos de GitHub.")
    exit(1)

genai.configure(api_key=api_key)

def limpiar(t):
    if not t: return ""
    return t.lower().strip().replace('á','a').replace('é','e').replace('í','i').replace('ó','o').replace('ú','u').replace('ü','u')

def generar_rosco_ia():
    model = genai.GenerativeModel('gemini-1.5-flash')
    letras = "ABCDEFGHIJLMNOPQRSTUVXYZ"
    rosco_final = []

    # BANCO DE RESPALDO DE CALIDAD (Por si la IA no responde bien)
    backup_real = {
        "A": {"letra":"A", "pregunta":"Aparato con alas que vuela por el cielo movido por motores.", "respuesta":"avion", "tipo":"CON LA"},
        "B": {"letra":"B", "pregunta":"Mamífero marino de enorme tamaño que vive en todos los océanos.", "respuesta":"ballena", "tipo":"CON LA"},
        "C": {"letra":"C", "pregunta":"Edificio o parte de él que sirve de vivienda para una familia.", "respuesta":"casa", "tipo":"CON LA"},
        "D": {"letra":"D", "pregunta":"Pieza cúbica usada en juegos de azar que tiene puntos del uno al seis.", "respuesta":"dado", "tipo":"CON LA"},
        "E": {"letra":"E", "pregunta":"Animal mamífero con una larga trompa y grandes orejas.", "respuesta":"elefante", "tipo":"CON LA"},
        "F": {"letra":"F", "pregunta":"Torre alta con una luz potente que guía a los barcos de noche.", "respuesta":"faro", "tipo":"CON LA"},
        "G": {"letra":"G", "pregunta":"Animal doméstico de la familia de los felinos que maúlla y caza ratones.", "respuesta":"gato", "tipo":"CON LA"},
        "H": {"letra":"H", "pregunta":"Agua que se ha vuelto sólida y fría debido al descenso de la temperatura.", "respuesta":"hielo", "tipo":"CON LA"},
        "I": {"letra":"I", "pregunta":"Porción de tierra rodeada de agua por todas partes.", "respuesta":"isla", "tipo":"CON LA"},
        "J": {"letra":"J", "pregunta":"Animal de África con el cuello muy largo y manchas en su piel.", "respuesta":"jirafa", "tipo":"CON LA"},
        "L": {"letra":"L", "pregunta":"Cuerpo celeste que gira alrededor de la Tierra y brilla de noche.", "respuesta":"luna", "tipo":"CON LA"},
        "M": {"letra":"M", "pregunta":"Fruto del manzano, de forma redonda y piel roja, verde o amarilla.", "respuesta":"manzana", "tipo":"CON LA"},
        "N": {"letra":"N", "pregunta":"Fruta cítrica de color naranja con mucha vitamina C.", "respuesta":"naranja", "tipo":"CON LA"},
        "O": {"letra":"O", "pregunta":"Órgano del cuerpo que sirve para percibir los sonidos.", "respuesta":"oreja", "tipo":"CON LA"},
        "P": {"letra":"P", "pregunta":"Animal mamífero conocido por ser el mejor amigo del hombre.", "respuesta":"perro", "tipo":"CON LA"},
        "Q": {"letra":"Q", "pregunta":"Alimento sólido que se obtiene madurando la cuajada de la leche.", "respuesta":"queso", "tipo":"CON LA"},
        "R": {"letra":"R", "pregunta":"Aparato que sirve para medir el tiempo y dar las horas.", "respuesta":"reloj", "tipo":"CON LA"},
        "S": {"letra":"S", "pregunta":"Estrella con luz propia que nos da calor y luz durante el día.", "respuesta":"sol", "tipo":"CON LA"},
        "T": {"letra":"T", "pregunta":"Medio de transporte que circula por raíles formado por varios vagones.", "respuesta":"tren", "tipo":"CON LA"},
        "U": {"letra":"U", "pregunta":"Fruta pequeña y redonda que crece en racimos y sirve para hacer vino.", "respuesta":"uva", "tipo":"CON LA"},
        "V": {"letra":"V", "pregunta":"Estación del año en la que hace más calor y los días son más largos.", "respuesta":"verano", "tipo":"CON LA"},
        "X": {"letra":"X", "pregunta":"Prueba que se hace para evaluar los conocimientos de un alumno.", "respuesta":"examen", "tipo":"CONTIENE LA"},
        "Y": {"letra":"Y", "pregunta":"Embarcación de lujo de gran tamaño y recreo.", "respuesta":"yate", "tipo":"CON LA"},
        "Z": {"letra":"Z", "pregunta":"Calzado que cubre el pie para protegerlo al caminar.", "respuesta":"zapato", "tipo":"CON LA"}
    }

    temas = ["naturaleza", "objetos", "historia", "ciencia", "deportes", "cine"]

    for l in letras:
        exito = False
        try:
            # Pedimos a la IA una pregunta detallada y variada
            prompt = (f"Actúa como guionista de Pasapalabra. Genera una pregunta para la letra {l}. "
                      f"Tema: {random.choice(temas)}. La definición debe ser larga y profesional. "
                      f"Respuesta en ESPAÑOL. JSON: {{\"letra\":\"{l}\", \"pregunta\":\"...\", \"respuesta\":\"...\", \"tipo\":\"CON LA\"}}")
            
            res = model.generate_content(prompt)
            data = json.loads(res.text.replace("```json", "").replace("```", "").strip())
            
            # Validamos que la respuesta sea válida
            resp_limpia = limpiar(data['respuesta'])
            if (data['tipo'] == "CON LA" and resp_limpia.startswith(l.lower())) or (l.lower() in resp_limpia):
                rosco_final.append(data)
                exito = True
        except:
            pass
        
        if not exito:
            rosco_final.append(backup_real[l])

    with open('preguntas.json', 'w', encoding='utf-8') as f:
        json.dump(rosco_final, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    generar_rosco_ia()
