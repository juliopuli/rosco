import os
import json
import google.generativeai as genai
import time
import random

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    exit(1)

genai.configure(api_key=api_key)

def limpiar(t):
    if not t: return ""
    return t.lower().strip().replace('á','a').replace('é','e').replace('í','i').replace('ó','o').replace('ú','u').replace('ü','u')

def generar_rosco_ia():
    model = genai.GenerativeModel('gemini-1.5-flash')
    letras = "ABCDEFGHIJLMNOPQRSTUVXYZ"
    rosco_final = []

    # BANCO SEGURO CON DEFINICIONES CONCRETAS
    banco = {
        "A": {"letra":"A", "pregunta":"Vehículo provisto de alas que se desplaza por el aire gracias a uno o varios motores.", "respuesta":"avion", "tipo":"CON LA"},
        "B": {"letra":"B", "pregunta":"Mamífero marino de gran tamaño que respira por un orificio en la parte superior de la cabeza.", "respuesta":"ballena", "tipo":"CON LA"},
        "C": {"letra":"C", "pregunta":"Edificio o parte de él que sirve de vivienda para una persona o una familia.", "respuesta":"casa", "tipo":"CON LA"},
        "D": {"letra":"D", "pregunta":"Pieza cúbica con puntos del uno al seis que se usa en diversos juegos de azar.", "respuesta":"dado", "tipo":"CON LA"},
        "E": {"letra":"E", "pregunta":"Animal mamífero de gran tamaño con una larga trompa y grandes orejas que vive en África o Asia.", "respuesta":"elefante", "tipo":"CON LA"},
        "F": {"letra":"F", "pregunta":"Torre alta situada en la costa con una luz potente para guiar a los navegantes durante la noche.", "respuesta":"faro", "tipo":"CON LA"},
        "G": {"letra":"G", "pregunta":"Animal mamífero felino de tamaño pequeño, doméstico y con gran agilidad.", "respuesta":"gato", "tipo":"CON LA"},
        "H": {"letra":"H", "pregunta":"Agua que se ha vuelto sólida y fría debido a una temperatura muy baja.", "respuesta":"hielo", "tipo":"CON LA"},
        "I": {"letra":"I", "pregunta":"Porción de tierra que está completamente rodeada de agua por todas partes.", "respuesta":"isla", "tipo":"CON LA"},
        "J": {"letra":"J", "pregunta":"Animal mamífero de África con un cuello extremadamente largo y manchas en su piel.", "respuesta":"jirafa", "tipo":"CON LA"},
        "L": {"letra":"L", "pregunta":"Cuerpo celeste que gira alrededor de la Tierra y que refleja la luz del Sol durante la noche.", "respuesta":"luna", "tipo":"CON LA"},
        "M": {"letra":"M", "pregunta":"Fruto del manzano, de forma redondeada y sabor dulce o ácido, con piel de color verde, amarilla o roja.", "respuesta":"manzana", "tipo":"CON LA"},
        "N": {"letra":"N", "pregunta":"Color que se asocia con la oscuridad total y que es el opuesto al blanco.", "respuesta":"negro", "tipo":"CON LA"},
        "O": {"letra":"O", "pregunta":"Órgano externo del cuerpo humano y otros mamíferos que permite percibir los sonidos.", "respuesta":"oreja", "tipo":"CON LA"},
        "P": {"letra":"P", "pregunta":"Animal mamífero doméstico que desciende del lobo y es conocido por su lealtad al ser humano.", "respuesta":"perro", "tipo":"CON LA"},
        "Q": {"letra":"Q", "pregunta":"Alimento sólido o semisólido que se obtiene mediante la maduración de la cuajada de la leche.", "respuesta":"queso", "tipo":"CON LA"},
        "R": {"letra":"R", "pregunta":"Máquina o instrumento que sirve para medir el tiempo y dividir el día en horas, minutos y segundos.", "respuesta":"reloj", "tipo":"CON LA"},
        "S": {"letra":"S", "pregunta":"Estrella con luz propia que ocupa el centro de nuestro sistema planetario y nos da calor.", "respuesta":"sol", "tipo":"CON LA"},
        "T": {"letra":"T", "pregunta":"Medio de transporte formado por una serie de vagones arrastrados por una locomotora sobre raíles.", "respuesta":"tren", "tipo":"CON LA"},
        "U": {"letra":"U", "pregunta":"Fruta pequeña, de forma redonda u ovalada, que crece en racimos y se utiliza para hacer vino.", "respuesta":"uva", "tipo":"CON LA"},
        "V": {"letra":"V", "pregunta":"Estación del año situada entre la primavera y el otoño en la que las temperaturas son más altas.", "respuesta":"verano", "tipo":"CON LA"},
        "X": {"letra":"X", "pregunta":"Instrumento musical de percusión compuesto por láminas de madera o metal afinadas.", "respuesta":"xilofono", "tipo":"CON LA"},
        "Y": {"letra":"Y", "pregunta":"Parte central de color amarillo del huevo de las aves.", "respuesta":"yema", "tipo":"CON LA"},
        "Z": {"letra":"Z", "pregunta":"Calzado que cubre el pie para protegerlo al caminar, generalmente con suela y cordones.", "respuesta":"zapato", "tipo":"CON LA"}
    }

    for l in letras:
        exito = False
        try:
            # Nuevo Prompt más exigente
            prompt = (f"Genera una definición detallada de diccionario para la letra {l} en el juego Pasapalabra. "
                      f"La definición debe ser profesional, de al menos 10 palabras, y no debe ser ambigua. "
                      f"Respuesta en ESPAÑOL. JSON: {{\"letra\":\"{l}\", \"pregunta\":\"...\", \"respuesta\":\"...\", \"tipo\":\"CON LA\"}}")
            
            res = model.generate_content(prompt)
            data = json.loads(res.text.replace("```json", "").replace("```", "").strip())
            
            resp_limpia = limpiar(data['respuesta'])
            if (data['tipo'] == "CON LA" and resp_limpia.startswith(l.lower())) or (l.lower() in resp_limpia):
                rosco_final.append(data)
                exito = True
        except: pass
        
        if not exito:
            rosco_final.append(banco[l])

    with open('preguntas.json', 'w', encoding='utf-8') as f:
        json.dump(rosco_final, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    generar_rosco_ia()
