import os
import json
import google.generativeai as genai

# Configuramos la IA con la llave secreta (que el robot cogerá de la caja fuerte)
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

def generar_rosco_ia():
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = """
    Genera un rosco de Pasapalabra en español. 
    Para cada letra del abecedario (A-Z, excluyendo K, W, Ñ), dame una pregunta de cultura general.
    Devuelve exclusivamente un JSON con este formato de lista:
    [{"letra": "A", "pregunta": "...", "respuesta": "...", "tipo": "CON LA"}, ...]
    Asegúrate de que 'tipo' sea 'CON LA' si empieza por esa letra o 'CONTIENE LA' si la lleva dentro.
    La respuesta debe ser una sola palabra.
    """
    
    try:
        response = model.generate_content(prompt)
        # Limpiamos la respuesta para quedarnos solo con el JSON
        texto = response.text.strip()
        if "```json" in texto:
            texto = texto.split("```json")[1].split("```")[0].strip()
        
        datos = json.loads(texto)
        
        with open('preguntas.json', 'w', encoding='utf-8') as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)
        print("Rosco generado por IA con éxito.")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    generar_rosco_ia()
