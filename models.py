from packages import mean_absolute_error
from packages import SARIMAX
from packages import plt
def model_sarima(serie_sales,serie,
                 best_params,
                 data_train_original,data_validation_original,
                    data_train_estacionalizado,data_validation_estacionalizado):

    """
    Ajusta y evalúa un modelo SARIMAX con parámetros específicos para la serie temporal, 
    calculando el error medio absoluto (MAE) de las predicciones.

    Parámetros:
    - serie: Serie temporal a analizar, que puede ser original o estacionalizada.
    - data_train_orginal: Conjunto de datos de entrenamiento basado en la serie original.
    - data_train_estacionalizado: Conjunto de datos de entrenamiento basado en la serie estacionalizada.

    Retorna:
    - None: Imprime el MAE del modelo ajustado.
    """
    #Identifica si se esta trabajando con la serie original o la estacionarizada, con base en esto elige el conjunto train
    #con el cual entrenar el modelo autorima

    if len(serie)<len(serie_sales):
        print("se trabajo con serie estacionalizada")
        #num_reg=int(len(serie_sales)*0.7)
        #train_data=serie_sales[:num_reg]
        #test_data=serie_sales[num_reg:]
        train_data=data_train_estacionalizado
        test_data=data_validation_estacionalizado
    else:
        print("se trabajo con serie orginal")
        #num_reg=int(len(serie)*0.7)
        #train_data=serie[:num_reg]
        #test_data=serie[num_reg:]
        train_data=data_train_original
        test_data=data_validation_original



    test_start = len(train_data)
    test_end = test_start + len(test_data) - 1

    p, d, q,P, D, Q, s=best_params
# Generar predicciones con un modelo específico
    try:
        model = SARIMAX(
        train_data,
        #order=(2, 0, 2),
        order=(p, d, q),
        seasonal_order=(P, D, Q, s),
        #seasonal_order=(0, 1, 0, 12),
        enforce_stationarity=False,
        enforce_invertibility=False,
        disp=0
        ).fit()


        predictions = model.predict(start=test_start, end=test_end)

    # Calcula métricas como MAE o MSE
        mae = mean_absolute_error(test_data, predictions)
        print(f"MAE del modelo:{best_params}: {mae}")
    except ValueError as e:
        print(f"Error en predicción: {e}")
    mae_percentage = (mae / test_data.mean()) * 100 

    print(f"El mae: {mae} representa un porcentaje de error del: {mae_percentage:.2f}%")
    print("Se ejecuto correctamente model_sarima")
    print("-------------------------------------------------------------------------------\n")
    plt.plot(test_data, label="Real")
    plt.plot(predictions, label="Predicciones")
    plt.legend()
    plt.show()