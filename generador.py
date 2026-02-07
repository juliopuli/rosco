import os
import json
import google.generativeai as genai

# Configuración de la API
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

def generar_rosco_ia():
    model = genai.GenerativeModel('gemini-1.5-flash')
    letras = "ABCDEFGHIJLMNOPQRSTUVXYZ"
    rosco_final = []

    # Diccionario de emergencia por si la IA se bloquea o falla
    emergencia = {
        "A": {"letra": "A", "pregunta": "Primera letra del abecedario.", "respuesta": "a", "tipo": "CON LA"},
        "H": {"letra": "H", "pregunta": "Lo que pones en la bebida para enfriarla.", "respuesta": "hielo", "tipo": "CON LA"}
    }

    for l in letras:
        print(f"Procesando letra: {l}")
        exito = False
        
        # Intentamos que la IA nos de la pregunta
        prompt = f"Dame una pregunta de Pasapalabra en ESPAÑOL. Letra: {l}. La respuesta DEBE empezar por {l}. Formato JSON: {{\"letra\":\"{l}\", \"pregunta\":\"...\", \"respuesta\":\"...\", \"tipo\":\"CON LA\"}}"
        
        try:
            response = model.generate_content(prompt)
            texto = response.text.strip()
            # Limpiamos el texto de posibles etiquetas de código
            texto = texto.replace("```json", "").replace("```", "").strip()
            
            p = json.loads(texto)
            
            # Validación simple: ¿La respuesta empieza por la letra?
            if p['respuesta'].lower().strip().startswith(l.lower()):
                rosco_final.append(p)
                exito = True
                print(f"  ✅ {l} aceptada")
        except:
            print(f"  ⚠️ Error en letra {l}, usando respaldo.")

        # SI LA IA FALLÓ O EL FILTRO LA RECHAZÓ, METEMOS UNA DE SEGURIDAD
        if not exito:
            if l in emergencia:
                rosco_final.append(emergencia[l])
            else:
                # Generamos una genérica básica para que el archivo no esté vacío
                rosco_final.append({"letra": l, "pregunta": f"Empieza por la letra {l}.", "respuesta": l.lower(), "tipo": "CON LA"})

    # Guardado final: Garantizamos que siempre habrá 24 objetos
    with open('preguntas.json', 'w', encoding='utf-8') as f:
        json.dump(rosco_final, f, ensure_ascii=False, indent=2)
    print("Misión cumplida: preguntas.json generado.")

if __name__ == "__main__":
    generar_rosco_ia()
