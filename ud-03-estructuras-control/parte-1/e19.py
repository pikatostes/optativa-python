def ingresarDinero(saldo_actual):
    try:
        ingreso = float(input("➡️ Ingrese la cantidad a depositar: "))
        if ingreso > 0:
            saldo_actual += ingreso
            print(f"✅ Depósito exitoso. Nuevo saldo: {saldo_actual:.2f}€")
        else:
            print("❌ La cantidad a depositar debe ser mayor que cero.")
    except ValueError:
        print("❌ Entrada no válida. Por favor, ingrese un número.")
    return saldo_actual # Devolver el saldo actualizado

def retirarDinero(saldo_actual):
    """Permite al usuario retirar dinero y actualiza el saldo."""
    try:
        retiro = float(input("➡️ Ingrese la cantidad a retirar: "))
        if retiro > 0:
            if retiro <= saldo_actual:
                saldo_actual -= retiro
                print(f"✅ Retiro exitoso. Nuevo saldo: {saldo_actual:.2f}€")
            else:
                print("❌ Saldo insuficiente para realizar el retiro.")
        else:
            print("❌ La cantidad a retirar debe ser mayor que cero.")
    except ValueError:
        print("❌ Entrada no válida. Por favor, ingrese un número.")
    return saldo_actual # Devolver el saldo actualizado

def mostrarMenu(saldo_actual):
    """Muestra el menú, pide una opción y realiza la acción correspondiente."""
    print("\n--- 🏧 Bienvenido a su cajero ---")
    print(f"💰 Saldo actual: {saldo_actual:.2f}€") # Formato de moneda
    print("--- Elija una opción: ---")
    print("1. Ingresar")
    print("2. Retirar")
    print("3. Salir")
    
    opcion = 0
    try:
        opcion = int(input("Opcion: "))
    except ValueError:
        print("❌ Entrada no válida. Por favor, ingrese 1, 2 o 3.")
        return saldo_actual, 0 # Devolver el saldo y una opción no válida para continuar

    if opcion == 1:
        saldo_actual = ingresarDinero(saldo_actual)
    elif opcion == 2:
        saldo_actual = retirarDinero(saldo_actual)
    elif opcion == 3:
        print("👋 Gracias por usar nuestro cajero. ¡Hasta pronto!")
        return saldo_actual, 3 # Devolver la opción de salida
    else:
        print("❌ Opción no válida. Por favor, intente de nuevo.")

    return saldo_actual, 0 # Devolver el saldo actualizado y una opción para continuar

# --- Inicio del Programa Principal ---

saldo = 1000.00
opcion = 0 # Inicializar opcion a un valor diferente de 3 para entrar en el bucle

while opcion != 3:
    # La función retorna el nuevo saldo y la opción elegida
    saldo, opcion = mostrarMenu(saldo)
