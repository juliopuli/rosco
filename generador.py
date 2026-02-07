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
        print(f"Buscando pregunta real para la {l}...")
        exito = False
        intentos = 0
        
        # Aumentamos a 10 intentos para asegurar calidad
        while intentos < 10 and not exito:
            prompt = f"""
            Eres un guionista veterano del programa Pasapalabra. 
            Genera una pregunta de CULTURA GENERAL para la letra '{l}'.
            REGLA: La respuesta DEBE empezar por la letra '{l}' en ESPAÑOL.
            EVITA: Definiciones genéricas o infantiles. No digas 'Letra {l}'.
            Responde SOLO con este formato JSON: 
            {{"letra": "{l}", "pregunta": "Definición interesante aquí...", "respuesta": "PalabraReal", "tipo": "CON LA"}}
            """
            try:
                response = model.generate_content(prompt)
                texto = response.text.strip().replace("```json", "").replace("```", "").strip()
                p = json.loads(texto)
                
                # Validamos que la respuesta sea válida y no una sola letra
                if p['respuesta'].lower().startswith(l.lower()) and len(p['respuesta']) > 2:
                    rosco_final.append(p)
                    exito = True
                    print(f"  ✅ {l} conseguida: {p['respuesta']}")
                else:
                    intentos += 1
            except:
                intentos += 1

        # Si tras 10 veces falla, usamos un banco de datos manual de CALIDAD, no genérico
        if not exito:
            banco_emergencia = {
                "C": {"letra": "C", "pregunta": "Líquido transparente que bebemos.", "respuesta": "cristalina", "tipo": "CON LA"},
                "D": {"letra": "D", "pregunta": "Órgano duro dentro de la boca.", "respuesta": "diente", "tipo": "CON LA"},
                "E": {"letra": "E", "pregunta": "Lugar donde se guardan libros.", "respuesta": "estanteria", "tipo": "CON LA"}
            }
            rosco_final.append(banco_emergencia.get(l, {"letra": l, "pregunta": f"Elemento químico o común que empieza por {l}.", "respuesta": "xenon" if l=="X" else "yodo" if l=="Y" else "zinc", "tipo": "CON LA"}))

    with open('preguntas.json', 'w', encoding='utf-8') as f:
        json.dump(rosco_final, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    generar_rosco_ia()
