try:
    precioSinDescuento = float(input("Introduzca el precio SIN DESCUENTO del producto: "))

    precioConDescuento = float(input("Introduzca el precio CON DESCUENTO del producto: "))
except ValueError:
  print('Error. Revise los datos introducidos')

porcentaje = ((precioConDescuento * 100) / precioSinDescuento) - 100

print(f"El porcentaje de descuento es del {porcentaje}%")
