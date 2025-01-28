from packages import pd
def concat_series_df(*args):

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

def concat_result(predictions,df_sales_predictions,best_results_backtesting,country,category):
    predictions=predictions[-12:].copy()
    predictions['country']=country
    predictions['category group']=category
    predictions['model']='sarimax'
    predictions['mape']=best_results_backtesting['mape']
    predictions=predictions[['country','category group','date','venta','model','mape']]
    df_sales_predictions = pd.concat([predictions, df_sales_predictions], axis=0)
    df_sales_predictions['date'] = pd.to_datetime(df_sales_predictions['date'])
    df_sales_predictions=df_sales_predictions.sort_values(by=['country','category group','date'])
    return df_sales_predictions



def concat_result_country(predictions,df_sales_predictions,best_results_backtesting,country):
    predictions=predictions[-12:].copy()
    predictions['country']=country
    predictions['model']='sarimax'
    predictions['mape']=best_results_backtesting['mape']
    predictions=predictions[['country','date','venta','model','mape']]
    df_sales_predictions = pd.concat([predictions, df_sales_predictions], axis=0)
    df_sales_predictions['date'] = pd.to_datetime(df_sales_predictions['date'])
    df_sales_predictions=df_sales_predictions.sort_values(by=['country','date'])
    return df_sales_predictions




def concat_result_country_basico(predictions,df_sales_predictions,country):
    predictions=predictions[-12:].copy()
    predictions['country']=country
    predictions['model']='sarimax'
    predictions=predictions[['country','date','venta','model']]
    df_sales_predictions = pd.concat([predictions, df_sales_predictions], axis=0)
    df_sales_predictions['date'] = pd.to_datetime(df_sales_predictions['date'])
    df_sales_predictions=df_sales_predictions.sort_values(by=['country','date'])
    return df_sales_predictions