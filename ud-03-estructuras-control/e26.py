import random

dado1 = random.randint(1, 6)
dado2 = random.randint(1, 6)
dado3 = random.randint(1, 6)

print(f"dado1: {dado1}, dado2: {dado2}, dado3: {dado3}")

if dado1 == 6 and dado2 == 6 and dado3 == 6:
    print("Excelente")
elif dado1 == 6 and dado2 == 6 or dado2 == 6 and dado3 == 6 or dado1 == 6 and dado3 == 6:
    print("Muy bien")
elif dado1 == 6 or dado2 == 6 or dado3 == 6:
    print("Regular")
else:
    print("Pésimo")