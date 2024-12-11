
#=================
#--- Paquetes
#=================
import warnings
from packages import auto_arima
from packages import product
from packages import mean_absolute_error
from packages import itertools
from packages import SARIMAX

#====================================================================
#--- Obitiene los mejores parametros de la serie segun Autoarima
#====================================================================

def best_parameters_auto_arima(serie):
    
    ''' Recibe una serie, realiza un proceso autoarima para obtener los mejores parametros para:p,d,q,P,D,Q,s

    Parámetros:
        serie (pd.Series): Serie 

    Retorna:
        tuple: best_params_arima: parametros p,d,q
                best_seasonal_params_arima: parametros P,D,Q,s
    '''
    # Ignorar advertencias para mantener limpio el output
    warnings.filterwarnings("ignore", category=UserWarning, message='Non-invertible|Non-stationary')


    #Realizar autoarima
    auto_model = auto_arima(serie,
                        seasonal=True,
                        m=12,  # Periodo estacional
                        trace=False,  # Muestra el progreso
                        error_action='ignore',
                        suppress_warnings=True,
                        stepwise=True)

    # Obtén los parámetros recomendados
    best_params_arima = auto_model.get_params()['order']
    best_seasonal_params_arima = auto_model.get_params()['seasonal_order']

    #print(f"Parámetros recomendados por AutoARIMA: {best_params}, {best_seasonal_params}")
    return best_params_arima,best_seasonal_params_arima

#==============================================================
#--- Genera una cuadricula de parametros
#==============================================================

def generate_param_grid(best_params_arima,best_seasonal_params_arima):

    """
    Genera todas las combinaciones posibles de los mejores parametros obtenidos de Autoarima .
    
    Parámetros:
    - best_params_arima: parametros p,d,q
      best_seasonal_params_arima: parametros P,D,Q,s
    Retorna:
    - param_grid: Lista de combinaciones de parámetros.
    """
    p_range = range(max(0, best_params_arima[0] - 2), best_params_arima[0] + 4)
    d_range = [best_params_arima[1]]
    q_range = range(max(0, best_params_arima[2] - 2), best_params_arima[2] + 4)

    P_range = range(max(0, best_seasonal_params_arima[0] - 2), best_seasonal_params_arima[0] + 4)
    D_range = [best_seasonal_params_arima[1]]
    Q_range = range(max(0, best_seasonal_params_arima[2] - 2), best_seasonal_params_arima[2] + 4)
    s_range = [best_seasonal_params_arima[3]]

    trend = [None, 'n', 'c']  # Si "trend" no es necesario, remuévelo
    param_grid = {
        'order': list(product(p_range, d_range, q_range)),
        'seasonal_order': list(product(P_range, D_range, Q_range, s_range)),
        'trend': trend
    }

    #FIltra p,d,q P,D,Q,s!=0
    param_grid['order'] = [order for order in param_grid['order'] if order != (0, 0, 0)]
    param_grid['seasonal_order'] = [s_order for s_order in param_grid['seasonal_order'] if s_order[:3] != (0, 0, 0)]
    
    #Filtra p,d,q,P,D,Q,s cuya suma sea menor 24
    valid_params = [
        params for params in param_grid['order']
        if sum(params) < 24 # Requisito para que el modelo pueda ajustarse
        ]
    param_grid['order'] = valid_params
    
    print("Se ejecuto correctamente: generate_param_grid")
    print("-------------------------------------------------------------------------------\n")
    return param_grid

