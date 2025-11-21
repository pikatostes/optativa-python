height = int(input("Introduce an ODD height: "))

if height % 2 == 0:
    print("The height must be ODD")
    exit

for i in range(height):
    if i % 2 == 0:
        print("*" + " *" * (height-2) + " *")
    else:
        print("*   " * (height//2+1))