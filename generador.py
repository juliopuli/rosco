import os
import json
import google.generativeai as genai
import time
import random
from datetime import datetime

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

    # LISTA DE TEMAS PARA FORZAR VARIEDAD
    temas = [
        "ciencia y tecnología", "historia universal", "cine y series", 
        "geografía del mundo", "naturaleza y animales", "arte y literatura", 
        "gastronomía", "deportes", "objetos cotidianos", "mitología"
    ]

    print(f"--- Iniciando generación variada: {datetime.now()} ---")

    for l in letras:
        tema_elegido = random.choice(temas) # Elegimos un tema distinto para cada letra
        exito = False
        intentos = 0
        
        while intentos < 2 and not exito:
            try:
                # El prompt ahora incluye un tema aleatorio y una instrucción de originalidad
                prompt = (f"Actúa como el guionista experto de Pasapalabra. Genera una definición para la letra {l}. "
                          f"El tema debe ser: {tema_elegido}. "
                          f"IMPORTANTE: No uses palabras demasiado obvias o infantiles. "
                          f"La definición debe ser profesional y detallada (mínimo 12 palabras). "
                          f"Respuesta en ESPAÑOL. JSON: {{\"letra\":\"{l}\", \"pregunta\":\"...\", \"respuesta\":\"...\", \"tipo\":\"CON LA\"}}")
                
                res = model.generate_content(prompt)
                data = json.loads(res.text.replace("```json", "").replace("```", "").strip())
                
                resp_limpia = limpiar(data['respuesta'])
                # Validación de seguridad
                if (data['tipo'] == "CON LA" and resp_limpia.startswith(l.lower())) or (l.lower() in resp_limpia):
                    rosco_final.append(data)
                    exito = True
                    print(f"✅ {l} ({tema_elegido}): {data['respuesta']}")
                else:
                    intentos += 1
            except:
                intentos += 1
                time.sleep(1)
        
        if not exito:
            # Palabra de emergencia genérica pero funcional
            rosco_final.append({"letra":l, "pregunta":f"Se dice de aquello que empieza por la letra {l} y que es común en el diccionario español.", "respuesta":l.lower()+"abara", "tipo":"CON LA"})

    with open('preguntas.json', 'w', encoding='utf-8') as f:
        json.dump(rosco_final, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    generar_rosco_ia()
