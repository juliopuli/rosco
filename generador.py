import os
import json
import google.generativeai as genai
import time
import random
from datetime import datetime

# 1. CONFIGURACIÓN DE SEGURIDAD
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("❌ ERROR: No se encontró la GEMINI_API_KEY en los secretos de GitHub.")
    exit(1)

genai.configure(api_key=api_key)

def limpiar_texto(t):
    if not t: return ""
    # Quita tildes y pasa a minúsculas para una validación justa
    s = t.lower().strip()
    s = s.replace('á','a').replace('é','e').replace('í','i').replace('ó','o').replace('ú','u').replace('ü','u')
    return s

def validar_palabra(letra, respuesta, tipo):
    l = letra.lower()
    r = limpiar_texto(respuesta)
    if not r or len(r) < 3: return False
    
    if "CON LA" in tipo.upper():
        return r.startswith(l)
    else: # CONTIENE LA
        return l in r

def generar_rosco_ia():
    model = genai.GenerativeModel('gemini-1.5-flash')
    letras = "ABCDEFGHIJLMNOPQRSTUVXYZ"
    rosco_final = []

    # 2. BANCO DE RESPALDO MANUAL (100% VERIFICADO)
    banco_emergencia = {
        "A": {"pregunta": "Cuerpo celeste que brilla con luz propia.", "respuesta": "astro", "tipo": "CON LA"},
        "B": {"pregunta": "Objeto que sirve para iluminar una estancia.", "respuesta": "bombilla", "tipo": "CON LA"},
        "C": {"pregunta": "Edificio o lugar donde se vive.", "respuesta": "casa", "tipo": "CON LA"},
        "D": {"pregunta": "Objeto cúbico con puntos que se usa para jugar.", "respuesta": "dado", "tipo": "CON LA"},
        "E": {"pregunta": "Animal mamífero con trompa y grandes orejas.", "respuesta": "elefante", "tipo": "CON LA"},
        "F": {"pregunta": "Torre alta con luz que guía a los barcos.", "respuesta": "faro", "tipo": "CON LA"},
        "G": {"pregunta": "Animal doméstico que maúlla y caza ratones.", "respuesta": "gato", "tipo": "CON LA"},
        "H": {"pregunta": "Masa de agua congelada por el frío.", "respuesta": "hielo", "tipo": "CON LA"},
        "I": {"pregunta": "Porción de tierra rodeada de agua por todas partes.", "respuesta": "isla", "tipo": "CON LA"},
        "J": {"pregunta": "Líquido que se extrae de las frutas al exprimirlas.", "respuesta": "jugo", "tipo": "CON LA"},
        "L": {"pregunta": "Satélite natural que gira alrededor de la Tierra.", "respuesta": "luna", "tipo": "CON LA"},
        "M": {"pregunta": "Fruta de piel roja, verde o amarilla.", "respuesta": "manzana", "tipo": "CON LA"},
        "N": {"pregunta": "Color que representa la oscuridad total.", "respuesta": "negro", "tipo": "CON LA"},
        "O": {"pregunta": "Parte del cuerpo que sirve para oír.", "respuesta": "oido", "tipo": "CON LA"},
        "P": {"pregunta": "Animal mamífero conocido como el mejor amigo del hombre.", "respuesta": "perro", "tipo": "CON LA"},
        "Q": {"pregunta": "Alimento sólido que se obtiene de la leche.", "respuesta": "queso", "tipo": "CON LA"},
        "R": {"pregunta": "Aparato que sirve para medir el tiempo.", "respuesta": "reloj", "tipo": "CON LA"},
        "S": {"pregunta": "Mueble que sirve para sentarse.", "respuesta": "silla", "tipo": "CON LA"},
        "T": {"pregunta": "Vehículo pesado que circula sobre raíles.", "respuesta": "tren", "tipo": "CON LA"},
        "U": {"pregunta": "Fruta pequeña que crece en racimos.", "respuesta": "uva", "tipo": "CON LA"},
        "V": {"pregunta": "Estación del año donde hace más calor.", "respuesta": "verano", "tipo": "CON LA"},
        "X": {"pregunta": "Prueba o evaluación de conocimientos.", "respuesta": "examen", "tipo": "CONTIENE LA"},
        "Y": {"pregunta": "Parte central y amarilla del huevo.", "respuesta": "yema", "tipo": "CON LA"},
        "Z": {"pregunta": "Calzado que cubre el pie para caminar.", "respuesta": "zapato", "tipo": "CON LA"}
    }

    print(f"--- Iniciando generación: {datetime.now()} ---")

    for l in letras:
        exito_letra = False
        intentos = 0
        
        while intentos < 2 and not exito_letra:
            try:
                # Pedimos a la IA una pregunta única
                prompt = f"Genera una pregunta de Pasapalabra para la letra {l}. Respuesta en ESPAÑOL. Formato JSON estricto: {{\"letra\":\"{l}\", \"pregunta\":\"...\", \"respuesta\":\"...\", \"tipo\":\"CON LA\"}}"
                response = model.generate_content(prompt)
                
                # Limpieza de la respuesta de la IA
                raw_text = response.text.replace("```json", "").replace("```", "").strip()
                data = json.loads(raw_text)
                
                # VALIDACIÓN CRÍTICA: ¿La respuesta de la IA es real y contiene la letra?
                if validar_palabra(l, data['respuesta'], data['tipo']):
                    rosco_final.append(data)
                    exito_letra = True
                    print(f"✅ {l}: IA generó correctamente '{data['respuesta']}'")
                else:
                    print(f"⚠️ {l}: IA dio respuesta inválida. Reintentando...")
                    intentos += 1
            except Exception as e:
                intentos += 1
                time.sleep(1)

        # Si la IA falla tras los intentos, usamos el BACKUP MANUAL
        if not exito_letra:
            print(f"🆘 {l}: Usando banco de emergencia.")
            backup = banco_emergencia[l]
            rosco_final.append(backup)

    # 3. GUARDAR Y FORZAR ACTUALIZACIÓN
    with open('preguntas.json', 'w', encoding='utf-8') as f:
        json.dump(rosco_final, f, ensure_ascii=False, indent=2)
        # Añadimos saltos de línea aleatorios al final para que el archivo cambie siempre de tamaño
        f.write("\n" * random.randint(1, 5))

    print(f"--- Proceso finalizado con éxito ---")

if __name__ == "__main__":
    generar_rosco_ia()
