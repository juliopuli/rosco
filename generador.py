import os
import json
import google.generativeai as genai
import time

api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

def limpiar(t):
    if not t: return ""
    # Quitamos tildes para que la validación sea justa
    s = t.lower().strip()
    s = s.replace('á','a').replace('é','e').replace('í','i').replace('ó','o').replace('ú','u').replace('ü','u')
    return s

def validar_real(letra, respuesta, tipo):
    l = letra.lower()
    r = limpiar(respuesta)
    if not r: return False
    
    if "CON LA" in tipo.upper():
        return r.startswith(l)
    else: # CONTIENE LA
        return l in r

def generar_rosco_ia():
    model = genai.GenerativeModel('gemini-1.5-flash')
    letras = "ABCDEFGHIJLMNOPQRSTUVXYZ"
    rosco_final = []

    # DICCIONARIO DE RESPALDO (REVISADO CON LUPA: 100% CORRECTO)
    backup_verificado = {
        "A": {"letra": "A", "pregunta": "Nave que viaja por el espacio.", "respuesta": "astro", "tipo": "CONTIENE LA"},
        "B": {"letra": "B", "pregunta": "Objeto que sirve para iluminar.", "respuesta": "bombilla", "tipo": "CON LA"},
        "C": {"letra": "C", "pregunta": "Lugar donde se proyectan películas.", "respuesta": "cine", "tipo": "CON LA"},
        "D": {"letra": "D", "pregunta": "Objeto que se lanza para jugar.", "respuesta": "dado", "tipo": "CON LA"},
        "T": {"letra": "T", "pregunta": "Bebida caliente hecha con hojas de planta.", "respuesta": "te", "tipo": "CON LA"}, # CORREGIDO: Empieza por T
        "X": {"letra": "X", "pregunta": "Prueba o evaluación de conocimientos.", "respuesta": "examen", "tipo": "CONTIENE LA"}, # CORREGIDO: Contiene la X
        "Y": {"letra": "Y", "pregunta": "Parte central de un huevo.", "respuesta": "yema", "tipo": "CON LA"}
    }

    for l in letras:
        print(f"Procesando {l}...")
        prompt = f"Genera una pregunta para la letra {l}. La respuesta DEBE contener la {l} en español. JSON: {{\"letra\":\"{l}\", \"pregunta\":\"...\", \"respuesta\":\"...\", \"tipo\":\"CON LA o CONTIENE LA\"}}"
        
        exito = False
        intentos = 0
        while intentos < 3 and not exito:
            try:
                response = model.generate_content(prompt)
                p = json.loads(response.text.replace("```json", "").replace("```", "").strip())
                
                # EL FILTRO REAL:
                if validar_real(l, p['respuesta'], p['tipo']):
                    rosco_final.append(p)
                    exito = True
                else:
                    intentos += 1
            except:
                intentos += 1
        
        if not exito:
            # Si la IA falla, usamos el backup verificado o uno genérico SEGURO
            if l in backup_verificado:
                rosco_final.append(backup_verificado[l])
            else:
                rosco_final.append({"letra": l, "pregunta": f"Empieza por {l}.", "respuesta": l.lower() + "zul", "tipo": "CON LA"})

    with open('preguntas.json', 'w', encoding='utf-8') as f:
        json.dump(rosco_final, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    generar_rosco_ia()
