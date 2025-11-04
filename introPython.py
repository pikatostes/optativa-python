def e1():
    print("Buenas tardes")

def e2():
    area = 5 ** 2

    print(f"El area del cuadrado es de {area}")

def e3():
    lado = int(input("Introduzca el area del cuadrado: "))

    area = lado ** 2

    print(f"El area es de {area}")
    
ejercicios = {
    1: e1,
    2: e2,
    3: e3
}

option = int(input("Introduzca un número: "))

ejercicios[option]()