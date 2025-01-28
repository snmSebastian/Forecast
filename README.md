
# Proyecto: Predicción de Ventas con Modelos SARIMAX

Este proyecto tiene como objetivo predecir ventas utilizando modelos SARIMAX. Está organizado en módulos y carpetas para un flujo de trabajo limpio y eficiente, desde la carga de datos hasta la generación de resultados.

## Estructura del Proyecto

```
proyecto/
├── data/              # Procesamiento de datos
│   ├── __init__.py
│   ├── data_loading.py       # Carga de datos
│   └── data_segmentation.py  # Segmentación de datos
├── main_code/         # Lógica principal
│   ├── __init__.py
│   ├── lst_dictionary.py     # Diccionario de listas
│   └── main.py               # Punto de entrada del proyecto
├── models/            # Modelos predictivos
│   ├── __init__.py
│   └── model_sarimax/ # Modelos SARIMAX
│       ├── __init__.py
│       ├── parameter_generation.py  # Generación de parámetros
│       ├── prediction.py            # Predicciones
│       ├── sarimax.py               # Implementación de SARIMAX
│       └── model_training.py        # Entrenamiento del modelo
├── parameters/        # Optimización de hiperparámetros
│   ├── __init__.py
│   └── parameters_optimization.py
├── preprocessing/     # Preprocesamiento
│   ├── __init__.py
│   └── time_series_analysis.py
├── results/           # Resultados y transformaciones inversas
│   ├── __init__.py
│   ├── combine_series_to_dataframes.py
│   └── transform_inverse.py
├── requirements.txt   # Dependencias del proyecto
└── README.md          # Documentación principal
```

---
## Detalles de Carpetas

#### **data/**
- **`data_loading.py`**: 
  - Función `historical_sales_and_predicts`: Crea un DataFrame con el histórico de ventas y predicciones agrupado por `category group` y `country`.
  - Función `historical_sales_and_predicts_country`: Similar a la anterior, pero agrupa solo por `country`.

#### **main_code/**
- **`lst_dictionary.py`**: Contiene un diccionario donde las claves son países y los valores son listas de categorías.
- **`main.py`**: Ejecuta las funciones principales para generar los reportes.

#### **models/model_sarimax/**
- **`parameter_generation.py`**:
  - Función `generate_initial_param_grid`: Genera una rejilla inicial de parámetros para SARIMAX.
- **`prediction.py`**:
  - Función `fit_final_model_and_predict`: Ajusta el modelo y genera predicciones.
  - Función `fit_final_model_and_predict_basico`: Variante simplificada para predicciones básicas.
- **`sarimax.py`**:
  - Función `sarimax_model`: Implementa un pipeline completo para entrenar y validar un modelo SARIMAX.
  - Función `sarimax_model_basico`: Versión básica para generar pronósticos rápidos.
- **`model_training.py`**:
  - Función `perform_grid_search`: Realiza una búsqueda exhaustiva de hiperparámetros.
  - Función `get_best_sarimax_parameters`: Selecciona los mejores parámetros basados en MAE.
  - Función `run_backtesting`: Evalúa los modelos mediante backtesting.

#### **parameters/**
- **`parameters_optimization.py`**:
  - Función `best_parameters_auto_arima`: Obtiene los mejores parámetros iniciales utilizando AutoARIMA.
  - Función `generate_param_grid`: Genera combinaciones de parámetros para Grid Search.

#### **preprocessing/**
- **`time_series_analysis.py`**:
  - Función `time_serie`: Genera series temporales filtradas por país y grupo de categorías.
  - Función `preprocess_series`: Realiza preprocesamiento básico para estacionarizar las series.

#### **results/**
- **`combine_series_to_dataframes.py`**:
  - Función `concat_series_df`: Combina múltiples series o DataFrames en un único DataFrame.
- **`transform_inverse.py`**:
  - Función `inverse_transform`: Reconvierte las predicciones preprocesadas a la escala original.

---
## Uso


1. Ejecuta el archivo principal:
   ```bash
   python main_code/main.py
   ```
2. Personaliza los filtros en `time_series_analysis.py` para ajustar los análisis según tus necesidades.

## Creditos
# Sebastián Núñez Mejía
### Matemático con Maestría en Big Data y Ciencia de Datos

---

📞 **Celular**: [3144610417](tel:+57314461041)  
✉️ **Email**: [snmsebastian@gmail.com](mailto:snmsebastian@gmail.com)  
🐙 **GitHub**: [https://github.com/snmSebastian](https://github.com/snmSebastian)  


---

**Áreas de especialización:**
- **Análisis de Datos**  
- **Machine Learning y Modelado Predictivo**  
- **Optimización de Procesos ETL**  
- **Automatización y Visualización de Datos**  
- **Gestión de Bases de Datos**  
- **Optimización de Decisiones Estratégicas**