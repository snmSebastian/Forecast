#================================
#--- Paquetes
#================================
from packages import Sarimax,ForecasterSarimax

def fit_final_model_and_predict(serie, best_results_backtesting):
    """
    Ajusta el modelo final con los mejores parámetros y realiza predicciones.
    """
    forecaster = ForecasterSarimax(
        regressor=Sarimax(
        order=best_results_backtesting['params']['order'],
        seasonal_order=best_results_backtesting['params']['seasonal_order'],
        trend=best_results_backtesting['params'].get('trend', None),
        maxiter=500
        )
        )

    # Ajustar el modelo final
    forecaster.fit(serie)
    # Realizar predicciones
    predicciones = forecaster.predict(steps=12)
    return predicciones


def fit_final_model_and_predict_basico(serie, best_params_arima,best_seasonal_params_arima):
    """
    Ajusta el modelo final con los mejores parámetros y realiza predicciones.
    """
    forecaster = ForecasterSarimax(
        regressor=Sarimax(
        order=best_params_arima,
        seasonal_order=best_seasonal_params_arima,
        maxiter=500
        )
        )

    # Ajustar el modelo final
    forecaster.fit(serie)
    # Realizar predicciones
    predicciones = forecaster.predict(steps=12)
    return predicciones
