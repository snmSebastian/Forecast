#======================
#--- Paquetes
#======================
from packages import np,seasonal_decompose,pd


#==============================================
#---- Creacion series de tiempo
#==============================================
#--- Country-Category Group
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
            (df['country'] == filtros['country']) & 
            (df['category group'].isin(filtros['category group']))
        ]

        # Crear un diccionario para almacenar las series de tiempo
        series_dict={}
        series_sales_dict={}
        # Agrupar por categoría y generar la serie de tiempo por cada categoría
        for category in filtros['category group']:
            df_categoria = df_filtrado[df_filtrado['category group'] == category]
        
            if not df_categoria.empty:
                df_grouped = df_categoria
            
                # Crear la serie de tiempo
                serie = df_grouped.set_index('date')['venta']
                serie = serie.asfreq('MS')  # Frecuencia mensual
                # Verificar y rellenar NaN solo si es necesario
                if serie.isna().any():
                    serie = serie.interpolate(method='linear')  # Interpolación lineal
              # Guardar la serie en el diccionario
                series_dict[category] = serie
        series_sales_dict=series_dict.copy()    
        print("Se ejecutó correctamente: time_serie")
        print("-------------------------------------------------------------------------------\n")
        return series_sales_dict,series_dict
    except Exception as e:
        print(f"Error en la generación de series de tiempo: {e}")

#--- Country

def time_serie_country(df, filtros_country):
    
    
    """
    Genera series de tiempo por país 

    Args:
        df (pd.DataFrame): DataFrame con los datos de ventas.
        filters (dict): Filtros para seleccionar país. 
                        

    Returns:
        dict: Diccionario con series de tiempo para cada country.
        dict: Diccionario con datos originales sin preprocesar por country.
    """


    try:
        # Filtrar el DataFrame según el país y las categorías proporcionadas
        df_filtrado = df[
            (df['country'].isin(filtros_country)) 
        ]

        # Crear un diccionario para almacenar las series de tiempo
        series_dict={}
        series_sales_dict={}
        # Agrupar por categoría y generar la serie de tiempo por cada categoría
        for country in filtros_country:
            df_country = df_filtrado[df_filtrado['country'] == country]
        
            if not df_country.empty:
                df_grouped = df_country
            
                # Crear la serie de tiempo
                serie = df_grouped.set_index('date')['venta']
                serie = serie.asfreq('MS')  # Frecuencia mensual
                # Verificar y rellenar NaN solo si es necesario
                if serie.isna().any():
                    serie = serie.interpolate(method='linear')  # Interpolación lineal
              # Guardar la serie en el diccionario
                series_dict[country] = serie
        series_sales_dict=series_dict.copy()    
        print("Se ejecutó correctamente: time_serie")
        print("-------------------------------------------------------------------------------\n")
        return series_sales_dict,series_dict
    except Exception as e:
        print(f"Error en la generación de series de tiempo: {e}")


#==============================
#--- Preproccesing
#==============================


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
        diff_serie_tendencia = serie.diff().dropna()

        # Diferencias estacionales para eliminar estacionalidad
        diff_serie_estacionalidad = diff_serie_tendencia.diff(12).dropna()
        transfor_serie=diff_serie_estacionalidad

        #print("Se ejecutó correctamente: preprocess_series")
        #print("-------------------------------------------------------------------------------\n")
        return transfor_serie,diff_serie_tendencia,diff_serie_estacionalidad
    except Exception as e:
        #print(f"Error en el preprocesamiento de la serie: {e}")
        return None,None,None