import os
import json
import google.generativeai as genai
import time

api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

def limpiar_json(texto):
    return texto.replace("```json", "").replace("```", "").strip()

def generar_rosco_ia():
    model = genai.GenerativeModel('gemini-1.5-flash')
    letras = "ABCDEFGHIJLMNOPQRSTUVXYZ"
    rosco_final = []
    
    # Diccionario de respaldo de ALTA CALIDAD (Si la IA falla, usará estos)
    backup_profesional = {
        "A": {"letra": "A", "pregunta": "Cuerpo celeste que brilla con luz propia.", "respuesta": "astro", "tipo": "CON LA"},
        "B": {"letra": "B", "pregunta": "Mamífero rumiante con cuernos.", "respuesta": "buey", "tipo": "CON LA"},
        "C": {"letra": "C", "pregunta": "Satélite natural de la Tierra.", "respuesta": "luna", "tipo": "CONTIENE LA"},
        "D": {"letra": "D", "pregunta": "Objeto cúbico usado en juegos de azar.", "respuesta": "dado", "tipo": "CON LA"},
        "E": {"letra": "E", "pregunta": "Animal con trompa de gran tamaño.", "respuesta": "elefante", "tipo": "CON LA"},
        "F": {"letra": "F", "pregunta": "Luz que emite un vehículo por la noche.", "respuesta": "faro", "tipo": "CON LA"},
        "G": {"letra": "G", "pregunta": "Animal doméstico que maúlla.", "respuesta": "gato", "tipo": "CON LA"},
        "H": {"letra": "H", "pregunta": "Masa de agua congelada.", "respuesta": "hielo", "tipo": "CON LA"},
        "I": {"letra": "I", "pregunta": "Porción de tierra rodeada de agua.", "respuesta": "isla", "tipo": "CON LA"},
        "J": {"letra": "J", "pregunta": "Líquido que se extrae de las frutas.", "respuesta": "jugo", "tipo": "CON LA"},
        "L": {"letra": "L", "pregunta": "Rey de la selva.", "respuesta": "leon", "tipo": "CON LA"},
        "M": {"letra": "M", "pregunta": "Capital de España.", "respuesta": "madrid", "tipo": "CON LA"},
        "N": {"letra": "N", "pregunta": "Color de la oscuridad total.", "respuesta": "negro", "tipo": "CON LA"},
        "O": {"letra": "O", "pregunta": "Animal que da lana.", "respuesta": "oveja", "tipo": "CON LA"},
        "P": {"letra": "P", "pregunta": "Instrumento para escribir con tinta.", "respuesta": "pluma", "tipo": "CON LA"},
        "Q": {"letra": "Q", "pregunta": "Alimento sólido hecho de leche.", "respuesta": "queso", "tipo": "CON LA"},
        "R": {"letra": "R", "pregunta": "Color de la sangre.", "respuesta": "rojo", "tipo": "CON LA"},
        "S": {"letra": "S", "pregunta": "Mueble para sentarse.", "respuesta": "silla", "tipo": "CON LA"},
        "T": {"letra": "T", "pregunta": "Vehículo con cuatro ruedas.", "respuesta": "coche", "tipo": "CONTIENE LA"},
        "U": {"letra": "U", "pregunta": "Fruta que se come en racimos.", "respuesta": "uva", "tipo": "CON LA"},
        "V": {"letra": "V", "pregunta": "Soplido fuerte del aire.", "respuesta": "viento", "tipo": "CON LA"},
        "X": {"letra": "X", "pregunta": "Instrumento musical de láminas.", "respuesta": "xilofono", "tipo": "CON LA"},
        "Y": {"letra": "Y", "pregunta": "Embarcación de recreo lujosa.", "respuesta": "yate", "tipo": "CON LA"},
        "Z": {"letra": "Z", "pregunta": "Calzado que cubre el pie.", "respuesta": "zapato", "tipo": "CON LA"}
    }

    # Procesamos en grupos pequeños para evitar el bloqueo de la cuenta Free
    grupos = [letras[i:i+4] for i in range(0, len(letras), 4)]

    for grupo in grupos:
        print(f"Generando preguntas para: {grupo}")
        prompt = f"""
        Eres un experto en el diccionario RAE. Genera preguntas de cultura general para las letras: {grupo}.
        REGLAS:
        - Cada respuesta DEBE ser una palabra real en español.
        - La respuesta DEBE empezar por la letra indicada.
        - Devuelve SOLO un array JSON así: 
        [{{"letra": "A", "pregunta": "...", "respuesta": "...", "tipo": "CON LA"}}]
        """
        
        try:
            response = model.generate_content(prompt)
            data = json.loads(limpiar_json(response.text))
            for item in data:
                # Solo aceptamos si la respuesta es coherente con la letra
                if item['respuesta'].lower().startswith(item['letra'].lower()):
                    rosco_final.append(item)
            time.sleep(10) # Pausa larga para no saturar la API gratuita
        except:
            print(f"Error en grupo {grupo}, se usará el respaldo profesional.")

    # RELLENO DE CALIDAD: Si falta alguna letra, usamos el diccionario profesional
    letras_listas = [p['letra'] for p in rosco_final]
    for l in letras:
        if l not in letras_listas:
            rosco_final.append(backup_profesional[l])

    with open('preguntas.json', 'w', encoding='utf-8') as f:
        json.dump(rosco_final, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    generar_rosco_ia()
