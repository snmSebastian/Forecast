#==========================
#--- Paquetes
#==========================
from parameters.parameters_optimization import best_parameters_auto_arima,generate_param_grid

def generate_initial_param_grid(serie):
    """
    Genera una rejilla inicial de parámetros para SARIMAX.

    Args:
        serie (pd.Series): Serie temporal para la que se generarán los parámetros.

    Returns:
        dict: Rejilla de parámetros con las mejores combinaciones iniciales.
    """

    best_params_arima,best_seasonal_params_arima=best_parameters_auto_arima(serie)
    param_grid=generate_param_grid(best_params_arima,best_seasonal_params_arima)
    return param_grid
