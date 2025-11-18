try:
    username = str(input("Introduzca su usuario: "))
    password = str(input("Introduzca su contraseña: "))
except:
  print("Ha ocurrido un error.")

if username == "alex" and password == "alex":
    print("Acceso autorizado. Bienvenido.")
else:
    print("Error en credenciales.")