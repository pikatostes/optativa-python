matricula = 0
mensualidad = 0
igv = 0

try:
    nombre = str(input("Introduzca su nombre: "))
    
    print("[1] Ing. de Sistemas")
    print("[2] Derecho")
    print("[3] Ing. Naviera")
    print("[4] Ing. Pesquera")
    print("[5] Contabilidad")
    print("[6] Administración")
    facultad = int(input("Ingrese su facultad: "))
except ValueError:
    print("Ha ocurrido un error")
    
if facultad == 1:
    matricula = 350
    mensualidad = 650
elif facultad == 2:
    matricula = 300
    mensualidad = 550
elif facultad == 3:
    matricula = 300
    mensualidad = 500
elif facultad == 4:
    matricula = 310
    mensualidad = 460
elif facultad == 5:
    matricula = 280
    mensualidad = 490
elif facultad == 6:
    matricula = 360
    mensualidad = 520
    
igv = (matricula + mensualidad) * 0.18
print(f"Su importe de matricula es {matricula}€, su mensualidad es de {mensualidad}€ y su IGV es de {igv}")