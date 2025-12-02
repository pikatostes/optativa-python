# Verificar si un carácter específico está en la cadena con un ciclo y comparaciones.

word = input("Introduce a word: ")
letter = input("Introduce the letter to look for: ")

letterChecker = False

for i in word:
    if i == letter:
        letterChecker = True
        
if letterChecker == True:
    print(f"The letter '{letter}' has been found in '{word}'")
else:
    print(f"The letter '{letter}' hasn't been found in '{word}'")
    