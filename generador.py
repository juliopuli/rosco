import json
import random

# Diccionario gigante de posibilidades (puedes ampliarlo cuanto quieras)
banco_maestro = [
    {"letra": "A", "pregunta": "Satélite lanzado por la Unión Soviética en 1957.", "respuesta": "sputnik", "tipo": "CONTIENE LA"},
    {"letra": "A", "pregunta": "País cuya capital es Kabul.", "respuesta": "afganistan", "tipo": "CON LA"},
    {"letra": "B", "pregunta": "Escritor argentino autor de 'El Aleph'.", "respuesta": "borges", "tipo": "CON LA"},
    {"letra": "C", "pregunta": "Nombre del elemento químico con símbolo Cu.", "respuesta": "cobre", "tipo": "CON LA"},
    {"letra": "D", "pregunta": "Lugar donde se guardan los datos en informática.", "respuesta": "disco", "tipo": "CON LA"},
    {"letra": "E", "pregunta": "Fase de la luna en la que no se ve.", "respuesta": "nueva", "tipo": "CONTIENE LA"},
    {"letra": "F", "pregunta": "Instrumento para medir la temperatura.", "respuesta": "termometro", "tipo": "CONTIENE LA"},
    {"letra": "G", "pregunta": "Nombre del gato que siempre persigue a Jerry.", "respuesta": "tom", "tipo": "CONTIENE LA"},
    {"letra": "H", "pregunta": "Gas noble usado en bombillas y letreros brillantes.", "respuesta": "neon", "tipo": "CONTIENE LA"},
    {"letra": "I", "pregunta": "Isla donde nació Napoleón Bonaparte.", "respuesta": "corcega", "tipo": "CONTIENE LA"},
    {"letra": "J", "pregunta": "Punto más alto de la superficie terrestre.", "respuesta": "everest", "tipo": "CONTIENE LA"},
    {"letra": "L", "pregunta": "Nombre del satélite que orbita la Tierra.", "respuesta": "luna", "tipo": "CON LA"},
    {"letra": "M", "pregunta": "Sustancia que transporta el oxígeno en la sangre.", "respuesta": "hemoglobina", "tipo": "CONTIENE LA"},
    {"letra": "N", "pregunta": "Planeta más lejano del sol.", "respuesta": "neptuno", "tipo": "CON LA"},
    {"letra": "O", "pregunta": "Líquido transparente sin olor ni sabor.", "respuesta": "agua", "tipo": "CONTIENE LA"},
    {"letra": "P", "pregunta": "Ciudad italiana sepultada por el Vesubio.", "respuesta": "pompeya", "tipo": "CON LA"},
    {"letra": "Q", "pregunta": "Hueso que forma la rodilla.", "respuesta": "rotula", "tipo": "CONTIENE LA"},
    {"letra": "R", "pregunta": "Línea que une el centro del círculo con el borde.", "respuesta": "radio", "tipo": "CON LA"},
    {"letra": "S", "pregunta": "Nombre de la estrella de nuestro sistema.", "respuesta": "sol", "tipo": "CON LA"},
    {"letra": "T", "pregunta": "Animal que lleva su casa a cuestas.", "respuesta": "tortuga", "tipo": "CON LA"},
    {"letra": "U", "pregunta": "País cuya capital es Montevideo.", "respuesta": "uruguay", "tipo": "CON LA"},
    {"letra": "V", "pregunta": "Nombre del volcán que destruyó Pompeya.", "respuesta": "vesubio", "tipo": "CON LA"},
    {"letra": "X", "pregunta": "Instrumento musical de láminas de metal.", "respuesta": "glockenspiel", "tipo": "CONTIENE LA"},
    {"letra": "Y", "pregunta": "Material con el que se hacen las pizarras naturales.", "respuesta": "pizarra", "tipo": "CONTIENE LA"},
    {"letra": "Z", "pregunta": "Hueso que une el hombro con el codo.", "respuesta": "humero", "tipo": "CONTIENE LA"}
]

def generar_rosco():
    letras = "ABCDEFGHIJLMNOPQRSTUVXYZ"
    nuevo_rosco = []
    for letra in letras:
        opciones = [p for p in banco_maestro if p['letra'] == letra]
        if opciones:
            nuevo_rosco.append(random.choice(opciones))
    
    with open('preguntas.json', 'w', encoding='utf-8') as f:
        json.dump(nuevo_rosco, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    generar_rosco()
