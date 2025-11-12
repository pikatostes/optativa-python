nota = float(input("Introduzca su nota: "))

if nota < 0 or nota > 10:
    print("Nota fuera de rango (debe estar entre 0 y 10).")
elif nota < 3:
    print("Muy deficiente")
elif nota < 5:
    print("Insuficiente")
elif nota < 6:
    print("Suficiente")
elif nota < 7:
    print("Bien")
elif nota < 9:
    print("Notable")
elif nota <= 10:
    print("Sobresaliente")