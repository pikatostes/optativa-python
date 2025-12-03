height = int(input("Introduce a height: "))

mid = height // 2 + 1
print(mid)

for i in range(mid):
    if i == 0:
        print(" " * (mid - 1) + "*")
    elif i < mid / 2:
        print(" " * (mid - i - 1) + "*" * (2*i+1))
    else:
        print()