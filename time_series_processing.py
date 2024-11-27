''' 
Se genera la serie y se estacionariza mediante la prueba dicker
'''

from packages import adfuller  # Prueba de estacionariedad para series temporales
from packages import np
#---------------------------------------
#---- Creacion series de tiempo
#---------------------------------------

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

    return serie, series_sales

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
    min_observations= len(serie)-24
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
        print(f'se diferencia la serie por {diff_order} vez')