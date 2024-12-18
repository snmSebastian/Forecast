#======================
#--- Paquetes
#======================
from packages import np


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