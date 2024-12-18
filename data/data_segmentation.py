#======================================================
#--- Datos de entrenamiento y validacion
#======================================================
def data_model(serie):
    ''' 
    Segmenta una serie en conjuntos de entrenamiento, y test 
    Args: 
        serie (pd.Series): Serie temporal a segmentar.
    
    Returns:
        tuple: Conjuntos (train, test).
    '''
    #size_data_train=int(len(serie)*0.6)
    size_data_train=46
    train_data=serie[:size_data_train]
    test_data=serie[size_data_train:]
    print("Se ejecuto correctamente: data_model")
    print("-------------------------------------------------------------------------------\n")

    return train_data,test_data

#=======================================================
#--- Dataframe que contendra los resultados
#=======================================================

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
    print(df_sales_forecast.head())
    print("-------------------------------------------------------------------------------\n")

    return  df_sales_forecast

