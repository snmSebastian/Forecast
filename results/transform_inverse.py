from packages import pd,np
def inverse_transform(original_serie,diff_serie_tendencia,diff_serie_estacionalidad,predictions):
    diff_serie_tendencia=diff_serie_tendencia[:12]
    from results import concat,concat2
    series_concats=concat(diff_serie_tendencia,diff_serie_estacionalidad,predictions)
    for i in range(len(series_concats)):
        if i >=12:
            series_concats.loc[i,"venta"] += series_concats.loc[ i-12,"venta"]
    
    # Calcular el primer valor de original_serie
    first_value = np.log(original_serie.iloc[0])
    # Crear el DataFrame con columnas "date" y "venta"
    df_first_value = pd.DataFrame({"date": [original_serie.index[0]], "venta": [first_value]})
    serie_tendencia_inversa=concat2(df_first_value,series_concats)

    for i in range(len(serie_tendencia_inversa)):
        if i >=1:
            serie_tendencia_inversa.loc[i,"venta"] += serie_tendencia_inversa.loc[ i-1,"venta"]
    serie_exp=serie_tendencia_inversa
    if (serie_exp['venta'] > 0).all():
        serie_exp['venta'] = np.exp(serie_exp['venta'])

    return serie_exp