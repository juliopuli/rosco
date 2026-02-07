import os
import json
import google.generativeai as genai
import time

api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

def limpiar_json(texto):
    return texto.replace("```json", "").replace("```", "").strip()

def generar_rosco_ia():
    # Usamos Gemini 1.5 Flash
    model = genai.GenerativeModel('gemini-1.5-flash')
    letras = "ABCDEFGHIJLMNOPQRSTUVXYZ"
    rosco_final = []
    
    # Dividimos en 3 grupos para no saturar la versión gratuita
    grupos = [letras[i:i+8] for i in range(0, len(letras), 8)]

    for grupo in grupos:
        print(f"Generando bloque: {grupo}")
        prompt = f"""
        Actúa como guionista de Pasapalabra. Genera preguntas de cultura general para estas letras: {grupo}.
        REGLAS: 
        - Respuestas en ESPAÑOL que EMPIECEN por la letra.
        - Formato JSON: [{{"letra": "A", "pregunta": "...", "respuesta": "...", "tipo": "CON LA"}}]
        """
        
        intentos = 0
        while intentos < 3:
            try:
                response = model.generate_content(prompt)
                res_limpia = limpiar_json(response.text)
                datos = json.loads(res_limpia)
                
                for p in datos:
                    if p['respuesta'].lower().startswith(p['letra'].lower()):
                        rosco_final.append(p)
                break 
            except:
                intentos += 1
                time.sleep(5) # Pausa para respetar el límite de la versión gratuita

    # SEGURO DE VIDA: Si alguna letra falta, rellenamos con algo digno
    letras_generadas = [p['letra'] for p in rosco_final]
    for l in letras:
        if l not in letras_generadas:
            respaldos = {"C": "Capital de Venezuela", "D": "Lo que usas para jugar parchís"}
            respuestas = {"C": "caracas", "D": "dado"}
            rosco_final.append({
                "letra": l, 
                "pregunta": respaldos.get(l, f"Palabra común que empieza por {l}"), 
                "respuesta": respuestas.get(l, "comun"), 
                "tipo": "CON LA"
            })

    with open('preguntas.json', 'w', encoding='utf-8') as f:
        json.dump(rosco_final, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    generar_rosco_ia()
