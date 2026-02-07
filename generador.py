import os
import json
import google.generativeai as genai

api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

def limpiar_alfanumerico(texto):
    if not texto: return ""
    # Quitamos acentos y caracteres raros para comparar puramente
    s = texto.lower().strip()
    s = s.replace('á','a').replace('é','e').replace('í','i').replace('ó','o').replace('ú','u')
    return "".join(c for c in s if c.isalnum())

def validar_ortografia(letra, respuesta, tipo):
    letra_buscada = letra.lower()
    palabra = limpiar_alfanumerico(respuesta)
    
    if not palabra: return False
    
    if "CON LA" in tipo.upper():
        return palabra.startswith(letra_buscada)
    else: # CONTIENE LA
        return letra_buscada in palabra

def generar_rosco_ia():
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = """
    Genera un rosco de Pasapalabra (A-Z, sin K, W, Ñ). 
    Sé extremadamente estricto con la ortografía. 
    Si la letra es B, la palabra DEBE tener una B.
    Devuelve SOLO el JSON:
    [{"letra": "A", "pregunta": "...", "respuesta": "Palabra", "tipo": "CON LA o CONTIENE LA"}]
    """
    
    try:
        response = model.generate_content(prompt)
        texto = response.text.strip()
        if "```json" in texto:
            texto = texto.split("```json")[1].split("```")[0].strip()
        
        datos_ia = json.loads(texto)
        rosco_validado = []

        for p in datos_ia:
            # EL FILTRO CRÍTICO:
            if validar_ortografia(p['letra'], p['respuesta'], p['tipo']):
                rosco_validado.append(p)
            else:
                # Si falla, el robot avisa en la consola de GitHub
                print(f"❌ RECHAZADA: Letra {p['letra']} - Respuesta '{p['respuesta']}' no cumple '{p['tipo']}'")

        with open('preguntas.json', 'w', encoding='utf-8') as f:
            json.dump(rosco_validado, f, ensure_ascii=False, indent=2)
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    generar_rosco_ia()
