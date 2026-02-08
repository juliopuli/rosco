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

    for l in letras:
        exito = False
        intentos = 0
        while intentos < 2 and not exito:
            try:
                prompt = (f"Actúa como el guionista de Pasapalabra. Genera una definición culta, precisa y detallada "
                          f"para la letra {l}. La definición debe tener al menos 12 palabras. "
                          f"Respuesta en ESPAÑOL. JSON: {{\"letra\":\"{l}\", \"pregunta\":\"...\", \"respuesta\":\"...\", \"tipo\":\"CON LA\"}}")
                
                res = model.generate_content(prompt)
                data = json.loads(res.text.replace("```json", "").replace("```", "").strip())
                
                resp_limpia = limpiar(data['respuesta'])
                if (data['tipo'] == "CON LA" and resp_limpia.startswith(l.lower())) or (l.lower() in resp_limpia):
                    rosco_final.append(data)
                    exito = True
                    print(f"✅ {l} generada.")
            except:
                intentos += 1
                time.sleep(1)
        
        if not exito:
            # Respaldo simple si la IA falla
            rosco_final.append({"letra":l, "pregunta":f"Palabra común que comienza por la letra {l}.", "respuesta":l.lower()+"abara", "tipo":"CON LA"})

    with open('preguntas.json', 'w', encoding='utf-8') as f:
        json.dump(rosco_final, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    generar_rosco_ia()
