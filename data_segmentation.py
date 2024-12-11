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
    print("Se ejecuto correctamente: data_model2")
    print("-------------------------------------------------------------------------------\n")

    return train_data,test_data
