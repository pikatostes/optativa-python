import math

radio = int(input("Introduzca el radio de la esfera: "))

diametro = radio * 2

longitud = 2 * math.pi * radio
area = math.pi * radio**2
volumen = 4/3 * math.pi * radio**3

datos = [longitud, area, volumen]

for dato in datos:
    print(dato)