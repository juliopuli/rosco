import os
import json
import google.generativeai as genai
import time

api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

def limpiar_json(texto):
    # Elimina posibles etiquetas de markdown y espacios extra
    return texto.replace("```json", "").replace("```", "").strip()

def generar_rosco_ia():
    model = genai.GenerativeModel('gemini-1.5-flash')
    letras = "ABCDEFGHIJLMNOPQRSTUVXYZ"
    rosco_final = []

    for l in letras:
        print(f"Generando contenido único para la letra: {l}")
        exito = False
        intentos = 0
        
        while intentos < 5 and not exito:
            # Prompt ultra-específico para evitar repeticiones
            prompt = f"""
            Genera una pregunta de Pasapalabra para la letra '{l}'.
            REQUISITOS:
            - La respuesta DEBE ser un sustantivo común o propio en ESPAÑOL.
            - La respuesta DEBE empezar por la letra '{l}'.
            - Nivel: Cultura general (Geografía, Ciencia, Arte).
            - NO uses definiciones infantiles ni menciones la letra en la respuesta.
            
            Formato JSON estricto: 
            {{"letra": "{l}", "pregunta": "...", "respuesta": "...", "tipo": "CON LA"}}
            """
            try:
                response = model.generate_content(prompt)
                data = json.loads(limpiar_json(response.text))
                
                # Validación de seguridad: Que la respuesta sea real y empiece por la letra
                resp = data['respuesta'].lower().strip()
                if resp.startswith(l.lower()) and len(resp) > 2:
                    rosco_final.append(data)
                    exito = True
                    print(f"  ✅ Letra {l} lista: {resp}")
                else:
                    intentos += 1
            except Exception as e:
                print(f"  ⚠️ Error en {l}, reintentando...")
                intentos += 1
                time.sleep(1) # Pausa para no saturar la API

    # Si por algún motivo extremo falta una letra, este bloque NO repite la misma pregunta
    if len(rosco_final) < len(letras):
        print("Aviso: El rosco está incompleto, pero no se han generado duplicados.")

    with open('preguntas.json', 'w', encoding='utf-8') as f:
        json.dump(rosco_final, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    generar_rosco_ia()
