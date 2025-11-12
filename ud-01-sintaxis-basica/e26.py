# Cálculo del salario neto semanal

# Entrada de datos
salarioHora = float(input("Introduzca el salario por hora (€): "))
horasTrabajadas = float(input("Introduzca el número total de horas trabajadas: "))

# Cálculo del salario bruto
if horasTrabajadas <= 35:
    salarioBruto = salarioHora * horasTrabajadas
else:
    horasExtra = horasTrabajadas - 35
    salarioBruto = (35 * salarioHora) + (horasExtra * salarioHora * 1.5)

# Cálculo del salario neto según tramos impositivos
if salarioBruto <= 500:
    salarioNeto = salarioBruto
elif salarioBruto <= 900:
    salarioNeto = 500 + (salarioBruto - 500) * (1 - 0.25)
else:
    salarioNeto = 500 + 400 * (1 - 0.25) + (salarioBruto - 900) * (1 - 0.45)

# Resultado final
print(f"\nSalario bruto semanal: {salarioBruto:.2f} €")
print(f"Salario neto semanal: {salarioNeto:.2f} €")
