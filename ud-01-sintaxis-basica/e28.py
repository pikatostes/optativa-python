sumaPares = 0
sumaImpares = 0

for i in range(100, 201):
    if i % 2 == 0:
        sumaPares += i
    else:
        sumaImpares += i

print(f"Suma pares: {sumaPares}, Suma impares: {sumaImpares}")