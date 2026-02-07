import json
import random

# BANCO MAESTRO AMPLIADO
banco_maestro = [
    {"letra": "A", "pregunta": "Satélite lanzado por la URSS en 1957.", "respuesta": "sputnik", "tipo": "CONTIENE LA"},
    {"letra": "A", "pregunta": "País cuya capital es Kabul.", "respuesta": "afganistan", "tipo": "CON LA"},
    {"letra": "A", "pregunta": "Persona que pilota una aeronave.", "respuesta": "aviador", "tipo": "CON LA"},
    {"letra": "B", "pregunta": "Escritor argentino autor de 'El Aleph'.", "respuesta": "borges", "tipo": "CON LA"},
    {"letra": "B", "pregunta": "Capital de Bélgica.", "respuesta": "bruselas", "tipo": "CON LA"},
    {"letra": "B", "pregunta": "Instrumento de viento madera de sonido muy grave.", "respuesta": "fagot", "tipo": "CONTIENE LA"},
    {"letra": "C", "pregunta": "Nombre del elemento químico con símbolo Cu.", "respuesta": "cobre", "tipo": "CON LA"},
    {"letra": "C", "pregunta": "País de origen del grupo musical ABBA.", "respuesta": "suecia", "tipo": "CONTIENE LA"},
    {"letra": "C", "pregunta": "Mamífero rumiante de cuello muy largo.", "respuesta": "jirafa", "tipo": "CONTIENE LA"},
    {"letra": "D", "pregunta": "Lugar donde se guardan los datos en informática.", "respuesta": "disco", "tipo": "CON LA"},
    {"letra": "D", "pregunta": "Sexto mes del año.", "respuesta": "junio", "tipo": "CONTIENE LA"},
    {"letra": "E", "pregunta": "Fase de la luna en la que no se ve.", "respuesta": "nueva", "tipo": "CONTIENE LA"},
    {"letra": "E", "pregunta": "País cuya capital es Nairobi.", "respuesta": "kenia", "tipo": "CONTIENE LA"},
    {"letra": "F", "pregunta": "Instrumento para medir la temperatura.", "respuesta": "termometro", "tipo": "CONTIENE LA"},
    {"letra": "F", "pregunta": "Nombre del elemento químico con símbolo F.", "respuesta": "fluor", "tipo": "CON LA"},
    {"letra": "G", "pregunta": "Nombre del gato que siempre persigue a Jerry.", "respuesta": "tom", "tipo": "CONTIENE LA"},
    {"letra": "G", "pregunta": "Punto más alto de la superficie terrestre.", "respuesta": "everest", "tipo": "CONTIENE LA"},
    {"letra": "H", "pregunta": "Gas noble usado en letreros brillantes.", "respuesta": "neon", "tipo": "CONTIENE LA"},
    {"letra": "H", "pregunta": "Animal que tiene una trompa larga.", "respuesta": "elefante", "tipo": "CONTIENE LA"},
    {"letra": "I", "pregunta": "Isla donde nació Napoleón Bonaparte.", "respuesta": "corcega", "tipo": "CONTIENE LA"},
    {"letra": "I", "pregunta": "País cuya capital es Reikiavik.", "respuesta": "islandia", "tipo": "CON LA"},
    {"letra": "J", "pregunta": "País del sol naciente.", "respuesta": "japon", "tipo": "CON LA"},
    {"letra": "J", "pregunta": "El planeta más grande del sistema solar.", "respuesta": "jupiter", "tipo": "CON LA"},
    {"letra": "L", "pregunta": "Nombre del satélite que orbita la Tierra.", "respuesta": "luna", "tipo": "CON LA"},
    {"letra": "L", "pregunta": "Ciudad de la luz y capital de Francia.", "respuesta": "paris", "tipo": "CONTIENE LA"},
    {"letra": "M", "pregunta": "Sustancia que transporta oxígeno en la sangre.", "respuesta": "hemoglobina", "tipo": "CONTIENE LA"},
    {"letra": "M", "pregunta": "Capital de España.", "respuesta": "madrid", "tipo": "CON LA"},
    {"letra": "N", "pregunta": "Planeta más lejano del sol.", "respuesta": "neptuno", "tipo": "CON LA"},
    {"letra": "N", "pregunta": "Símbolo químico del Sodio.", "respuesta": "na", "tipo": "CON LA"},
    {"letra": "O", "pregunta": "Líquido transparente sin olor ni sabor.", "respuesta": "agua", "tipo": "CONTIENE LA"},
    {"letra": "O", "pregunta": "Metal precioso de color amarillo.", "respuesta": "oro", "tipo": "CON LA"},
    {"letra": "P", "pregunta": "Ciudad italiana sepultada por el Vesubio.", "respuesta": "pompeya", "tipo": "CON LA"},
    {"letra": "P", "pregunta": "Órgano que bombea sangre.", "respuesta": "corazon", "tipo": "CONTIENE LA"},
    {"letra": "Q", "pregunta": "Hueso que forma la rodilla.", "respuesta": "rotula", "tipo": "CONTIENE LA"},
    {"letra": "Q", "pregunta": "Alimento sólido que se obtiene por maduración de la cuajada de la leche.", "respuesta": "queso", "tipo": "CON LA"},
    {"letra": "R", "pregunta": "Línea que une el centro del círculo con el borde.", "respuesta": "radio", "tipo": "CON LA"},
    {"letra": "R", "pregunta": "Animal que vive en el desierto y tiene joroba.", "respuesta": "dromedario", "tipo": "CONTIENE LA"},
    {"letra": "S", "pregunta": "Nombre de la estrella de nuestro sistema.", "respuesta": "sol", "tipo": "CON LA"},
    {"letra": "S", "pregunta": "País con forma de bota.", "respuesta": "italia", "tipo": "CONTIENE LA"},
    {"letra": "T", "pregunta": "Animal que lleva su casa a cuestas.", "respuesta": "tortuga", "tipo": "CON LA"},
    {"letra": "T", "pregunta": "Famoso barco hundido en 1912.", "respuesta": "titanic", "tipo": "CON LA"},
    {"letra": "U", "pregunta": "País cuya capital es Montevideo.", "respuesta": "uruguay", "tipo": "CON LA"},
    {"letra": "U", "pregunta": "Séptimo planeta del sistema solar.", "respuesta": "urano", "tipo": "CON LA"},
    {"letra": "V", "pregunta": "Volcán que destruyó Pompeya.", "respuesta": "vesubio", "tipo": "CON LA"},
    {"letra": "V", "pregunta": "Planeta más caluroso del sistema solar.", "respuesta": "venus", "tipo": "CON LA"},
    {"letra": "X", "pregunta": "Gas noble usado en faros de coches.", "respuesta": "xenon", "tipo": "CON LA"},
    {"letra": "X", "pregunta": "Instrumento de láminas golpeadas por mazas.", "respuesta": "xilofono", "tipo": "CON LA"},
    {"letra": "Y", "pregunta": "Material que se usa para pizarras.", "respuesta": "pizarra", "tipo": "CONTIENE LA"},
    {"letra": "Y", "pregunta": "Material blanco para escayolar.", "respuesta": "yeso", "tipo": "CON LA"},
    {"letra": "Z", "pregunta": "Hueso del brazo entre hombro y codo.", "respuesta": "humero", "tipo": "CONTIENE LA"},
    {"letra": "Z", "pregunta": "Calzado que cubre el pie.", "respuesta": "zapato", "tipo": "CON LA"}
]

def generar_rosco():
    letras = "ABCDEFGHIJLMNOPQRSTUVXYZ"
    nuevo_rosco = []
    for letra in letras:
        # Filtramos todas las opciones que coinciden con la letra
        opciones = [p for p in banco_maestro if p['letra'].upper() == letra]
        if opciones:
            # Elegimos UNA al azar de entre todas las disponibles para esa letra
            nuevo_rosco.append(random.choice(opciones))
    
    # Escribimos el archivo preguntas.json
    with open('preguntas.json', 'w', encoding='utf-8') as f:
        json.dump(nuevo_rosco, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    generar_rosco()
