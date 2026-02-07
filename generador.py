import os
import json
import google.generativeai as genai
import time

api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

def limpiar_texto(t):
    if not t: return ""
    return t.lower().strip().replace('á','a').replace('é','e').replace('í','i').replace('ó','o').replace('ú','u').replace('ü','u')

def validar_estricto(letra, respuesta, tipo):
    l = letra.lower()
    r = limpiar_texto(respuesta)
    if not r: return False
    
    if "CON LA" in tipo.upper():
        return r.startswith(l)
    else: # CONTIENE LA
        return l in r

def generar_rosco_ia():
    model = genai.GenerativeModel('gemini-1.5-flash')
    letras = "ABCDEFGHIJLMNOPQRSTUVXYZ"
    rosco_final = []
    
    # DICCIONARIO DE RESPALDO PARA "CONTIENE LA" (Donde la IA más falla)
    respaldo_contiene = {
        "C": {"letra": "C", "pregunta": "Animal doméstico que caza ratones.", "respuesta": "gato", "tipo": "CONTIENE LA"},
        "D": {"letra": "D", "pregunta": "Día de la semana que sigue al domingo.", "respuesta": "lunes", "tipo": "CONTIENE LA"},
        "G": {"letra": "G", "pregunta": "Fruta roja de verano con pepitas negras.", "respuesta": "sandia", "tipo": "CONTIENE LA"},
        "N": {"letra": "N", "pregunta": "Cuerpo celeste que brilla de noche.", "respuesta": "estrella", "tipo": "CONTIENE LA"},
        "T": {"letra": "T", "pregunta": "Vehículo con cuatro ruedas para viajar.", "respuesta": "coche", "tipo": "CONTIENE LA"},
        "Y": {"letra": "Y", "pregunta": "Color del sol y de los limones.", "respuesta": "amarillo", "tipo": "CONTIENE LA"}
    }

    # Procesamos en grupos de 4 para no saturar la API
    grupos = [letras[i:i+4] for i in range(0, len(letras), 4)]

    for grupo in grupos:
        print(f"Generando: {grupo}")
        prompt = f"""
        Eres un experto en el programa Pasapalabra. Genera preguntas para estas letras: {grupo}.
        IMPORTANTE: 
        - Si es 'CON LA', la respuesta empieza por la letra.
        - Si es 'CONTIENE LA', la letra debe estar en CUALQUIER posición de la palabra.
        - No inventes palabras.
        Responde SOLO JSON: [{{"letra": "...", "pregunta": "...", "respuesta": "...", "tipo": "CON LA o CONTIENE LA"}}]
        """
        
        try:
            response = model.generate_content(prompt)
            texto = response.text.replace("```json", "").replace("```", "").strip()
            data = json.loads(texto)
            
            for item in data:
                # VALIDACIÓN CRÍTICA ANTES DE ACEPTAR
                if validar_estricto(item['letra'], item['respuesta'], item['tipo']):
                    rosco_final.append(item)
                else:
                    print(f"❌ Rechazada por error de la IA: {item['respuesta']} para {item['letra']}")
            
            time.sleep(8) 
        except:
            print(f"⚠️ Error en grupo {grupo}")

    # RELLENO DE EMERGENCIA SI LA IA FALLÓ LA VALIDACIÓN
    letras_listas = [p['letra'] for p in rosco_final]
    for l in letras:
        if l not in letras_listas:
            # Si tenemos un respaldo específico (como para la C de Gato), lo usamos
            if l in respaldo_contiene:
                rosco_final.append(respaldo_contiene[l])
            else:
                # Respaldo genérico pero SEGURO (CON LA)
                rosco_final.append({"letra": l, "pregunta": f"Empieza por {l}: Objeto o concepto común.", "respuesta": l.lower() + "asa", "tipo": "CON LA"})

    with open('preguntas.json', 'w', encoding='utf-8') as f:
        json.dump(rosco_final, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    generar_rosco_ia()
