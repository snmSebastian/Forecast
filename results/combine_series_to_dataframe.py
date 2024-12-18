from packages import pd
def concat(*args):
    """
    Combina múltiples series y/o DataFrames en un único DataFrame, con las columnas 'date' y 'venta'.
    
    Parámetros:
    *args: Series o DataFrames donde el índice (para series) o la columna 'date' (para DataFrames) es de tipo fecha.
    
    Retorna:
    pd.DataFrame: DataFrame con las columnas 'date' y 'venta', que combina los datos de todas las entradas.
    """
    # Lista para almacenar DataFrames individuales
    dataframes = []
    
    for obj in args:
        if isinstance(obj, pd.Series):  # Si es una serie
            df = obj.reset_index()  # Convierte la serie a DataFrame
            df.columns = ['date', 'venta']  # Renombra las columnas
        elif isinstance(obj, pd.DataFrame):  # Si es un DataFrame
            # Asegúrate de que tenga las columnas requeridas
            if 'date' in obj.columns and 'venta' in obj.columns:
                df = obj[['date', 'venta']]
            else:
                raise ValueError("Los DataFrames deben tener columnas 'date' y 'venta'")
        else:
            raise TypeError("Solo se aceptan objetos de tipo pd.Series o pd.DataFrame")
        
        dataframes.append(df)
        
    # Concatenar todos los DataFrames
    series_concats = pd.concat(dataframes, ignore_index=True)
    series_concats['date']=pd.to_datetime(series_concats['date'],format='%Y-%m-%d')
    series_concats=series_concats.sort_values(by='date').reset_index(drop=True)
    return series_concats

def concat2(*args):
    """
    Combina múltiples series y/o DataFrames en un único DataFrame, con las columnas 'date' y 'venta'.
    
    Parámetros:
    *args: Series o DataFrames donde el índice (para series) o la columna 'date' (para DataFrames) es de tipo fecha.
    
    Retorna:
    pd.DataFrame: DataFrame con las columnas 'date' y 'venta', que combina los datos de todas las entradas.
    """
    # Lista para almacenar DataFrames individuales
    dataframes = []
    
    for obj in args:
        if isinstance(obj, pd.Series):
            if not isinstance(obj.index, pd.DatetimeIndex):
                raise ValueError("El índice de la serie debe ser de tipo pd.DatetimeIndex")
            
            # Convertir la serie a DataFrame
            df = obj.reset_index()  # Convierte el índice en columna
            df.columns = ['date', 'venta']  # Renombrar las columnas adecuadamente
            
        elif isinstance(obj, pd.DataFrame):
            if 'date' not in obj.columns or 'venta' not in obj.columns:
                raise ValueError("Los DataFrames deben tener columnas 'date' y 'venta'")
            
            # Filtrar las columnas necesarias
            df = obj[['date', 'venta']]
            
            if not pd.api.types.is_datetime64_any_dtype(df['date']):
                raise ValueError("La columna 'date' debe ser de tipo fecha")
        else:
            raise TypeError("Solo se aceptan objetos de tipo pd.Series o pd.DataFrame")
        
        # Agregar el DataFrame procesado a la lista
        dataframes.append(df)
    
    # Concatenar todos los DataFrames
    result = pd.concat(dataframes, ignore_index=True)
    
    # Asegurar que la columna 'date' sea de tipo datetime
    result['date'] = pd.to_datetime(result['date'], format='%Y-%m-%d', errors='coerce')
    
    # Verificar si hay valores NaT después de convertir a datetime
    if result['date'].isna().any():
        raise ValueError("Se encontraron valores no válidos en la columna 'date' después de la conversión")
    
    # Ordenar por la columna 'date' y reiniciar el índice
    result = result.sort_values(by='date').reset_index(drop=True)
    
    return result