import matplotlib.pyplot as plt
import numpy as np
import csv

# Leer y cargar datos desde archivos CSV
def load_csv_to_array(file_path):
    # Abrir el archivo CSV y cargar sus datos en una matriz numpy
    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)
        headers = next(csv_reader)  # Ignorar la primera fila, generalmente contiene encabezados
        data = list(csv_reader)  # Convertir las filas a una lista
    return np.array(data)  # Convertir la lista a una matriz numpy para un fácil manejo

# Cargar datos desde archivos CSV
estaciones = load_csv_to_array('csv/2020_MeteoCat_Estacions.csv')
detalle_estaciones = load_csv_to_array('csv/2022_MeteoCat_Detall_Estacions.csv')
metadatos = load_csv_to_array('csv/MeteoCat_Metadades.csv')

# Calcular promedio de temperaturas por día y acrónimo
def calcular_promedio_temp(acronimo, estacion_id):
    # Crear un diccionario para almacenar temperaturas por día
    dias_temperaturas = {}
    for fila in detalle_estaciones:
        fecha, cod_estacion, acronimo_estacion, valor = fila[0], fila[2], fila[3], float(fila[4])
        dia = int(fecha.split("-")[2])  # Obtener el día del mes
        mes = fecha.split("-")[1]  # Obtener el mes
        
        # Solo considerar datos de febrero y de la estación específica
        if mes == "02" and acronimo_estacion.upper() == acronimo.upper() and (
            estacion_id == "TOTS" or cod_estacion == estacion_id
        ):
            # Si el día aún no está en el diccionario, agregarlo
            if dia not in dias_temperaturas:
                dias_temperaturas[dia] = []
            dias_temperaturas[dia].append(valor)  # Agregar temperatura al día correspondiente

    # Calcular el promedio de temperaturas por día
    promedios = [(dia, sum(valores) / len(valores)) for dia, valores in dias_temperaturas.items()]
    return promedios  # Devolver la lista de promedios de temperatura por día

# Graficar la temperatura media de febrero de 2022
def graficar_temp_media_febrero():
    # Obtener promedios de temperatura para todas las estaciones
    temp_todas_estaciones = np.array(calcular_promedio_temp("TM", "TOTS"))

    # IDs de estaciones y sus colores correspondientes
    estaciones_ids = ["D5", "X4", "X8", "X2"]
    colores = ["purple", "cyan", "brown", "pink"]  # Nuevos colores

    # Gráfica de temperaturas medias en todas las estaciones
    plt.plot(temp_todas_estaciones[:, 0], temp_todas_estaciones[:, 1], 'o-', color='black', label='Todas las estaciones')
    plt.title("Temperatura media en febrero 2022")  # Título del gráfico
    plt.xlabel("Días")  # Etiqueta del eje x
    plt.xticks(range(1, 29))  # Configurar el rango de días
    plt.ylabel("Temperatura (°C)")  # Etiqueta del eje y
    plt.grid(True)  # Mostrar cuadrícula
    plt.legend()  # Mostrar leyenda
    plt.show()  # Mostrar el gráfico

    # Gráfica de temperatura por cada estación individual
    for idx, estacion in enumerate(estaciones_ids):
        temp_estacion = np.array(calcular_promedio_temp("TM", estacion))
        plt.plot(temp_estacion[:, 0], temp_estacion[:, 1], 'o-', color=colores[idx], label=f'Estación {estacion}')
    plt.title("Temperatura media por estación en febrero 2022")  # Título del gráfico
    plt.xlabel("Días")  # Etiqueta del eje x
    plt.xticks(range(1, 29))  # Configurar el rango de días
    plt.ylabel("Temperatura (°C)")  # Etiqueta del eje y
    plt.grid(True)  # Mostrar cuadrícula
    plt.legend()  # Mostrar leyenda
    plt.show()  # Mostrar el gráfico

    # Subgráficas por cada estación
    fig, axes = plt.subplots(4, 1, figsize=(10, 10), sharex=True, sharey=True)  # Configurar las subgráficas
    
    # Graficar temperatura por cada estación
    for idx, estacion in enumerate(estaciones_ids):
        temp_estacion = np.array(calcular_promedio_temp("TM", estacion))
        axes[idx].plot(temp_estacion[:, 0], temp_estacion[:, 1], 'o-', color=colores[idx])
        axes[idx].set_title(f'Estación {estacion}')  # Título de cada subgráfica
        axes[idx].set_xlabel("Días")  # Etiqueta del eje x
        axes[idx].set_ylabel("Temperatura Media (°C)")  # Etiqueta del eje y
        axes[idx].grid(True)  # Mostrar cuadrícula

    plt.tight_layout()  # Ajustar para evitar solapamientos
    plt.show()  # Mostrar el gráfico con subgráficas

