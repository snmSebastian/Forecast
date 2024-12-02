# SBD-Forescast
Este repositorio contiene el codigo desarrollado para el modelo de prediccion de ventas

packages.py: Se genera un archivo con todas los paquetes-librerias y modulos que seran usados

data_loading.py: COntiene las funciones para cargar y procesar la informacion tanto de sharepoint como csv.

    historical_sales:  lectura del csv con la inf de venta historica:  este archivo csv es el resultado de unificar        todos  los xlsx de sharepoint,filtrando las columnas de interes para el modelo
    
    Arg: ruta con la ubicacion del archivo csv con la informacion historica de venta
    
    return: dataframe(df_SalesAndProduct) agrupando la venta mensual, organizada por data,country y brand
            y filtrando los valores positivos para realizar un pronostico de venta bruta

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



time_series_processing.py: Contiene 3 funciones: creacion de series, estacionarizacion series, metricas de series.

    def time_serie(df, filtros):Filtra los datos de ventas según los filtros especificados y devuelve una serie de tiempo.
    Args:
        df (pd.DataFrame): DataFrame con datos de ventas.
        filtros (dict): Diccionario de condiciones para filtrar.
    Returns:
        pd.Series: Serie de tiempo de ventas filtrada.


    def seasonalize_series(serie): Estacionariza la serie de entrada para eliminar tendencias mediante diferenciaciones sucesivas hasta que pase la prueba de ADF o se alcancen las restricciones definidas.

    Args:
        serie (pd.Series): Serie temporal a estacionarizar.
        max_diff (int): Máximo número de diferenciaciones permitidas (default=12).
        min_observations (int): Mínima cantidad de observaciones requeridas después de diferenciar (default=24).
        p_threshold (float): Umbral para el p-valor de la prueba ADF (default=0.05).

    Returns:
        pd.Series: Serie estacionaria con p-valor (ADF) < p_threshold, o la serie diferenciada al máximo permitido.
    
    def time_series_metrics(serie): Esta función realiza un análisis básico de una serie temporal, proporcionando métricas
    claves relacionadas con su descomposición y estacionariedad.

    Parámetros:
    - `serie` (pandas.Series): Serie temporal a analizar.

    Retorna:
    - `dict`: Diccionario con las métricas de descomposición y el p-valor de la prueba ADF.
    """

    def forecast_data(df_sales_and_product):
    """
    Prepara un DataFrame para almacenar resultados de pronósticos, 
    filtrando y agregando datos de ventas por país, categoría y mes.

    Args:
        df_sales_and_product (pd.DataFrame): DataFrame con datos de ventas.

    Returns:
        pd.DataFrame: DataFrame preparado con ventas agregadas por país, categoría y mes.
    """



data_segmentation.py: COntiene 2 funciones, segmentacion de datos de entrenamiento y validacion, eleccion 
    de datos de entrenamiento.

    def data_model(serie_sales):Segmenta una serie en conjuntos de entrenamiento, validación y prueba, y genera versiones estacionalizadas.

    Args: 
        serie (pd.Series): Serie temporal a segmentar.
    
    Returns:
        tuple: Conjuntos originales y estacionalizados (train, validation, test).
    
    def select_data: Selecciona entre datos originales y estacionalizados dependiendo del tamaño de la serie.

    Arg:serie_sales,serie,\
                 data_train_original, data_validation_original,\
                      data_train_estacionalizado, data_validation_estacionalizado
    Out: train_data, test_data

parameters_optimization.py
    def best_parameters_auto_arima(serie,
                              data_train_orginal, data_train_estacionalizado):
    
    Recibe una serie estacionarizada, realiza un proceso autoarima para obtener los mejores parametros para:p,d,q,P,D,Q,s
    Parámetros:
        serie (pd.Series): Serie estacionarizada 
        data_train_orginal, tomado de la serie sin estacionarizar
        data_train_estacionalizado tomado de la serie  estacionarizarada

    Retorna:
        tuple: Rangos para los parámetros p, d, q, P, D, Q y s.
    
    def generate_param_grid(p_range, d_range, q_range, P_range, D_range, Q_range, s_range):
        Genera todas las combinaciones posibles de hiperparámetros para el modelo SARIMAX.
    
    Parámetros:
    - p_range, d_range, q_range: Rango de los parámetros ARIMA (p, d, q).
    - P_range, D_range, Q_range: Rango de los parámetros estacionales (P, D, Q).
    - s_range: Rango del período estacional (s).
    
    Retorna:
    - param_grid: Lista de combinaciones de parámetros.

definition_trainig_model.py: Contiene la definicion de cada uno de los modelos que se entrenaran:
    Sarimax

definition_final_model.py: Contiene la definicion  de cada uno de los modelos finales que se entrenaron:
    Sarimax    


sarimax_model.py: COntiene dos funciones, encontrar los mejores parametros para hacer sarimax, y entrenar sarimax    con   esos parametros
    def sarimax_models(param_grid, data_train_orginal,data_test_orginal,data_test_estacionalizado,data_train_estacionalizado):

    Evalúa todos los modelos SARIMAX generados a partir de un param_grid y selecciona el mejor modelo según el MAE.
    
    Parámetros:
    - param_grid: Combinaciones de parámetros.
    - y_train: Datos de entrenamiento.
    - y_test: Datos de prueba.
    
    Retorna:
    - best_params: Los mejores parámetros encontrados.
    - best_mae: El MAE más bajo obtenido.
  
    generate_sarimax_by_category: 
        Genera y evalúa modelos SARIMAX para cada categoría en la lista proporcionada.

    Esta función toma un DataFrame con información de ventas y, para cada categoría especificada:
    - Filtra los datos de ventas.
    - Estacionariza la serie temporal.
    - Segmenta los datos en conjuntos de entrenamiento, validación y prueba.
    - Optimiza los hiperparámetros para un modelo SARIMAX.
    - Evalúa los modelos generados y selecciona el mejor.
    - Ajusta el modelo final y calcula el MAE.

    Args:
        df_sales_and_product (pd.DataFrame): DataFrame con datos de ventas.
        lst_category (list): Lista de categorías para las cuales se evaluarán y ajustarán modelos SARIMAX.

    Returns:
        None: La función imprime los resultados del modelo para cada categoría. 
        Los resultados incluyen el mejor modelo y el MAE asociado.

    Notas:
        - La función supone que las columnas necesarias (`Category Group`, `Date`, `Total Sales`, etc.) están presentes en `df_sales_and_product`.
        - Los modelos se ajustan para series estacionalizadas.
        - Requiere que las funciones auxiliares (time_serie, seasonalize_series, etc.) estén correctamente implementadas.
    
caegory_model_pipeline.py:
    '''Recibe informacion de ventas, y filtros de categorias, y evalua para cada categoria un modelo sarimax
    con los mejores parametros
    Arg: df_sales_and_product( dataframe de ventas)
        lst_category:lista de las categorias a las cuales se les realizara pronostico
    Out: dataframe con 12 registros mas correspondientes al pronostico
        columnas( sales, )
    '''

file_prueba.py
    def csv_prueba(ruta_csv,lst_category):
        Crea un csv filtrando por los elementos de Category Group
    Arg: ruta_csv: ruta del archivo CSV principal que contiene los datos históricos
         lst_category: lista con las categorías que se desean filtrar en los datos.
    Out: df_prueba: csv con la data filtrada
   


























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