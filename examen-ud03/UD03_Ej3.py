text = ""
letter = ""
equalsIntroduced = False
option = 0

while option != 3:
    print("Bienvenido")
    print("[1] Introducir texto carácter por carácter")
    print("[2] Mostrar cadena de texto")
    print("[3] Salir del programa")

    option = int(input("Introduzca su opción: "))

    match option:
        case 1:
            text = ""
            while equalsIntroduced == False:
                letter = str(input("Introduce a letter: "))
                if letter == "=":
                    equalsIntroduced = True
                else:
                    text += letter
        case 2:
            for i in text:
                print(i)
        case 3:
            exit
