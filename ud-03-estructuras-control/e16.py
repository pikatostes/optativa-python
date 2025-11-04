num = -1

while num < 0 or num > 99999:
  try:
    num = int(input("Introduzca un número de 0 a 99999: "))
  except:
    print('Error. El número ha de ser entre 0 a 99999')

num = str(num)

print(f"El número tiene {len(num)} dígitos")




