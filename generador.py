import os
import json
import google.generativeai as genai
import time

# Configuración de la API
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("❌ ERROR: No se encontró la GEMINI_API_KEY en los secretos.")
    exit(1) # Esto hará que salga la cruz roja si falta la clave

genai.configure(api_key=api_key)

def limpiar(t):
    if not t: return ""
    return t.lower().strip().replace('á','a').replace('é','e').replace('í','i').replace('ó','o').replace('ú','u').replace('ü','u')

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

    # BANCO DE RESPALDO (Plan B infalible)
    banco_completo = {
        "A": {"pregunta": "Insecto que produce miel.", "respuesta": "abeja", "tipo": "CON LA"},
        "B": {"pregunta": "Mamífero marino enorme.", "respuesta": "ballena", "tipo": "CON LA"},
        "C": {"pregunta": "Edificio donde vivimos.", "respuesta": "casa", "tipo": "CON LA"},
        "D": {"pregunta": "Reptil extinguido.", "respuesta": "dinosaurio", "tipo": "CON LA"},
        "E": {"pregunta": "Animal con trompa.", "respuesta": "elefante", "tipo": "CON LA"},
        "F": {"pregunta": "Torre con luz para barcos.", "respuesta": "faro", "tipo": "CON LA"},
        "G": {"pregunta": "Ave que pone huevos.", "respuesta": "gallina", "tipo": "CON LA"},
        "H": {"pregunta": "Agua congelada.", "respuesta": "hielo", "tipo": "CON LA"},
        "I": {"pregunta": "Tierra rodeada de agua.", "respuesta": "isla", "tipo": "CON LA"},
        "J": {"pregunta": "Animal de cuello largo.", "respuesta": "jirafa", "tipo": "CON LA"},
        "L": {"pregunta": "Satélite de la Tierra.", "respuesta": "luna", "tipo": "CON LA"},
        "M": {"pregunta": "Fruta roja o verde.", "respuesta": "manzana", "tipo": "CON LA"},
        "N": {"pregunta": "Color oscuro.", "respuesta": "negro", "tipo": "CON LA"},
        "O": {"pregunta": "Sirve para escuchar.", "respuesta": "oido", "tipo": "CON LA"},
        "P": {"pregunta": "El mejor amigo del hombre.", "respuesta": "perro", "tipo": "CON LA"},
        "Q": {"pregunta": "Comida hecha de leche.", "respuesta": "queso", "tipo": "CON LA"},
        "R": {"pregunta": "Animal al que le gusta el queso.", "respuesta": "raton", "tipo": "CON LA"},
        "S": {"pregunta": "Estrella del sistema solar.", "respuesta": "sol", "tipo": "CON LA"},
        "T": {"pregunta": "Vehículo sobre raíles.", "respuesta": "tren", "tipo": "CON LA"},
        "U": {"pregunta": "Fruta para el vino.", "respuesta": "uva", "tipo": "CON LA"},
        "V": {"pregunta": "Estación calurosa.", "respuesta": "verano", "tipo": "CON LA"},
        "X": {"pregunta": "Instrumento musical.", "respuesta": "xilofono", "tipo": "CON LA"},
        "Y": {"pregunta": "Parte amarilla del huevo.", "respuesta": "yema", "tipo": "CON LA"},
        "Z": {"pregunta": "Calzado.", "respuesta": "zapato", "tipo": "CON LA"}
    }

    for l in letras:
        print(f"Procesando {l}...")
        exito = False
        intentos = 0
        
        while intentos < 2 and not exito:
            try:
                prompt = f"Pregunta corta Pasapalabra letra {l}. Respuesta en ESPAÑOL. JSON: {{\"letra\":\"{l}\", \"pregunta\":\"...\", \"respuesta\":\"...\", \"tipo\":\"CON LA\"}}"
                response = model.generate_content(prompt)
                p = json.loads(response.text.replace("```json", "").replace("```", "").strip())
                
                if validar_real(l, p['respuesta'], p['tipo']):
                    rosco_final.append(p)
                    exito = True
                else:
                    intentos += 1
            except:
                intentos += 1
                time.sleep(1)
        
        if not exito:
            backup = banco_completo.get(l, {"letra": l, "pregunta": f"Empieza por {l}.", "respuesta": "error", "tipo": "CON LA"})
            backup["letra"] = l
            rosco_final.append(backup)

    with open('preguntas.json', 'w', encoding='utf-8') as f:
        json.dump(rosco_final, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    generar_rosco_ia()
