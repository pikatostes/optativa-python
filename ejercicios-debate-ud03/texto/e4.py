# Construir manualmente una nueva cadena añadiendo un carácter a la vez (ejemplo: filtrar caracteres o construir cadenas invertidas).

newString = ""
letter = " "

while letter != "":
    letter = input("Introduce a letter: ")
    newString += letter
    
print(newString)