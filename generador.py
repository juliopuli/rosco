import os
import json
import google.generativeai as genai

# Configuración de la IA
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

def limpiar_alfanumerico(texto):
    if not texto: return ""
    s = texto.lower().strip()
    # Normalización para validación (quitar tildes para comparar)
    s = s.replace('á','a').replace('é','e').replace('í','i').replace('ó','o').replace('ú','u').replace('ü','u')
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
    
    # Prompt reforzado para evitar el inglés
    prompt = """
    Eres un experto lingüista de la Lengua Española (RAE). Tu tarea es generar un rosco de Pasapalabra.
    
    REGLAS CRÍTICAS:
    1. El idioma de pensamiento y respuesta debe ser ÚNICAMENTE ESPAÑOL.
    2. Ignora palabras en inglés (ej: no uses 'Elephant' para la H, usa 'Zanahoria' o 'Búho').
    3. Para 'CON LA [letra]': la respuesta debe empezar por esa letra en ESPAÑOL.
    4. Para 'CONTIENE LA [letra]': la letra debe aparecer dentro de la palabra en ESPAÑOL.
    5. Respuestas de UNA SOLA PALABRA.
    
    Genera para las letras: A, B, C, D, E, F, G, H, I, J, L, M, N, O, P, Q, R, S, T, U, V, X, Y, Z.
    
    Devuelve exclusivamente un JSON:
    [{"letra": "A", "pregunta": "...", "respuesta": "...", "tipo": "CON LA"}]
    """
    
    try:
        response = model.generate_content(prompt)
        texto = response.text.strip()
        if "```json" in texto:
            texto = texto.split("```json")[1].split("```")[0].strip()
        
        datos_ia = json.loads(texto)
        rosco_validado = []

        for p in datos_ia:
            # Filtro de seguridad en español
            if validar_ortografia(p['letra'], p['respuesta'], p['tipo']):
                rosco_validado.append(p)
            else:
                print(f"❌ ERROR LINGÜÍSTICO: Letra {p['letra']} - '{p['respuesta']}' no válida en español.")

        with open('preguntas.json', 'w', encoding='utf-8') as f:
            json.dump(rosco_validado, f, ensure_ascii=False, indent=2)
        print(f"✅ Rosco generado con {len(rosco_validado)} preguntas válidas.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    generar_rosco_ia()
