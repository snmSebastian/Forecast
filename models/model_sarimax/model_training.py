#==========================
#--- Paquetes
#==========================
from packages import Sarimax,grid_search_sarimax,ForecasterSarimax,TimeSeriesFold,backtesting_sarimax


#===================
#--- GridSearch
#===================
def perform_grid_search(serie,param_grid):
    """
    Realiza una búsqueda de rejilla (Grid Search) para encontrar las mejores combinaciones de parámetros
    para un modelo SARIMAX utilizando validación cruzada.

    Args:
        serie (pd.Series): Serie temporal sobre la que se ajustará el modelo.
        param_grid (list[dict]): Lista de combinaciones de parámetros a evaluar. Cada diccionario debe incluir:
            - `order` (tuple): Parámetros (p, d, q) para SARIMAX.
            - `seasonal_order` (tuple): Parámetros (P, D, Q, s) para la estacionalidad.

    Returns:
        pd.DataFrame or None: Resultados del Grid Search, ordenados por la métrica seleccionada. 
        Si ocurre un error, devuelve `None`.
    """
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
        

#==========================================
#--- Top10 best parameters by gridsearch
#==========================================
def get_best_sarimax_parameters(resultados_grid):
    """
    Selecciona las combinaciones de parámetros más prometedoras (basadas en el MAE) 
    del Grid Search.

    Args:
        resultados_grid (pd.DataFrame): Resultados del Grid Search, con columnas:
            - `order`: Parámetros (p, d, q) del modelo SARIMAX.
            - `seasonal_order`: Parámetros (P, D, Q, s) para la estacionalidad.
            - `mean_absolute_error`: MAE asociado a cada combinación de parámetros.

    Returns:
        list[dict]: Lista de las mejores combinaciones de parámetros. Cada diccionario incluye:
            - `order` (tuple): Parámetros del modelo SARIMAX.
            - `seasonal_order` (tuple): Parámetros para la estacionalidad.
    """
    #   Ordenar los resultados por MAE (por si acaso no vienen ordenados)
    resultados_grid_sorted = resultados_grid.sort_values('mean_absolute_error')

    # Seleccionar el top N de las mejores combinaciones
    top_n=10
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

#====================
# --- Backtesting 
#====================
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
