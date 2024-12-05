'''
Se genera un archivo con todas los paquetes-librerias y modulos que seran usados
'''

# ---------------------------
# --- Paquetes necesarios ---
# ---------------------------

# Búsqueda y manipulación de archivos
import glob  # Permite buscar archivos que coincidan con un patrón específico
import os  # Interacción con el sistema operativo (rutas, directorios, etc.)
from io import StringIO  # Manipulación de cadenas como archivos
import contextlib  # Manejo avanzado de contextos (redirección de salidas, etc.)
import re  # Operaciones con expresiones regulares (búsqueda y manipulación de patrones)

# Operaciones numéricas y arreglos
import numpy as np  # Realiza cálculos numéricos y manejo de arreglos
from itertools import product # genera todas las combinaciones posibles de parámetros a partir de los rangos proporcionados
import itertools

# Manipulación y análisis de datos
import pandas as pd  # Trabaja con estructuras de datos como DataFrames y series
import  random

# Manejo de fechas y horas
from datetime import datetime, timedelta  # Manipulación de fechas y cálculos temporales

# Visualización de datos
import matplotlib.pyplot as plt  # Visualización básica de gráficos (líneas, barras, etc.)
import seaborn as sns  # Visualización avanzada y estadística (mejora los gráficos de Matplotlib)

# Análisis estadístico y series temporales
from statsmodels.tsa.stattools import adfuller  # Prueba de estacionariedad para series temporales
import statsmodels.api as sm  # Modelos estadísticos avanzados (regresión, ANOVA, etc.)
from statsmodels.tsa.statespace.sarimax import SARIMAX  # Modelado SARIMAX (ARIMA con estacionalidad)
from statsmodels.tsa.stattools import kpss  # Prueba de estacionariedad KPSS
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf  # Gráficos de autocorrelación y PACF
from statsmodels.tsa.seasonal import seasonal_decompose  # Descomposición de series temporales

# Machine Learning (regresión y predicción)
from sklearn.linear_model import LinearRegression  # Modelos de regresión lineal
from sklearn.metrics import mean_absolute_error #para calcular el error absoluto medio (MAE) entre predicciones y valores reales
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import mean_squared_error
# Modelado avanzado con ARIMA (pmdarima)
import pmdarima  # Herramientas avanzadas para modelos ARIMA
from pmdarima import ARIMA  # Modelado ARIMA
from pmdarima import auto_arima 
import warnings # Selección automática de parámetros para ARIMA

# Skforecast (modelos SARIMAX y backtesting)
import skforecast  # Biblioteca para series temporales con modelos SARIMAX
from skforecast.datasets import fetch_dataset  # Carga de conjuntos de datos de ejemplo
from skforecast.plot import set_dark_theme  # Personalización de gráficos para series temporales
from skforecast.sarimax import Sarimax  # Modelos SARIMAX optimizados
from skforecast.recursive import ForecasterSarimax  # Predicción recursiva con SARIMAX
from skforecast.model_selection import TimeSeriesFold  # Validación cruzada para series temporales
from skforecast.model_selection import backtesting_sarimax  # Backtesting para evaluar modelos SARIMAX
from skforecast.model_selection import grid_search_sarimax  # Búsqueda de hiperparámetros para SARIMAX



'''__all__ = [
    'glob', 'os', 'StringIO', 'contextlib', 're', 
    'np', 'pd', 'datetime', 'timedelta', 'plt', 'sns', 
    'adfuller', 'sm', 'SARIMAX', 'kpss', 'plot_acf', 'plot_pacf', 'seasonal_decompose',
    'LinearRegression', 'pmdarima', 'ARIMA', 'auto_arima', 
    'skforecast', 'fetch_dataset', 'set_dark_theme', 'Sarimax', 'ForecasterSarimax', 
    'TimeSeriesFold', 'backtesting_sarimax', 'grid_search_sarimax'
]'''