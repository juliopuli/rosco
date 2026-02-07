import os
import json
import google.generativeai as genai

api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

def limpiar_texto(texto):
    return "".join(c for c in texto if c.isalnum()).lower().replace('á','a').replace('é','e').replace('í','i').replace('ó','o').replace('ú','u')

def validar_ortografia(letra, respuesta, tipo):
    letra = letra.lower()
    resp_limpia = limpiar_texto(respuesta)
    if "CON LA" in tipo.upper():
        return resp_limpia.startswith(letra)
    else: # CONTIENE LA
        return letra in resp_limpia

def obtener_pregunta_ia(letra):
    model = genai.GenerativeModel('gemini-1.5-flash')
    intentos = 0
    while intentos < 5: # Reintenta hasta 5 veces por letra
        prompt = f"Dame una pregunta de Pasapalabra para la letra '{letra}'. Responde solo en JSON: {{\"letra\": \"{letra}\", \"pregunta\": \"...\", \"respuesta\": \"una_sola_palabra\", \"tipo\": \"CON LA o CONTIENE LA\"}}"
        
        try:
            response = model.generate_content(prompt)
            texto = response.text.strip()
            if "```json" in texto:
                texto = texto.split("```json")[1].split("```")[0].strip()
            
            data = json.loads(texto)
            if validar_ortografia(data['letra'], data['respuesta'], data['tipo']):
                return data
        except:
            pass
        intentos += 1
    return None

def generar_rosco_ia():
    letras = "ABCDEFGHIJLMNOPQRSTUVXYZ"
    rosco_final = []
    
    for l in letras:
        print(f"Generando letra {l}...")
        p = obtener_pregunta_ia(l)
        if p:
            rosco_final.append(p)
    
    with open('preguntas.json', 'w', encoding='utf-8') as f:
        json.dump(rosco_final, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    generar_rosco_ia()
