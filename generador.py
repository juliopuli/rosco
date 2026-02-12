import os
import json
import google.generativeai as genai
import time
import random

# Configuración de la API
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    exit(1)

genai.configure(api_key=api_key)

def limpiar(t):
    if not t: return ""
    return t.lower().strip().replace('á','a').replace('é','e').replace('í','i').replace('ó','o').replace('ú','u').replace('ü','u')

def generar_rosco_ia():
    model = genai.GenerativeModel('gemini-1.5-flash')
    letras = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"  # ✅ TODAS LAS LETRAS (27)
    rosco_final = []

    # BANCO DE RESPALDO REAL (Si la IA falla, usará estas preguntas de verdad)
    banco_real = {
        "A": {"letra":"A", "pregunta":"Vehículo con alas que vuela por el aire.", "respuesta":"avion", "tipo":"CON LA"},
        "B": {"letra":"B", "pregunta":"Mamífero marino de gran tamaño.", "respuesta":"ballena", "tipo":"CON LA"},
        "C": {"letra":"C", "pregunta":"Edificio donde vive una familia.", "respuesta":"casa", "tipo":"CON LA"},
        "D": {"letra":"D", "pregunta":"Pieza cúbica con puntos para jugar.", "respuesta":"dado", "tipo":"CON LA"},
        "E": {"letra":"E", "pregunta":"Animal con trompa y orejas grandes.", "respuesta":"elefante", "tipo":"CON LA"},
        "F": {"letra":"F", "pregunta":"Torre con luz para guiar barcos.", "respuesta":"faro", "tipo":"CON LA"},
        "G": {"letra":"G", "pregunta":"Animal que maúlla y caza ratones.", "respuesta":"gato", "tipo":"CON LA"},
        "H": {"letra":"H", "pregunta":"Agua congelada.", "respuesta":"hielo", "tipo":"CON LA"},
        "I": {"letra":"I", "pregunta":"Tierra rodeada de agua.", "respuesta":"isla", "tipo":"CON LA"},
        "J": {"letra":"J", "pregunta":"Animal con el cuello muy largo.", "respuesta":"jirafa", "tipo":"CON LA"},
        "K": {"letra":"K", "pregunta":"Arte marcial japonés con kimono.", "respuesta":"karate", "tipo":"CON LA"},
        "L": {"letra":"L", "pregunta":"Satélite de la Tierra que brilla de noche.", "respuesta":"luna", "tipo":"CON LA"},
        "M": {"letra":"M", "pregunta":"Fruto del manzano.", "respuesta":"manzana", "tipo":"CON LA"},
        "N": {"letra":"N", "pregunta":"Fruta con mucha vitamina C.", "respuesta":"naranja", "tipo":"CON LA"},
        "Ñ": {"letra":"Ñ", "pregunta":"Mamífero de Sudamérica parecido a la llama.", "respuesta":"ñandu", "tipo":"CON LA"},
        "O": {"letra":"O", "pregunta":"Órgano para escuchar.", "respuesta":"oreja", "tipo":"CON LA"},
        "P": {"letra":"P", "pregunta":"Animal amigo del hombre que ladra.", "respuesta":"perro", "tipo":"CON LA"},
        "Q": {"letra":"Q", "pregunta":"Alimento hecho de leche.", "respuesta":"queso", "tipo":"CON LA"},
        "R": {"letra":"R", "pregunta":"Aparato para ver la hora.", "respuesta":"reloj", "tipo":"CON LA"},
        "S": {"letra":"S", "pregunta":"Estrella que nos da luz y calor.", "respuesta":"sol", "tipo":"CON LA"},
        "T": {"letra":"T", "pregunta":"Vehículo sobre raíles.", "respuesta":"tren", "tipo":"CON LA"},
        "U": {"letra":"U", "pregunta":"Fruta que crece en racimos.", "respuesta":"uva", "tipo":"CON LA"},
        "V": {"letra":"V", "pregunta":"Estación de más calor.", "respuesta":"verano", "tipo":"CON LA"},
        "W": {"letra":"W", "pregunta":"Red mundial de información e internet.", "respuesta":"web", "tipo":"CONTIENE LA"},
        "X": {"letra":"X", "pregunta":"Prueba escolar para evaluar.", "respuesta":"examen", "tipo":"CONTIENE LA"},
        "Y": {"letra":"Y", "pregunta":"Barco de recreo grande.", "respuesta":"yate", "tipo":"CON LA"},
        "Z": {"letra":"Z", "pregunta":"Calzado para el pie.", "respuesta":"zapato", "tipo":"CON LA"}
    }

    for l in letras:
        exito = False
        try:
            prompt = (f"Eres el guionista de Pasapalabra. Genera una pregunta para la letra {l}. "
                      f"Que sea una definición profesional y clara. "
                      f"JSON: {{\"letra\":\"{l}\", \"pregunta\":\"...\", \"respuesta\":\"...\", \"tipo\":\"CON LA\"}}")
            
            res = model.generate_content(prompt)
            # Limpiamos posibles formatos de la IA
            limpio = res.text.replace("```json", "").replace("```", "").strip()
            data = json.loads(limpio)
            
            if l.lower() in limpiar(data['respuesta']):
                rosco_final.append(data)
                exito = True
        except: pass
        
        if not exito:
            rosco_final.append(banco_real[l])

    with open('preguntas.json', 'w', encoding='utf-8') as f:
        json.dump(rosco_final, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    generar_rosco_ia()
