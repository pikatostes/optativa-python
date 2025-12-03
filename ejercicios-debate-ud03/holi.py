# Extraer subcadenas usando slicing (rebanado de cadenas sin usar listas).KO

height = int(input("Introduce a height:"))
mashNum = ""

for i in range(height):
    print(" " * (height - i - 1) + "{mashNum}" + i + reversed(mashNum))
    mashNum += str(i)