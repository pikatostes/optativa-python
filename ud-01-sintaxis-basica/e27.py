opcion = 0
notaDiez = False

while opcion != -1:
    opcion = int(input("Introduzca un número entero del 0 al 10 (-1 para terminar): "))
    
    if opcion == -1:
        break
    elif opcion == 10:
        notaDiez = True

if notaDiez:
    print("Se introdujo un diez")
else:
    print("No se introdujo un diez")