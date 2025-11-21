word = input("Introduce a word: ")
letter = input("Introduce the letter to look for: ")
letterCounter = 0

for i in word:
    if i == letter:
        letterCounter += 1
        
print(f"The letter '{letter}' has been found {letterCounter} times")