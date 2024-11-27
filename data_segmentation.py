
def data_model(serie_sales,serie):
    ''' 
    Segmenta una serie en conjuntos de entrenamiento, validación y prueba, y genera versiones estacionalizadas.

    Args: 
        serie (pd.Series): Serie temporal a segmentar.
    
    Returns:
        tuple: Conjuntos originales y estacionalizados (train, validation, test).
    '''
    num_reg_train_original=int(len(serie_sales)*0.7)
    num_reg_train_estacional=int(len(serie)*0.7)
   
    if num_reg_train_original == 0 or num_reg_train_estacional == 0:
        raise ValueError("No se puede generar el conjunto de entrenamiento con estas proporciones.")

    data_train_original=serie_sales[:num_reg_train_original]
    data_validation_original=serie_sales[num_reg_train_original:]

    data_train_estacionalizado=serie[:num_reg_train_estacional]
    data_validation_estacionalizado=serie[num_reg_train_estacional:]

    print(f'num reg serie {len(serie)}')
    print(f'num reg serie_sales {len(serie_sales)}')
    print("Se ejecuto correctamente: data_model")
    print("-------------------------------------------------------------------------------\n")

    return data_train_original, data_validation_original, data_train_estacionalizado,data_validation_estacionalizado
