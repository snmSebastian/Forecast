# SBD-Forescast
Este repositorio contiene el codigo desarrollado para el modelo de prediccion de ventas

packages.py: Se genera un archivo con todas los paquetes-librerias y modulos que seran usados

sales_loader.py
    historical_sales:  lectura del csv con la inf de venta historica:  este archivo csv es el resultado de unificar        todos  los xlsx de sharepoint,filtrando las columnas de interes para el modelo
    
    Arg: ruta con la ubicacion del archivo csv con la informacion historica de venta
    
    return: dataframe(df_SalesAndProduct) agrupando la venta mensual, organizada por data,country y brand
            y filtrando los valores positivos para realizar un pronostico de venta bruta
    
sales_loader_sharepoint.py

    sales_sharepoint:Función para procesar los datos de ventas desde archivos XLSX alojados en SharePoint 
    y cruzarlos con datos maestros de productos.

    Pasos:
    1. Leer todos los archivos de ventas en la ruta especificada (`paht_data_historica`).
    2. Unificar los datos de ventas en un único DataFrame (`df_sales`).
    3. Leer el archivo maestro de productos desde la ruta especificada (`paht_data_product`).
    4. Seleccionar columnas clave de ventas y productos.
    5. Cruzar las ventas con los productos para agregar clasificaciones por SKU.
    6. Agregar una columna de fecha a partir del año fiscal y periodo fiscal.
    7. Retornar el DataFrame final procesado.

    Args:
    paht_data_historica (str): Ruta a la carpeta con archivos de ventas en formato XLSX.
    paht_data_product (str): Ruta al archivo maestro de productos en formato XLSX.

    Returns:
    pd.DataFrame: DataFrame combinado de ventas y productos

devoluciones.py
    def devolucion(df_sales_and_product,year): Analiza el porcentaje de registros que corresponden a devoluciones en un año específicoy en el conjunto completo de datos. Esto permite evaluar la factibilidad de imputar
    las devoluciones en las series temporales.

    Args:
        df_sales_and_product (pd.DataFrame): DataFrame con columnas 'Date' y 'Total Sales'.
        año (int): Año para analizar las devoluciones.

    Returns:
        None

time_series_processing.py
    def time_serie(df, filtros):Filtra los datos de ventas según los filtros especificados y devuelve una serie de tiempo.
    Args:
        df (pd.DataFrame): DataFrame con datos de ventas.
        filtros (dict): Diccionario de condiciones para filtrar.
    Returns:
        pd.Series: Serie de tiempo de ventas filtrada.
    
series_metrics.py
    def time_series_metrics(serie):
    """

    Esta función realiza un análisis básico de una serie temporal, proporcionando métricas
    claves relacionadas con su descomposición y estacionariedad.

    Parámetros:
    - `serie` (pandas.Series): Serie temporal a analizar.

    Retorna:
    - `dict`: Diccionario con las métricas de descomposición y el p-valor de la prueba ADF.
    """

series_graphs.py
    Funciones de visualización de series temporales:

    1. graph_box(serie): 
    Genera un boxplot para visualizar la distribución de una serie y detecta valores atípicos (outliers) 
    utilizando el rango intercuartílico (IQR). Imprime los outliers detectados.

    Arg: serie no estacionarizada

    2. graph_line(serie): 
    Divide la serie temporal (original y estacionalizada) en conjuntos de entrenamiento y prueba, 
    y grafica ambas divisiones para observar su comportamiento.

    Arg: serie no estacionarizada

    3. graph_tendence(serie_sales): 
    Ajusta modelos de regresión lineal para calcular y graficar la tendencia de la serie temporal 
    en su forma original y estacionalizada, mostrando las pendientes asociadas.

    Arg: serie no estacionarizada

data_segmentation.py
    def data_model(serie_sales):Segmenta una serie en conjuntos de entrenamiento, validación y prueba, y genera versiones estacionalizadas.

    Args: 
        serie (pd.Series): Serie temporal a segmentar.
    
    Returns:
        tuple: Conjuntos originales y estacionalizados (train, validation, test).
    '''

parameters_auto_arima.py
    def best_parameters_auto_arima(serie,
                              data_train_orginal, data_train_estacionalizado):
    
    
    Recibe una serie estacionarizada, realiza un proceso autoarima para obtener los mejores parametros para:p,d,q,P,D,Q,s
    con base en estos valores establece los rangos que seran usados en la optimizacion de hiperparametros por medio de 
    gridsearch

    Parámetros:
        serie (pd.Series): Serie estacionarizada 
        data_train_orginal, tomado de la serie sin estacionarizar
        data_train_estacionalizado tomado de la serie  estacionarizarada

    Retorna:
        tuple: Rangos para los parámetros p, d, q, P, D, Q y s.
    '''

param_grid_generator.py
    def generate_param_grid(p_range, d_range, q_range, P_range, D_range, Q_range, s_range):

    Genera todas las combinaciones posibles de hiperparámetros para el modelo SARIMAX.
    
    Parámetros:
    - p_range, d_range, q_range: Rango de los parámetros ARIMA (p, d, q).
    - P_range, D_range, Q_range: Rango de los parámetros estacionales (P, D, Q).
    - s_range: Rango del período estacional (s).
    
    Retorna:
    - param_grid: Lista de combinaciones de parámetros.

sarimax_model_selection.py
    def sarimax_models(param_grid, data_train_orginal,data_test_orginal,data_test_estacionalizado,data_train_estacionalizado):

    Evalúa todos los modelos SARIMAX generados a partir de un param_grid y selecciona el mejor modelo según el MAE.
    
    Parámetros:
    - param_grid: Combinaciones de parámetros.
    - y_train: Datos de entrenamiento.
    - y_test: Datos de prueba.
    
    Retorna:
    - best_params: Los mejores parámetros encontrados.
    - best_mae: El MAE más bajo obtenido.

