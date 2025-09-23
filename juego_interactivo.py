import random

print("=== Juego educativo: Ingeniería en Energías Limpias ===")
print("Responde con el número de la opción correcta.")
print("Escribe 'salir' para terminar.")

puntos = 0

preguntas = [
    ("1. ¿Cuál es la eficiencia típica de un panel solar comercial?\n1) 5-10%\n2) 15-22%\n3) 40-50%", "2"),
    ("2. ¿Qué unidad se usa para medir la energía eléctrica?\n1) Watt\n2) Volt\n3) Kilowatt-hora", "3"),
    ("3. ¿Qué recurso es renovable?\n1) Carbón\n2) Biomasa\n3) Gas natural", "2"),
    ("4. ¿Cuál es el país con mayor capacidad instalada de energía solar?\n1) China\n2) Alemania\n3) Brasil", "1"),
    ("5. Una turbina eólica genera más electricidad si…\n1) El viento es constante y fuerte\n2) Está apagada\n3) Hace calor", "1"),
    ("6. ¿Qué tipo de energía usa movimiento del agua?\n1) Geotérmica\n2) Hidroeléctrica\n3) Biomasa", "2"),
    ("7. ¿Qué gas se reduce con energías limpias?\n1) CO₂\n2) N₂\n3) O₂", "1"),
    ("8. ¿Cuál es el principal reto de la energía solar?\n1) Se agota rápido\n2) Intermitencia (no siempre hay sol)\n3) Es contaminante", "2"),
    ("9. ¿Qué país es líder en generación de energía eólica marina?\n1) Dinamarca\n2) México\n3) Chile", "1"),
    ("10. ¿Qué tipo de batería se usa más en energías renovables?\n1) Plomo-ácido\n2) Ion-Litio\n3) Carbón", "2"),
    ("11. ¿Qué significa 'autoconsumo energético'?\n1) Vender energía a otros\n2) Generar y usar tu propia energía\n3) Comprar energía más barata", "2"),
    ("12. ¿Qué instrumento mide la radiación solar?\n1) Termómetro\n2) Piranómetro\n3) Voltímetro", "2"),
    ("13. ¿Qué país apostó fuertemente por la energía geotérmica?\n1) Islandia\n2) Egipto\n3) Colombia", "1"),
    ("14. ¿Qué porcentaje de la matriz energética mundial proviene de fósiles (aprox. 2023)?\n1) 20%\n2) 60%\n3) 80%", "3"),
    ("15. ¿Qué acción en un hogar reduce más el consumo energético?\n1) Reemplazar bombillos por LED\n2) Pintar paredes\n3) Usar más televisores", "1"),
]

random.shuffle(preguntas)

for i, (pregunta, correcta) in enumerate(preguntas, start=1):
    print("Recuerda: escribe 'salir' para terminar")
    respuesta = input(pregunta + "\nTu respuesta: ")

    if respuesta.lower() == "salir":
        break

    if respuesta == correcta:
        print("¡Correcto!")
        puntos += 1
    else:
        print("XXXXXXXX Incorrecto XXXXXXXXX")

print("\nJuego terminado. Tu puntaje fue:", puntos, "de", len(preguntas))
