#======================
#--- Paquetes
#======================

from packages import adfuller  # Prueba de estacionariedad para series temporales
from packages import sm


#==============================================
#---- Creacion series de tiempo
#==============================================

def time_serie(df, filtros):
    
    
    """
    Filtra los datos de ventas según los filtros especificados y devuelve una serie de tiempo por categoría.
    
    Args:
        df (pd.DataFrame): DataFrame con datos de ventas.
        filtros (dict): Diccionario de condiciones para filtrar.
        
    Returns:
        dict: Diccionario con series de tiempo, una por cada valor de 'Category Group'.
    """


    try:
        # Filtrar el DataFrame según el país y las categorías proporcionadas
        df_filtrado = df[
            (df['Country'] == filtros['Country']) & 
            (df['Category Group'].isin(filtros['Category Group']))&
            (df['Total Sales']>0)
        ]

        # Crear un diccionario para almacenar las series de tiempo
        series_dict={}
        series_sales_dict={}
        # Agrupar por categoría y generar la serie de tiempo por cada categoría
        for category in filtros['Category Group']:
            df_categoria = df_filtrado[df_filtrado['Category Group'] == category]
        
            if not df_categoria.empty:
                # Agrupar las ventas por mes
                df_grouped = (
                    df_categoria
                    .groupby(df_categoria['Date'].dt.to_period('M'))['Total Sales']
                    .sum()
                    .reset_index()
                )
                df_grouped['Date'] = df_grouped['Date'].dt.to_timestamp()
            
                # Crear la serie de tiempo
                serie = df_grouped.set_index('Date')['Total Sales']
                serie = serie.asfreq('MS')  # Frecuencia mensual
            
                # Guardar la serie en el diccionario
                series_dict[category] = serie
        series_sales_dict=series_dict.copy()    
        print("Se ejecutó correctamente: time_serie")
        print("-------------------------------------------------------------------------------\n")
        return series_sales_dict,series_dict
    except Exception as e:
        print(f"Error en la generación de series de tiempo: {e}")
#==============================================
# --- Estacionarizacion series
#=============================================     
def seasonalize_series(serie):
    '''
    Estacionariza la serie de entrada para eliminar tendencias mediante diferenciaciones sucesivas 
    hasta que pase la prueba de ADF o se alcancen las restricciones definidas.

    Args:
        serie (pd.Series): Serie temporal a estacionarizar.
        max_diff (int): Máximo número de diferenciaciones permitidas (default=12).
        min_observations (int): Mínima cantidad de observaciones requeridas después de diferenciar (default=24).
        p_threshold (float): Umbral para el p-valor de la prueba ADF (default=0.05).

    Returns:
        pd.Series: Serie estacionaria con p-valor (ADF) < p_threshold, o la serie diferenciada al máximo permitido.
    ''' 
    diff_order = 0  # Contador de diferenciaciones
    min_observations= len(serie)-48
    max_diff= 12
    p_threshold=0.05
    p_value = adfuller(serie)[1]
    print(f"{'La serie de ventas pasó la prueba de Dickey-Fuller y es estacionaria.' if p_value < p_threshold else 'La serie de ventas no pasó la prueba de Dickey-Fuller y no es estacionaria.'}")
    
    while diff_order < max_diff and len(serie) >= min_observations:
        # Prueba de Dickey-Fuller aumentada
        p_value = adfuller(serie)[1]
        if p_value <= p_threshold:
            print(f'se estacionarizo la serie con {diff_order} diferenciaciones')
            return serie
        
        # Aplicar diferenciación
        serie = serie.diff().dropna()
        diff_order += 1
    # Si no pasa la prueba ADF, devuelve la serie diferenciada
    print("La serie no se estacionarizó completamente, pero se alcanzó el máximo permitido.")
    return serie
#====================================
#--- Data frame Agrupado por country - category group -date

def forecast_data(df_sales_and_product):
    """
    Prepara un DataFrame para almacenar resultados de pronósticos, 
    filtrando y agregando datos de ventas por país, categoría y mes.

    Args:
        df_sales_and_product (pd.DataFrame): DataFrame con datos de ventas.

    Returns:
        pd.DataFrame: DataFrame preparado con ventas agregadas por país, categoría y mes.
    """
        
    df_sales_forecast = df_sales_and_product.groupby([df_sales_and_product['Country'],
                                                         df_sales_and_product['Category Group'],
                                                         df_sales_and_product['Date'].dt.to_period('M'),
                                                         ])['Total Sales'].sum().reset_index()
    df_sales_forecast['Date'] = df_sales_forecast['Date'].dt.to_timestamp()
    df_sales_forecast['Modelo']='Historico'
    df_sales_forecast['mae']=0
    print("Se ejecuto correctamente: forecast data1")
    #print(df_sales_forecast.head())
    print("-------------------------------------------------------------------------------\n")

    return  df_sales_forecast


#==============================
#--- METRICS OF SERIES
#==============================

def time_series_metrics(serie):
    """

    Esta función realiza un análisis básico de una serie temporal, proporcionando métricas
    claves relacionadas con su descomposición y estacionariedad.

    1. **Descomposición Estacional**:
    - Utiliza el método de descomposición estacional aditiva para separar la serie
    en componentes de tendencia, estacionalidad y ruido.
    - Calcula las medias de cada componente (tendencia, estacionalidad, ruido) 
    para los modelos aditivos y multiplicativos.

    2. **Prueba de Estacionariedad**:
    Realiza la prueba de raíz unitaria ADF (Augmented Dickey-Fuller) sobre la serie
    original para evaluar si es estacionaria.
    - Devuelve el p-valor asociado a la prueba ADF.

    Notas:
    - Se asume que la periodicidad de la serie es 12 (por ejemplo, datos mensuales en un año).
    - La función imprime información sobre la estacionariedad de la serie.

    Parámetros:
    - `serie` (pandas.Series): Serie temporal a analizar.

    Retorna:
    - `dict`: Diccionario con las métricas de descomposición y el p-valor de la prueba ADF.
    """
    
    descomposicionAdd = sm.tsa.seasonal_decompose(serie, model='additive', period=12)
   # log_ventas = np.log(serie["Total Sales"])
    descomposicionMul = sm.tsa.seasonal_decompose(serie, model='additive', period=12)
    

    pvalue_serie_estacionarizada= "si paso la prueba ADF" if sm.tsa.adfuller(serie)[1] < 0.05 else "No paso la prueba ADF"
    print(f'la serie estacionaria {pvalue_serie_estacionarizada}')
    print("Se ejecuto correctamente time_series_metrics")
    return {
        "Mod Add tendencia": descomposicionAdd.trend.mean(),
        "Mod Add estacionalidad": descomposicionAdd.seasonal.mean(),
        "Mod Add ruido": descomposicionAdd.resid.mean(),
        "Mod Mul tendencia": descomposicionMul.trend.mean(),
        "Mod Mul estacionalidad": descomposicionMul.seasonal.mean(),
        "Mod Mul ruido": descomposicionMul.resid.mean(),
        
        "ADF Test": sm.tsa.adfuller(serie)[1], 
          # p-value
    }

