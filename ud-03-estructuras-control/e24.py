while True:
    print("\n Bienvenido a Tiendas Don Pepe")
    try:
        montoCompra = float(input("Introduzca el monto de compra: "))
        break
    except ValueError:
        print("Ha ocurrido un error")
        
while True:
    print("[1] Lunes")
    print("[2] Martes")
    print("[3] Miércoles")
    print("[4] Jueves")
    print("[5] Viernes")
    print("[6] Sábado")
    print("[7] Domingo")
    
    try:
        dia = int(input("Introduzca una opción: "))
        
        if dia == 2 or dia == 4:
            montoCompra *= 0.85
            break
        else:
            break
        
    except ValueError:
        print("Ha ocurrido un error")

print(f"El valor del monto de compra es de: {montoCompra}")