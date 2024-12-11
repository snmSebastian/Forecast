#======================
#--- Paquetes
#======================

from packages import adfuller  # Prueba de estacionariedad para series temporales
from packages import sm,np


#==============================================
#---- Creacion series de tiempo
#==============================================

def time_serie(df, filtros):
    
    
    """
    Genera series de tiempo por categoría, filtradas por país y grupo de categorías.

    Args:
        df (pd.DataFrame): DataFrame con los datos de ventas.
        filters (dict): Filtros para seleccionar país y grupos de categorías. 
                        Ejemplo: {'Country': 'USA', 'Category Group': ['A', 'B']}

    Returns:
        dict: Diccionario con series de tiempo para cada categoría.
        dict: Diccionario con datos originales sin preprocesar por categoría.
    """


    try:
        # Filtrar el DataFrame según el país y las categorías proporcionadas
        df_filtrado = df[
            (df['Country'] == filtros['Country']) & 
            (df['Category Group'].isin(filtros['Category Group']))
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

def preprocess_series(serie):
    """
    Realiza un preprocesamiento básico para estacionarizar la serie.
    - Aplica diferencia regular y estacional si es necesario.
    - Transforma con logaritmo para estabilizar la varianza si la serie tiene valores positivos.

    Args:
        serie (pd.Series): Serie temporal original.

    Returns:
        pd.Series: Serie transformada.
    """
    try:
        # Logaritmo si la serie tiene valores positivos
        if (serie > 0).all():
            serie = np.log(serie)

        # Diferencias regulares para eliminar tendencia
        diff_serie = serie.diff().dropna()

        # Diferencias estacionales para eliminar estacionalidad
        diff_serie = diff_serie.diff(12).dropna()

        print("Se ejecutó correctamente: preprocess_series")
        print("-------------------------------------------------------------------------------\n")
        return diff_serie
    except Exception as e:
        print(f"Error en el preprocesamiento de la serie: {e}")
        return None