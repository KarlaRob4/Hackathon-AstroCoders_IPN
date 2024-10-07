import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt, spectrogram
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

import joblib

catalogDirectory = 'F:/Hackaton Ibero/space_apps_2024_seismic_detection/space_apps_2024_seismic_detection/data/lunar/training/catalogs/'
dataDirectory = 'F:/Hackaton Ibero/space_apps_2024_seismic_detection/space_apps_2024_seismic_detection/data/lunar/training/data/S12_GradeA/'
catalogFile = catalogDirectory + 'apollo12_catalog_GradeA_final.csv'
catalog = pd.read_csv(catalogFile)

#filenames = ['xa.s12.00.mhz.1970-01-19HR00_evid00002']

def getFrequencies(points):
    # Calcular el espectrograma
    frecuencias, tiempos, Sxx = spectrogram(points, fs=1000)

    # Obtener las frecuencias más significativas en cada instante
    # Encuentra el índice de la frecuencia máxima en cada columna de Sxx
    indices_max = np.argmax(Sxx, axis=0)

    # Usar los índices para obtener las frecuencias correspondientes
    frecuencias_significativas = frecuencias[indices_max]
    return frecuencias_significativas

def isSismicFrequency(frecuencias, arrivalIndex, points):
    isSismic = np.zeros(len(frecuencias))

    # Determinar el rango de índices que se llenarán con 1
    finalIndex = min(int(len(frecuencias)*(arrivalIndex-100) / len(points)) + 400, len(frecuencias))

    # Llenar los elementos desde arrivalIndex hasta finalIndex-1 con 1
    isSismic[int(len(frecuencias)*(arrivalIndex-100) / len(points)):finalIndex] = 1
    
    return isSismic

X = np.array([])
y = np.array([])

for _, row in catalog.iterrows():
    dataFilename = row.filename
    if dataFilename == 'xa.s12.00.mhz.1971-04-13HR00_evid00029': continue
    #if dataFilename in filenames:
    arrivalTime = row['time_rel(sec)']
    data = pd.read_csv(f'{dataDirectory}{dataFilename}.csv')
    points = data['velocity(m/s)'].values
    time = data['time_rel(sec)'].values
    arrivalIndex = np.argmin(np.abs(time - arrivalTime))

    frecuencias = getFrequencies(points)
    etiquetas = isSismicFrequency(frecuencias, arrivalIndex, points)

    X = np.concatenate((X, frecuencias))
    y = np.concatenate((y, etiquetas))

data = pd.DataFrame({'frequency': X, 'label': y})
X = data[['frequency']]  # Características
y = data['label']        # Etiquetas
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier(n_estimators=100, random_state=42)

print(X)
print(y)
print(X.shape)
print(y.shape)

# Entrenar el modelo
model.fit(X_train, y_train)
# Hacer predicciones
y_pred = model.predict(X_test)

# Calcular la precisión
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy * 100:.2f}%")

# Reporte de clasificación
#print(classification_report(y_test, y_pred))

# Guardar el modelo
joblib.dump(model, 'model.joblib')