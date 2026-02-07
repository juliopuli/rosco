import os
import json
import google.generativeai as genai

api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

def limpiar(t):
    if not t: return ""
    return t.lower().strip().replace('á','a').replace('é','e').replace('í','i').replace('ó','o').replace('ú','u').replace('ü','u')

def validar(letra, respuesta, tipo):
    l = letra.lower()
    r = limpiar(respuesta)
    if "CON LA" in tipo.upper():
        return r.startswith(l)
    else:
        return l in r

def generar_rosco_ia():
    model = genai.GenerativeModel('gemini-1.5-flash')
    letras = "ABCDEFGHIJLMNOPQRSTUVXYZ"
    rosco_final = []

    # INSTRUCCIONES ESTRICTAS
    prompt_base = """
    Eres un experto en el diccionario de la lengua española (RAE). 
    Genera una pregunta de Pasapalabra para la letra '{letra}'.
    REGLA DE ORO: La respuesta debe ser una palabra en ESPAÑOL que cumpla la regla ortográfica.
    PROHIBIDO: No pienses en inglés. (Ejemplo: No uses 'Elefante' para la H porque en inglés sea 'Elephant').
    
    Responde ÚNICAMENTE con este formato JSON:
    {{"letra": "{letra}", "pregunta": "...", "respuesta": "...", "tipo": "CON LA o CONTIENE LA"}}
    """

    for l in letras:
        print(f"Solicitando letra {l}...")
        intento = 0
        exito = False
        
        while intento < 3 and not exito:
            try:
                response = model.generate_content(prompt_base.format(letra=l))
                texto = response.text.strip()
                if "```json" in texto:
                    texto = texto.split("```json")[1].split("```")[0].strip()
                
                p = json.loads(texto)
                
                if validar(p['letra'], p['respuesta'], p['tipo']):
                    rosco_final.append(p)
                    exito = True
                    print(f"✅ Letra {l} correcta: {p['respuesta']}")
                else:
                    print(f"⚠️ Reintentando {l}... la IA sugirió '{p['respuesta']}' incorrectamente.")
                    intento += 1
            except:
                intento += 1

    with open('preguntas.json', 'w', encoding='utf-8') as f:
        json.dump(rosco_final, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    generar_rosco_ia()
