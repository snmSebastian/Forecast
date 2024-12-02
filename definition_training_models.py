from packages import SARIMAX
from packages import mean_absolute_error

#=================================================
#---- Definicion modelos que se entrenaran
#=================================================



#======================
#--- SARIMAX
#======================
def training_sarimax(params, train_data, test_data):
    """
    Entrena y evalúa un modelo SARIMAX con parámetros específicos.

    Retorna:
    - mae: Error absoluto medio.
    - predictions: Predicciones generadas por el modelo.
    """
    p, d, q, P, D, Q, s = params
    try:
        model = SARIMAX(
            train_data,
            order=(p, d, q),
            seasonal_order=(P, D, Q, s),
            enforce_stationarity=False,
            enforce_invertibility=False,
        ).fit(disp=False)
        predictions = model.predict(start=len(train_data), end=len(train_data) + len(test_data) - 1)
        mae = mean_absolute_error(test_data, predictions)
        return mae, predictions
    except Exception as e:
        print(f"Error con parámetros {params}: {e}")
        return float('inf'), None
    
