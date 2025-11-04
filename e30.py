cantidad = int(input("Introduzca la cantidad: "))
cantidadRestante = cantidad

billetes = [500, 200, 100, 50, 20, 10, 5]
cantidadBilletes = [0, 0, 0, 0, 0, 0, 0]

for i in range(len(billetes)):
    cantidadBilletes[i] = cantidadRestante / billetes[i]
    # round(number[, ndigits])
    cantidadRestante = cantidadRestante % billetes[i]
    
print(f"Para {cantidad} harán falta los siguientes billetes: ")
for j in range(len(cantidadBilletes)):
    print(f"{billetes[j]}€: {cantidadBilletes[j]}")