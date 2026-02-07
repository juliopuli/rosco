import os
import json
import google.generativeai as genai

api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

def limpiar(t):
    if not t: return ""
    return t.lower().strip().replace('á','a').replace('é','e').replace('í','i').replace('ó','o').replace('ú','u').replace('ü','u')

def generar_rosco_ia():
    model = genai.GenerativeModel('gemini-1.5-flash')
    letras = "ABCDEFGHIJLMNOPQRSTUVXYZ"
    rosco_final = []

    for l in letras:
        print(f"Generando nivel experto para la {l}...")
        exito = False
        intentos = 0
        
        while intentos < 4 and not exito:
            prompt = f"Actúa como el guionista de Pasapalabra. Dame una definición culta y profesional para la letra '{l}'. La respuesta debe empezar por '{l}' y ser en ESPAÑOL. Responde SOLO JSON: {{\"letra\": \"{l}\", \"pregunta\": \"...\", \"respuesta\": \"...\", \"tipo\": \"CON LA\"}}"
            try:
                response = model.generate_content(prompt)
                texto = response.text.strip().replace("```json", "").replace("```", "").strip()
                p = json.loads(texto)
                
                if p['respuesta'].lower().startswith(l.lower()) and len(p['respuesta']) > 2:
                    rosco_final.append(p)
                    exito = True
                else: intentos += 1
            except: intentos += 1

        if not exito:
            # Respaldos manuales más variados si la IA falla
            backups = {"A": "Aparato para volar", "B": "Fruta alargada amarilla", "C": "Satélite de la Tierra"}
            rosco_final.append({"letra": l, "pregunta": backups.get(l, f"Definición técnica para la letra {l}"), "respuesta": "avion" if l=="A" else "banana" if l=="B" else "luna" if l=="C" else l.lower(), "tipo": "CON LA"})

    with open('preguntas.json', 'w', encoding='utf-8') as f:
        json.dump(rosco_final, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    generar_rosco_ia()
