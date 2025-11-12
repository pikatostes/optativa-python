try:
    distanciaMillasMarinas = float(input("Introduzca la distancia en millas marinas: "))
except ValueError:
    print("Error. Revise los datos introducidos")
    
distanciaMetros = distanciaMillasMarinas * 1.852

print(f"La distancia de {distanciaMillasMarinas} millas marinas equivale a {distanciaMetros} metros")