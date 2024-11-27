from packages import sm

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