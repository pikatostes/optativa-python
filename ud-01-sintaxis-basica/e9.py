try:
    edad = int(input("Introduzca su edad: "))
except ValueError:
    print("Error. Revise los datos introducidos")
    
if edad >= 18:
    print("Eres mayor de edad")
else:
    print("Eres menor de edad")