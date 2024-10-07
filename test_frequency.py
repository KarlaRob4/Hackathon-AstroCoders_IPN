from joblib import load
import pandas as pd
import numpy as np
from scipy.signal import butter, filtfilt, spectrogram
import matplotlib.pyplot as plt
import sys

filename = sys.argv[1]
#filename = str(sys.argv[1])
# Cargar el modelo entrenado
model = load('model.joblib')

def getFrequencies(points):
    frecuencias, tiempos, Sxx = spectrogram(points, fs=1000)

    # Obtener las frecuencias más significativas en cada instante
    # Encuentra el índice de la frecuencia máxima en cada columna de Sxx
    indices_max = np.argmax(Sxx, axis=0)

    # Usar los índices para obtener las frecuencias correspondientes
    frecuencias_significativas = frecuencias[indices_max]
    return frecuencias_significativas

X = np.array([])
# Prediccion
dataDirectory = f'D:/Hackaton Ibero/space_apps_2024_seismic_detection/space_apps_2024_seismic_detection/data/lunar/test/data/{filename}.csv'
data = pd.read_csv(dataDirectory)
points = data['velocity(m/s)'].values
time = data['time_rel(sec)'].values

frecuencias = getFrequencies(points)

X = np.concatenate((X, frecuencias))
data = pd.DataFrame({'frequency': X})
X = data[['frequency']]

predictions = model.predict(X)

# Encontrar el índice del primer 1
arrivalIndex = np.where(predictions > 0.0)[0]

if len(arrivalIndex > 0): promedio =  int(np.median(arrivalIndex))
else: promedio = 0

# Graficar la señal original
plt.figure(figsize=(12, 6))
plt.plot(points, label='Señal')

for i in range(len(arrivalIndex)):
    if arrivalIndex[i] > 0:
        arrivalTime = time[int(len(points)*arrivalIndex[i] / len(frecuencias))]
        line_index = (np.abs(time - arrivalTime)).argmin() 
        # Dibujar la línea vertical en el índice especificado
        plt.axvline(x=line_index, color='black', linestyle='--')

arrivalTimePromedio = time[int(len(points)*promedio / len(frecuencias))]
line_indexPromedio = (np.abs(time - arrivalTimePromedio)).argmin()
plt.axvline(x=line_indexPromedio, color='r', linestyle='-')


# Añadir leyendas y etiquetas
plt.title('Señal Original con Línea en Índice Específico')
plt.xlabel('Tiempo (índices)')
plt.ylabel('Amplitud')
plt.legend()

plt.savefig('graph.jpg')

# Mostrar la gráfica
plt.tight_layout()
plt.show()
