height = int(input("Introduce an ODD height: "))

if height % 2 == 0:
    print("Height must be odd")
    exit()

mid = height // 2
line3a = mid - 1
line3b = mid + 1

for i in range(height // 2+1):
    if i == 0:
        print("*" * height)
    elif i == mid:
        print("*" + " " * (height-2) + "*")
    elif i == height // 2-1:
        print("*" + " " * i + "*" + " " * i + "*")
    else:
        print("*" + " " * i + "*" + " " * (height-2*i-4) + "*" + " " * i + "*")
        
for i in range(height // 2 - 1, -1, -1):
    if i == 0:
        print("*" * height)
    elif i == mid:
        print("*" + " " * (height-2) + "*")
    elif i == height // 2-1:
        print("*" + " " * i + "*" + " " * i + "*")
    else:
        print("*" + " " * i + "*" + " " * (height-2*i-4) + "*" + " " * i + "*")