# Graficar la distribución de temperaturas de febrero de 2022 y 2023
def graficar_distribucion_temp_febrero():
    # Obtener temperaturas de febrero de 2022
    temp_2022 = np.array(calcular_promedio_temp("TM", "TOTS"))[:, 1]

    # Graficar la distribución de temperaturas de 2022
    plt.hist(temp_2022, bins=range(8, 22), edgecolor='black', color="lightgreen")  # Nuevo color para 2022
    plt.xlabel('Temperatura (°C)')  # Etiqueta del eje x
    plt.ylabel('Frecuencia (Días)')  # Etiqueta del eje y
    plt.grid(True)  # Mostrar cuadrícula
    plt.title('Distribución de temperaturas de febrero de 2022')  # Título del gráfico
    plt.show()  # Mostrar el gráfico

    # Calcular la media y la desviación estándar de las temperaturas de 2022
    media_temp = np.mean(temp_2022)  # Media de las temperaturas de febrero de 2022
    desv_estandar = np.std(temp_2022)  # Desviación estándar

    # Generar temperaturas para febrero de 2023 con distribución normal
    temp_2023 = np.random.normal(media_temp, desv_estandar, 28)

    # Graficar la distribución de temperaturas de 2023
    plt.hist(temp_2023, bins=range(8, 22), edgecolor='black', color='lightblue')  # Color para 2023
    plt.xlabel('Temperatura (°C)')  # Etiqueta del eje x
    plt.ylabel('Frecuencia (Días)')  # Etiqueta del eje y
    plt.grid(True)  # Mostrar cuadrícula
    plt.title('Distribución de temperaturas de febrero de 2023')  # Título del gráfico
    plt.show()  # Mostrar el gráfico

# Graficar proporción de días de lluvia
def graficar_proporcion_lluvia_febrero():
    # Obtener precipitaciones de febrero de 2022
    precipitacion_2022 = np.array(calcular_promedio_temp("PPT", "TOTS"))

    # Contar la cantidad de días con y sin lluvia
    dias_con_lluvia = np.count_nonzero(precipitacion_2022[:, 1])  # Días con lluvia
    total_dias = len(precipitacion_2022)  # Total de días en febrero
    dias_sin_lluvia = total_dias - dias_con_lluvia  # Días sin lluvia
    
    # Gráfico de pie para la proporción de días de lluvia
    plt.pie([dias_con_lluvia, dias_sin_lluvia], labels=["Lluvia", "Sin Lluvia"], autopct='%1.1f%%', startangle=90, colors=["lightblue", "lightgray"])  # Nuevos colores
    plt.title("Proporción de días de lluvia en febrero 2022")  # Título del gráfico
    plt.axis('equal')  # Mantener proporción de círculo
    plt.show()  # Mostrar el gráfico

    # Gráfico de barras para las precipitaciones por día
    plt.barh(range(1, total_dias + 1), precipitacion_2022[:, 1], color="lightgreen")  # Color para las barras
    plt.xlabel("Precipitaciones")  # Etiqueta del eje x
    plt.ylabel("Días")  # Etiqueta del eje y
    plt.title("Precipitación por días en febrero 2022")  # Título del gráfico
    plt.show()  # Mostrar el gráfico

# Ejecución de las funciones de prueba
graficar_temp_media_febrero()
graficar_distribucion_temp_febrero()
graficar_proporcion_lluvia_febrero()
