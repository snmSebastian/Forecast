
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

def best_parameters_auto_arima(train_data):
    
    ''' Recibe una serie estacionarizada, realiza un proceso autoarima para obtener los mejores parametros para:p,d,q,P,D,Q,s
    con base en estos valores establece los rangos que seran usados en la optimizacion de hiperparametros por medio de 
    gridsearch

    Parámetros:
        serie (pd.Series): Serie estacionarizada 

    Retorna:
        tuple: Rangos para los parámetros p, d, q, P, D, Q y s.
    '''


    #Identifica si se esta trabajando con la serie original o la estacionarizada, con base en esto elige el conjunto train
    #con el cual entrenar el modelo autorima
    
    # Dividir la serie en conjuntos de entrenamiento, validación y prueba
    #train_data, val_data, test_data, train_data_est, val_data_est, test_data_est = Data_Model(serie)

    # Ignorar advertencias para mantener limpio el output
    warnings.filterwarnings("ignore", category=UserWarning, message='Non-invertible|Non-stationary')


    #Realizar autoarima
    auto_model = auto_arima(train_data,
                        seasonal=True,
                        m=12,  # Periodo estacional
                        trace=False,  # Muestra el progreso
                        error_action='ignore',
                        suppress_warnings=True,
                        stepwise=True)

# Obtén los parámetros recomendados
    best_params = auto_model.get_params()['order']
    best_seasonal_params = auto_model.get_params()['seasonal_order']

    #print(f"Parámetros recomendados por AutoARIMA: {best_params}, {best_seasonal_params}")

    # Define rangos reducidos basados en AutoARIMA
    p_range = range(max(0, best_params[0] - 1), best_params[0] + 2)
    d_range = [best_params[1]]  # Usualmente no necesitas variar mucho `d`
    q_range = range(max(0, best_params[2] - 1), best_params[2] + 2)

    P_range = range(max(0, best_seasonal_params[0] - 1), best_seasonal_params[0] + 2)
    D_range = [best_seasonal_params[1]]  # Similar a `d`, no suele variar mucho
    Q_range = range(max(0, best_seasonal_params[2] - 1), best_seasonal_params[2] + 2)
    s = [best_seasonal_params[3]]  # Período fijo

    '''
    print(f'p_range: {p_range}')
    print(f'd_range: {d_range}')
    print(f'q_range: {q_range}')
    print(f'P_range: {P_range}')
    print(f'D_range: {D_range}')
    print(f'Q_range: {Q_range}')
    print(f's_range: {s}')
    '''
    print("Se ejecuto correctamente: best_parameters_auto_arima")
    print("-------------------------------------------------------------------------------\n")
    return p_range, d_range, q_range, P_range, D_range, Q_range, s

#==========================================================================
#--- Genera rango alrededor de los mejores parametros Autoarima
#==========================================================================

def generate_param_grid(p_range, d_range, q_range, P_range, D_range, Q_range, s_range):
    """
    Genera todas las combinaciones posibles de hiperparámetros para el modelo SARIMAX.
    
    Parámetros:
    - p_range, d_range, q_range: Rango de los parámetros ARIMA (p, d, q).
    - P_range, D_range, Q_range: Rango de los parámetros estacionales (P, D, Q).
    - s_range: Rango del período estacional (s).
    
    Retorna:
    - param_grid: Lista de combinaciones de parámetros.
    """
    param_grid = list(product(p_range, d_range, q_range, P_range, D_range, Q_range, s_range))
    print("Se ejecuto correctamente: generate_param_grid")
    print("-------------------------------------------------------------------------------\n")

    return param_grid

