try:
    # Solicita la hora en formato "HH:MM:SS"
    horaMinutosSegundos = str(input("Introduzca la hora, separando con el caracter ':' (Ej: 14:30:59): "))

    # 1. Separar horas, minutos y segundos
    # Se divide la cadena usando el ':' como separador
    partes = horaMinutosSegundos.split(':')

    # Verificar que hay exactamente 3 partes
    if len(partes) != 3:
        print("Error: El formato de entrada no es 'HH:MM:SS'. Asegúrese de usar dos puntos (:) como separador.")
    else:
        # Convertir las partes a enteros
        # La conversión a int puede fallar si las partes no son números, se maneja en el 'except'
        horas = int(partes[0])
        minutos = int(partes[1])
        segundos = int(partes[2])

        # 2. Validar el rango de las horas, minutos y segundos
        if not (0 <= horas < 24 and 0 <= minutos < 60 and 0 <= segundos < 60):
            print("Error: Los valores de hora, minutos o segundos están fuera de rango.")
        else:
            # --- Lógica de cálculo transcurrido un segundo ---

            # 3. Sumar un segundo
            segundos_futuro = segundos + 1
            minutos_futuro = minutos
            horas_futuro = horas

            # 4. Manejar desbordamientos (segundos)
            if segundos_futuro == 60:
                segundos_futuro = 0
                minutos_futuro += 1

                # 5. Manejar desbordamientos (minutos)
                if minutos_futuro == 60:
                    minutos_futuro = 0
                    horas_futuro += 1

                    # 6. Manejar desbordamientos (horas - ciclo de 24h)
                    if horas_futuro == 24:
                        horas_futuro = 0

            # 7. Escribir el resultado
            print("-" * 30)
            print(f"Hora actual: {horaMinutosSegundos}")
            # Se usa el formato '02d' para asegurar que el número tenga al menos 2 dígitos (ej: 09 en lugar de 9)
            print(f"Transcurrido un segundo, la hora será: {horas_futuro:02d}:{minutos_futuro:02d}:{segundos_futuro:02d}")
            print("-" * 30)

except ValueError:
    # Captura errores de conversión si la entrada contiene caracteres no numéricos
    print("Ha ocurrido un error en la conversión. Asegúrese de que los valores de hora, minutos y segundos son números.")
except Exception as e:
    # Captura cualquier otro error inesperado
    print(f"Ha ocurrido un error inesperado: {e}")