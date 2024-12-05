from packages import SARIMAX
from packages import mean_absolute_error
from packages import warnings
from packages import ForecasterSarimax
from packages import Sarimax
from packages import plt
from series_graphs import graph_sales_forecast
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
    #Ignora los mensajes de alearta al entrenar el modelo
    warnings.filterwarnings("ignore")
    try:
        model = SARIMAX(
            train_data,
            order=(p, d, q),
            seasonal_order=(P, D, Q, s),
            enforce_stationarity=False,
            enforce_invertibility=False,
        ).fit(disp=False)
        #retorna los mensajes de alerta
        warnings.filterwarnings("default")
        predictions = model.predict(start=len(train_data), end=len(train_data) + len(test_data) - 1)
        mae = mean_absolute_error(test_data, predictions)
       
        return mae, predictions

    except Exception as e:
        print(f"Error con parámetros {params}: {e}")
        return float('inf'), None
    

#======================================
# --- Foracaster Sarimax    
#======================================

def trainig_forecaster_sarimax(params,train_data,test_data):
    """
    Entrena y evalúa un modelo Foracaster Sarimax de la clase skforecast con parámetros específicos.

    Retorna:
    - mae: Error absoluto medio.
    - predictions: Predicciones generadas por el modelo.
    """
    p, d, q, P, D, Q, s = params

    #Ignora los mensajes de alearta al entrenar el modelo
    warnings.filterwarnings("ignore")

    try:
        forecaster=ForecasterSarimax(
        regressor=Sarimax(
            order=(p,d,q),
            seasonal_order=(P,D,Q,s)
            )
        )
        forecaster.fit(y=train_data,suppress_warnings=True)
        predictions=forecaster.predict(steps=len(test_data))
        mae = mean_absolute_error(test_data, predictions)
        #retorna los mensajes de alerta
        warnings.filterwarnings("default")
        return mae, predictions
    except Exception as e:
        print(f"Error con parámetros {params}: {e}")
        return float('inf'), None

