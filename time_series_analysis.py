#======================
#--- Paquetes
#======================

from packages import adfuller  # Prueba de estacionariedad para series temporales
from packages import np
from packages import sm


#==============================================
#---- Creacion series de tiempo
#==============================================

def time_serie(df, filtros):
    """
    Filtra los datos de ventas según los filtros especificados y devuelve una serie de tiempo.
    Args:
        df (pd.DataFrame): DataFrame con datos de ventas.
        filtros (dict): Diccionario de condiciones para filtrar.
    Returns:
        pd.Series: Serie de tiempo de ventas filtrada.
    """
    for clave, valor in filtros.items():
        df = df[df[clave] == valor]
        
    df = df.groupby(df['Date'].dt.to_period('M'))['Total Sales'].sum().reset_index()
    df['Date'] = df['Date'].dt.to_timestamp()
    serie = df.set_index('Date')['Total Sales']
    serie = serie.asfreq('MS')
    series_sales=serie.copy()
    print("Se ejecuto correctamente: time_serie")
    print("-------------------------------------------------------------------------------\n")

    return  series_sales,serie

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
    serie_copy=serie.copy()
    len_serie=len(serie_copy)
    diff_order = 0  # Contador de diferenciaciones
    min_observations= len(serie)-48
    max_diff= len(serie)-12
    p_threshold=0.05
    p_value = adfuller(serie)[1]
    print(f"{'La serie de ventas pasó la prueba de Dickey-Fuller y es estacionaria.' if p_value < p_threshold else 'La serie de ventas no pasó la prueba de Dickey-Fuller y no es estacionaria.'}")
    
    while diff_order < max_diff and len(serie) >= min_observations:
        print("1")
        # Prueba de Dickey-Fuller aumentada
        p_value = adfuller(serie)[1]
        if p_value <= p_threshold:
            print("la serie es estacionaria")
            if len(serie)<len_serie:         
                    #print("se devuelve la serie estacionalizada")
                    # Devuelve la serie diferenciada o en su mejor estado
                    #print(f'serie inicial:{len(serie_copy)}\n')
                    #print(f'serie final:{len(serie)}\n')
                    print("Se ejecuto correctamente: seasonalize_serie")
                    #print(f"Máximo de diferenciaciones alcanzado: {diff_order}")
                    print("-------------------------------------------------------------------------------\n")
            else:                    
                    print("Se ejecuto correctamente: seasonalize_serie")
                    print("se devuelve la serie original")
                    print("-------------------------------------------------------------------------------\n")
            return serie
        
        # Aplicar diferenciación
        serie = serie.diff().dropna()
        diff_order += 1
        #print(f'se diferencia la serie por {diff_order} vez')


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


