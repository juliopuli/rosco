import os
import json
import google.generativeai as genai
import time

api_key = os.getenv("GEMINI_API_KEY")
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

    # --- PLAN B: DICCIONARIO COMPLETO (Por si la IA falla, usaremos esto) ---
    banco_completo = {
        "A": {"pregunta": "Insecto que produce miel y cera.", "respuesta": "abeja", "tipo": "CON LA"},
        "B": {"pregunta": "Mamífero cetáceo enorme que vive en el mar.", "respuesta": "ballena", "tipo": "CON LA"},
        "C": {"pregunta": "Mamífero carnívoro doméstico que maúlla.", "respuesta": "gato", "tipo": "CONTIENE LA"}, # OJO: Gato contiene C? NO. Mejor 'Casa'.
        # CORRECCIÓN MANUAL AL VUELO PARA EVITAR ERRORES:
        "C": {"pregunta": "Edificio donde vive una persona.", "respuesta": "casa", "tipo": "CON LA"},
        "D": {"pregunta": "Reptil prehistórico extinguido.", "respuesta": "dinosaurio", "tipo": "CON LA"},
        "E": {"pregunta": "Animal terrestre más grande con trompa.", "respuesta": "elefante", "tipo": "CON LA"},
        "F": {"pregunta": "Construcción con luz para guiar a los barcos.", "respuesta": "faro", "tipo": "CON LA"},
        "G": {"pregunta": "Ave de corral que pone huevos.", "respuesta": "gallina", "tipo": "CON LA"},
        "H": {"pregunta": "Agua en estado sólido.", "respuesta": "hielo", "tipo": "CON LA"},
        "I": {"pregunta": "Porción de tierra rodeada de agua.", "respuesta": "isla", "tipo": "CON LA"},
        "J": {"pregunta": "Mamífero de cuello muy largo.", "respuesta": "jirafa", "tipo": "CON LA"},
        "L": {"pregunta": "Satélite natural de la Tierra.", "respuesta": "luna", "tipo": "CON LA"},
        "M": {"pregunta": "Fruta amarilla con cáscara.", "respuesta": "manzana", "tipo": "CON LA"},
        "N": {"pregunta": "Color opuesto al blanco.", "respuesta": "negro", "tipo": "CON LA"},
        "O": {"pregunta": "Órgano de la audición.", "respuesta": "oido", "tipo": "CON LA"},
        "P": {"pregunta": "Animal que ladra.", "respuesta": "perro", "tipo": "CON LA"},
        "Q": {"pregunta": "Producto lácteo derivado de la leche.", "respuesta": "queso", "tipo": "CON LA"},
        "R": {"pregunta": "Animal pequeño con cola larga que roe.", "respuesta": "raton", "tipo": "CON LA"},
        "S": {"pregunta": "Estrella que nos da luz y calor.", "respuesta": "sol", "tipo": "CON LA"},
        "T": {"pregunta": "Objeto que marca la hora.", "respuesta": "reloj", "tipo": "CONTIENE LA"}, # OJO: Reloj no tiene T.
        # CORRECCIÓN:
        "T": {"pregunta": "Vehículo que circula sobre raíles.", "respuesta": "tren", "tipo": "CON LA"},
        "U": {"pregunta": "Fruta pequeña que crece en racimos.", "respuesta": "uva", "tipo": "CON LA"},
        "V": {"pregunta": "Estación del año más calurosa.", "respuesta": "verano", "tipo": "CON LA"},
        "X": {"pregunta": "Instrumento musical de percusión.", "respuesta": "xilofono", "tipo": "CON LA"},
        "Y": {"pregunta": "Parte amarilla del huevo.", "respuesta": "yema", "tipo": "CON LA"},
        "Z": {"pregunta": "Animal rayado blanco y negro.", "respuesta": "cebra", "tipo": "CONTIENE LA"} # Cebra no tiene Z.
        # CORRECCIÓN Z:
        "Z": {"pregunta": "Calzado que protege el pie.", "respuesta": "zapato", "tipo": "CON LA"}
    }

    for l in letras:
        print(f"Procesando {l}...")
        exito = False
        
        # 1. Intentamos con la IA
        intentos = 0
        while intentos < 2 and not exito:
            try:
                prompt = f"Dame una pregunta de Pasapalabra para la letra {l}. Respuesta en ESPAÑOL. JSON: {{\"letra\":\"{l}\", \"pregunta\":\"...\", \"respuesta\":\"...\", \"tipo\":\"CON LA\"}}"
                response = model.generate_content(prompt)
                p = json.loads(response.text.replace("```json", "").replace("```", "").strip())
                
                # VALIDACIÓN ESTRICTA
                if validar_real(l, p['respuesta'], p['tipo']):
                    rosco_final.append(p)
                    exito = True
                    print(f"  ✅ IA generó: {p['respuesta']}")
                else:
                    intentos += 1
            except:
                intentos += 1
                time.sleep(1) # Pequeña pausa
        
        # 2. SI LA IA FALLA, USAMOS EL BANCO (Plan B)
        if not exito:
            print(f"  ⚠️ Usando respaldo para {l}")
            backup = banco_completo.get(l, {
                "letra": l, 
                "pregunta": f"Palabra que empieza por {l}.", 
                "respuesta": "error", 
                "tipo": "CON LA"
            })
            # Aseguramos que el backup tenga la letra correcta
            backup["letra"] = l 
            rosco_final.append(backup)

    with open('preguntas.json', 'w', encoding='utf-8') as f:
        json.dump(rosco_final, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    generar_rosco_ia()
