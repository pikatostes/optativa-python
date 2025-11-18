try:
    altura = int(input("Introduzca la altura de la pirámide: "))
    
    if altura <= 0:
        raise ValueError
except ValueError:
    print("Error. Solo se permiten enteros.")
    
for i in range(1, altura+1):
    print("*" * i)