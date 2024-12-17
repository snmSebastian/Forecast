from parameters.parameters_optimization import best_parameters_auto_arima,generate_param_grid
from packages import Sarimax,grid_search_sarimax,ForecasterSarimax,TimeSeriesFold,backtesting_sarimax
from data.data_segmentation import data_model
from preprocessing.time_series_analysis import time_serie

"""
Constructor de la clase para inicializar la serie de tiempo.
"""
#serie=time_serie
#train_data,test_data = data_model2(serie) # Usando la función data_model2

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


def perform_grid_search(serie,param_grid):
    forecaster = ForecasterSarimax(
    regressor=Sarimax(
    order=(1, 1, 1),
    seasonal_order=(1, 1, 1, 12),
    enforce_stationarity=False,  # Relaja restricciones de estacionariedad
    enforce_invertibility=False,  # Relaja restricciones de invertibilidad
    maxiter=500
           )
    )
    initial_train_size=len(serie)-3*12
    cv = TimeSeriesFold(
    steps              = 12,
    initial_train_size = initial_train_size,
    refit              = True,
    fixed_train_size   = False,
    )

    try:
        resultados_grid = grid_search_sarimax(
        forecaster=forecaster,
        y=serie,
        cv=cv,
        param_grid=param_grid,
        metric='mean_absolute_error',
        return_best=False,
        n_jobs='auto',
        suppress_warnings_fit=True,
        verbose=False,
        show_progress=True,
        )
        return resultados_grid
    except Exception as e:
        print(f"Error al ajustar un modelo: {e}")
        resultados_grid = None
        return resultados_grid
        

def get_best_sarimax_parameters(resultados_grid, top_n=10):
    """
    Extrae las combinaciones de parámetros del top N resultados de `resultados_grid`.
    """
    #   Ordenar los resultados por MAE (por si acaso no vienen ordenados)
    resultados_grid_sorted = resultados_grid.sort_values('mean_absolute_error')

    # Seleccionar el top N de las mejores combinaciones
    top_rows = resultados_grid_sorted.head(top_n)
    top_params = []
    for _, row in top_rows.iterrows():
        params_dict = {
        'order': row['order'],
        'seasonal_order': row['seasonal_order'],
        #'trend': row.get('trend', None)
    }
        top_params.append(params_dict)

    return top_params

        
def run_backtesting(serie, top_params):
    """
    Realiza backtesting con todas las opciones de parámetros en top_params y devuelve el diccionario 
    con los mejores resultados (MAE).

    Args:
    - top_params: Lista de diccionarios con las combinaciones de parámetros.
    Returns:
    - mejores_resultados: Diccionario con los parámetros y MAE del mejor modelo.
    """
    best_results_backtesting = {
    'params': None,
    'mae': float('inf')  # Inicializamos con un valor muy alto
        }

    for params_dict in top_params:
        print(params_dict)
        forecaster = ForecasterSarimax(
                regressor=Sarimax(
                    order=params_dict['order'],
                    seasonal_order=params_dict['seasonal_order'],
                    #trend=params_dict['trend'],
                    maxiter=500
                )
            )
        initial_train_size=len(serie)-3*12
        cv = TimeSeriesFold(
                steps=12,
                initial_train_size=initial_train_size,
                refit=True,
            )

        # Realizar el backtesting
        try:
            resultados = backtesting_sarimax(
                forecaster=forecaster,
                y=serie,
                cv=cv,
                metric='mean_absolute_error',
                n_jobs="auto",
                suppress_warnings_fit=True,
                verbose=False,
                show_progress=True
            )
            
            mae = resultados[0]['mean_absolute_error'].iloc[0]  # Si 'backtesting_sarimax' devuelve un DataFrame o lista, extrae el MAE
            print(f'resultado [0]:{mae}')
            # Asegúrate de que `mae` es un valor numérico
            if  mae < best_results_backtesting['mae']:
                best_results_backtesting['mae'] = mae
                best_results_backtesting['params'] = params_dict
                print(f'se actualizaron resultados:{mae}-{params_dict}')
            #print(resultados)
            #return resultados
        except Exception as e:
            resultados=None
            best_results_backtesting=None
            print(f"Error al ajustar el modelo con parámetros {params_dict}: {e}")
    
    return resultados,best_results_backtesting

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
