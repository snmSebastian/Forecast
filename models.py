from packages import mean_absolute_error
from packages import SARIMAX
from packages import plt
from packages import np
from data_segmentation import select_data
def model_sarima(best_params,
                 train_data,test_data):

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

    p, d, q,P, D, Q, s=best_params
# Generar predicciones con un modelo específico
    try:
        model = SARIMAX(
        train_data,
        order=(p, d, q),
        seasonal_order=(P, D, Q, s),
        enforce_stationarity=False,
        enforce_invertibility=False,
        disp=0
        ).fit()
        # Generar predicciones a futuro con forecast
       # forecast_steps = 12  # Predecir los próximos 12 meses
       # forecast = model.forecast(steps=forecast_steps)
       
        predictions = model.predict(start=len(train_data), end=len(train_data) + len(test_data) - 1)
    # Calcula métricas como MAE o MSE
        mae = mean_absolute_error(test_data, predictions)
        mae_percentage = (mae / test_data.mean()) * 100
        print(f"MAE del modelo final: {mae} (error relativo: {mae_percentage:.2f}%)")    
        

         # Graficar resultados finales
        plt.figure(figsize=(10, 5))
        plt.plot(test_data, label="Real")
        plt.plot(predictions, label="Predicciones")
        plt.title(f"Modelo Final SARIMAX: {best_params}")
        plt.legend()
        plt.show()

        return mae, predictions
    except ValueError as e:
        print(f"Error en predicción: {e}")
        return None, None

    print("Se ejecuto correctamente model_sarima")
    print("-------------------------------------------------------------------------------\n")