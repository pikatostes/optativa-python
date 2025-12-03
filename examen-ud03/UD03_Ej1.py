height = int(input("Introduce a height: "))

for i in range(1, height + 1):
    print(f"{i}" * i)
    
for i in range(height - 1, 0, -1):
    print(f"{i}" * i)