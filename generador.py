import os
import json
import google.generativeai as genai
import re

api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

def limpiar_texto(texto):
    # Quita acentos y pone en minúsculas para validar
    return "".join(c for c in texto if c.isalnum()).lower().replace('á','a').replace('é','e').replace('í','i').replace('ó','o').replace('ú','u')

def validar_pregunta(letra, respuesta, tipo):
    letra = letra.lower()
    resp_limpia = limpiar_texto(respuesta)
    
    if "CON LA" in tipo.upper():
        return resp_limpia.startswith(letra)
    else: # CONTIENE LA
        return letra in resp_limpia

def generar_rosco_ia():
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = """
    Genera un rosco de Pasapalabra en español (A-Z, sin K, W, Ñ).
    Reglas estrictas:
    1. Si es 'CON LA', la respuesta DEBE empezar por esa letra.
    2. Si es 'CONTIENE LA', la respuesta DEBE tener esa letra en cualquier posición.
    3. Respuestas de UNA SOLA PALABRA y que existan en el diccionario.
    4. Evita nombres propios complejos.
    
    Devuelve solo el JSON:
    [{"letra": "A", "pregunta": "...", "respuesta": "...", "tipo": "CON LA"}, ...]
    """
    
    try:
        response = model.generate_content(prompt)
        texto = response.text.strip()
        if "```json" in texto:
            texto = texto.split("```json")[1].split("```")[0].strip()
        
        datos_crudos = json.loads(texto)
        datos_validados = []

        for p in datos_crudos:
            if validar_pregunta(p['letra'], p['respuesta'], p['tipo']):
                datos_validados.append(p)
            else:
                print(f"⚠️ IA se equivocó en {p['letra']}: {p['respuesta']} no cumple {p['tipo']}")
                # Aquí podrías añadir una lógica para reintentar, 
                # pero por ahora lo dejamos pasar para no entrar en bucle.

        with open('preguntas.json', 'w', encoding='utf-8') as f:
            json.dump(datos_validados, f, ensure_ascii=False, indent=2)
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    generar_rosco_ia()
