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
    if not resp_limpia: return False
    if "CON LA" in tipo.upper():
        return resp_limpia.startswith(letra)
    else:
        return letra in resp_limpia

def generar_rosco_ia():
    model = genai.GenerativeModel('gemini-1.5-flash')
    letras = "ABCDEFGHIJLMNOPQRSTUVXYZ"
    
    # Pedimos todo el rosco con un prompt mucho más "agresivo" en ortografía
    prompt = """
    Eres un experto lexicógrafo del diccionario de la RAE. 
    Genera un rosco de Pasapalabra (A-Z, sin K, W, Ñ).
    Para cada letra, elige una palabra real y común del español.
    REGLA DE ORO: Si dices 'CON LA', la palabra DEBE empezar por esa letra. 
    Si dices 'CONTIENE LA', la palabra DEBE tener esa letra.
    
    Devuelve SOLO un JSON así:
    [{"letra": "A", "pregunta": "...", "respuesta": "...", "tipo": "CON LA"}, ...]
    """
    
    try:
        response = model.generate_content(prompt)
        texto = response.text.strip()
        if "```json" in texto:
            texto = texto.split("```json")[1].split("```")[0].strip()
        
        datos = json.loads(texto)
        
        # Validamos uno por uno. Si uno falla, usamos un backup inmediato para esa letra
        rosco_final = []
        for p in datos:
            if validar_ortografia(p['letra'], p['respuesta'], p['tipo']):
                rosco_final.append(p)
            else:
                print(f"Letra {p['letra']} falló. IA dijo {p['respuesta']}")
        
        with open('preguntas.json', 'w', encoding='utf-8') as f:
            json.dump(rosco_final, f, ensure_ascii=False, indent=2)
            
    except Exception as e:
        print(f"Error crítico: {e}")

if __name__ == "__main__":
    generar_rosco_ia()
