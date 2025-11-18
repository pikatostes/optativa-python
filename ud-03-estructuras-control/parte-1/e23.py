while True:
    try:
        valorCompra = float(input("Introduzca el valor de la compra: "))
        break
    except ValueError:
        print('Ha ocurrido un error')

while True:
    print("¿Cómo se efectuó el pago?")
    print("[1] Efectivo")
    print("[2] Tarjeta")
    try:
        
        option = int(input())
        
        if option == 1:
            valorCompra *= 0.95
            break
        elif option == 2:
            valorCompra *= 1.03
            break
    except ValueError:
        print("Ha ocurrido un error")

print(f"Su coste total es de {valorCompra}")