import os
import json
import google.generativeai as genai

# Configuración de la IA
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

def limpiar_texto(texto):
    if not texto: return ""
    return "".join(c for c in texto if c.isalnum()).lower().replace('á','a').replace('é','e').replace('í','i').replace('ó','o').replace('ú','u')

def validar_ortografia(letra, respuesta, tipo):
    letra = letra.lower()
    resp_limpia = limpiar_texto(respuesta)
    if not resp_limpia: return False
    
    if "CON LA" in tipo.upper():
        return resp_limpia.startswith(letra)
    else: # CONTIENE LA
        return letra in resp_limpia

def generar_rosco_ia():
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = """
    Eres un experto en el diccionario de la RAE. Genera un rosco de Pasapalabra (A-Z, sin K, W, Ñ).
    Reglas:
    1. Una sola palabra por respuesta.
    2. Si es 'CON LA', debe empezar por esa letra.
    3. Si es 'CONTIENE LA', debe incluir esa letra.
    4. Devuelve SOLO un JSON con este formato:
    [{"letra": "A", "pregunta": "...", "respuesta": "...", "tipo": "CON LA"}, ...]
    """
    
    try:
        response = model.generate_content(prompt)
        texto = response.text.strip()
        if "```json" in texto:
            texto = texto.split("```json")[1].split("```")[0].strip()
        
        datos_ia = json.loads(texto)
        rosco_validado = []

        for p in datos_ia:
            # Solo guardamos la pregunta si la IA NO ha mentido con la letra
            if validar_ortografia(p['letra'], p['respuesta'], p['tipo']):
                rosco_validado.append(p)
            else:
                print(f"Letra {p['letra']} descartada por error de la IA: {p['respuesta']}")

        with open('preguntas.json', 'w', encoding='utf-8') as f:
            json.dump(rosco_validado, f, ensure_ascii=False, indent=2)
            
    except Exception as e:
        print(f"Error crítico: {e}")

if __name__ == "__main__":
    generar_rosco_ia()
