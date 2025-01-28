from packages import pd,np
def inverse_transform(original_serie,diff_serie_tendencia,diff_serie_estacionalidad,predictions):
    '''
    Reconvierte las predicciones preprocesadas a la escala original de la serie temporal.

    Args:
        original_serie (pd.Series): Serie original antes del preprocesamiento.
        diff_serie_tendencia (pd.DataFrame): Diferencias de tendencia con columnas "date" y "venta".
        diff_serie_estacionalidad (pd.DataFrame): Diferencias estacionales con columnas "date" y "venta".
        predictions (pd.DataFrame): Predicciones en escala diferenciada, con columnas "date" y "venta".

    Returns:
        pd.DataFrame: Serie temporal con columnas "date" y "venta" en la escala original.

    Pasos principales:
        1. Combina las diferencias de tendencia, estacionalidad y predicciones.
        2. Revierte las diferencias estacionales (desplazamiento de 12 pasos).
        3. Reintegra la tendencia acumulada, comenzando desde el primer valor original.
        4. Aplica la transformación exponencial para regresar de escala logarítmica.
    '''
    diff_serie_tendencia=diff_serie_tendencia[:12]
    from results import concat_series_df
    series_concats=concat_series_df(diff_serie_tendencia,diff_serie_estacionalidad,predictions)
    for i in range(len(series_concats)):
        if i >=12:
            series_concats.loc[i,"venta"] += series_concats.loc[ i-12,"venta"]
    
    # Calcular el primer valor de original_serie
    first_value = np.log(original_serie.iloc[0])
    # Crear el DataFrame con columnas "date" y "venta"
    df_first_value = pd.DataFrame({"date": [original_serie.index[0]], "venta": [first_value]})
    serie_tendencia_inversa=concat_series_df(df_first_value,series_concats)

    for i in range(len(serie_tendencia_inversa)):
        if i >=1:
            serie_tendencia_inversa.loc[i,"venta"] += serie_tendencia_inversa.loc[ i-1,"venta"]
    serie_exp=serie_tendencia_inversa
    if (serie_exp['venta'] > 0).all():
        serie_exp['venta'] = np.exp(serie_exp['venta'])

    return serie_exp