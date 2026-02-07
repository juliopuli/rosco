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
    return r.startswith(l) if "CON LA" in tipo.upper() else l in r

def generar_rosco_ia():
    model = genai.GenerativeModel('gemini-1.5-flash')
    letras = "ABCDEFGHIJLMNOPQRSTUVXYZ"
    rosco_final = []

    for l in letras:
        print(f"Generando nivel experto para la {l}...")
        exito = False
        intentos = 0
        
        while intentos < 4 and not exito:
            # PROMPT NIVEL DIFÍCIL
            prompt = f"""
            Actúa como un experto en cultura general y lexicografía. 
            Genera una pregunta de NIVEL DIFÍCIL para un concurso de TV para la letra '{l}'.
            
            REGLAS:
            1. La respuesta debe ser una palabra técnica, culta o de cultura general avanzada en ESPAÑOL.
            2. Evita palabras obvias o infantiles.
            3. La respuesta DEBE empezar por '{l}'.
            
            Responde SOLO con este JSON:
            {{"letra": "{l}", "pregunta": "...", "respuesta": "...", "tipo": "CON LA"}}
            """
            try:
                response = model.generate_content(prompt)
                texto = response.text.strip().replace("```json", "").replace("```", "").strip()
                p = json.loads(texto)
                p['tipo'] = "CON LA"
                
                if validar(l, p['respuesta'], p['tipo']) and len(p['respuesta']) > 2:
                    rosco_final.append(p)
                    exito = True
                    print(f"  🔥 {l} aceptada: {p['respuesta']}")
                else:
                    intentos += 1
            except:
                intentos += 1

        # Si falla mucho, un respaldo un poco más digno que solo la letra
        if not exito:
            rosco_final.append({"letra": l, "pregunta": f"Ciencia que estudia los astros y empieza por {l}.", "respuesta": "astronomia" if l=="A" else "biologia" if l=="B" else "cosmos" if l=="C" else "dinosaurio", "tipo": "CON LA"})

    with open('preguntas.json', 'w', encoding='utf-8') as f:
        json.dump(rosco_final, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    generar_rosco_ia()
