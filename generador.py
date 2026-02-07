import os
import json
import google.generativeai as genai

# Configuración
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

def limpiar_simple(t):
    if not t: return ""
    return t.lower().strip().replace('á','a').replace('é','e').replace('í','i').replace('ó','o').replace('ú','u').replace('ü','u')

def validar(letra, respuesta, tipo):
    l = letra.lower()
    r = limpiar_simple(respuesta)
    return r.startswith(l) if "CON LA" in tipo.upper() else l in r

def generar_rosco_ia():
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Un banco de seguridad por si la IA falla en alguna letra
    seguridad = {
        "A": {"letra": "A", "pregunta": "Macho de la abeja.", "respuesta": "zangano", "tipo": "CONTIENE LA"},
        "H": {"letra": "H", "pregunta": "Animal con trompa muy larga.", "respuesta": "elefante", "tipo": "CONTIENE LA"},
        "B": {"letra": "B", "pregunta": "Embarcación de madera.", "respuesta": "barco", "tipo": "CON LA"}
    }
    
    prompt = "Genera un rosco de Pasapalabra (A-Z, sin K, W, Ñ) en ESPAÑOL. Una palabra por respuesta. JSON format: [{\"letra\": \"A\", \"pregunta\": \"...\", \"respuesta\": \"...\", \"tipo\": \"CON LA\"}]"
    
    try:
        response = model.generate_content(prompt)
        texto = response.text.strip()
        if "```json" in texto:
            texto = texto.split("```json")[1].split("```")[0].strip()
        
        datos_ia = json.loads(texto)
        resultado_final = []
        letras_vistas = []

        for p in datos_ia:
            letra = p['letra'].upper()
            if validar(letra, p['respuesta'], p['tipo']):
                resultado_final.append(p)
                letras_vistas.append(letra)

        # RELLENO DE EMERGENCIA: Si falta alguna letra, la añadimos del banco o una genérica
        for l in "ABCDEFGHIJLMNOPQRSTUVXYZ":
            if l not in letras_vistas:
                if l in seguridad:
                    resultado_final.append(seguridad[l])
                else:
                    resultado_final.append({"letra": l, "pregunta": f"Empieza por {l}: Parte del cuerpo humano.", "respuesta": "brazo" if l=="B" else "cara" if l=="C" else "dedo", "tipo": "CON LA"})

        with open('preguntas.json', 'w', encoding='utf-8') as f:
            json.dump(resultado_final, f, ensure_ascii=False, indent=2)
        print("✅ Rosco generado y parcheado.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    generar_rosco_ia()
