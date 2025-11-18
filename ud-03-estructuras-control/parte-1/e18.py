try:
  num = float(input("Introduzca un número por teclado: "))
except:
  print('Ha ocurrido un error')
  
if num % 10 == 0:
    print("El número es multiplo de 10")
else:
    print("El número no es multiplo de 10")