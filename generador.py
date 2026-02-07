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

    for l in letras:
        print(f"Buscando palabra para la {l}...")
        exito_letra = False
        intentos = 0
        
        while intentos < 5 and not exito_letra:
            prompt = f"""
            Eres un experto en español. Dame una pregunta de Pasapalabra para la letra '{l}'.
            REGLA: La respuesta DEBE empezar por la letra '{l}' (usar 'CON LA').
            Responde SOLO con este JSON:
            {{"letra": "{l}", "pregunta": "...", "respuesta": "palabra_que_empiece_por_{l}", "tipo": "CON LA"}}
            """
            try:
                response = model.generate_content(prompt)
                texto = response.text.strip()
                if "```json" in texto:
                    texto = texto.split("```json")[1].split("```")[0].strip()
                
                p = json.loads(texto)
                # Forzamos a que el tipo sea 'CON LA' para evitar confusiones como 'Gato' para la C
                p['tipo'] = "CON LA" 
                
                if validar(l, p['respuesta'], p['tipo']):
                    rosco_final.append(p)
                    exito_letra = True
                    print(f"  ✅ {l} encontrada: {p['respuesta']}")
                else:
                    intentos += 1
            except:
                intentos += 1

    with open('preguntas.json', 'w', encoding='utf-8') as f:
        json.dump(rosco_final, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    generar_rosco_ia()
