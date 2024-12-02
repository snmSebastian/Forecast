#=======================
#--- Paquetes
#=======================
from packages import SARIMAX
from packages import plt


#========================================================
#--- Definicion de los modelos finales
#========================================================


#=======================
#--- Sarimax
#=======================
def model_sarima(best_params,serie):

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
        serie,
        order=(p, d, q),
        seasonal_order=(P, D, Q, s),
        enforce_stationarity=False,
        enforce_invertibility=False,
        disp=0
        ).fit()
        # Generar predicciones a futuro con forecast
        forecast_steps = 12  # Predecir los próximos 12 meses
        forecast = model.forecast(steps=forecast_steps)
       # predictions = model.predict(start=len(serie), end=len(serie) + len(test_data) - 1)
       # Graficar la serie original y el pronóstico
        #plt.figure(figsize=(10, 5))
        #plt.plot(serie, label="Serie Original", color="blue")
        #plt.plot(
        #    range(len(serie), len(serie) + forecast_steps),
         #   forecast, label="Pronóstico", color="orange"
        #)
        #plt.title(f"Modelo Final SARIMAX: {best_params}")
        #plt.legend()
        #plt.show()

        print(f"Pronóstico generado correctamente para los próximos {forecast_steps} meses.")
        return forecast
    except ValueError as e:
        print(f"Error en predicción: {e}")
        return None, None

    print("Se ejecuto correctamente model_sarima")
    print("-------------------------------------------------------------------------------\n")


