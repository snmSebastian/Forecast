
#============================================
#--- Mejores parametros para SARIMAX
#============================================
def find_sarima_order(serie, seasonal_periods=12, max_order=2, backtesting=False):
    """
    Encuentra los mejores parámetros SARIMAX para una serie temporal utilizando GridSearch.

    Args:
        serie (pd.Series): Serie temporal estacionarizada.
        seasonal_periods (int): Periodo estacional (default=12).
        max_order (int): Máximo valor de p, q, P, Q a evaluar (default=2).
        backtesting (bool): Indica si se utiliza validación cruzada (default=False).

    Returns:
        dict: Mejor combinación de hiperparámetros y su métrica de error.
    """
    try:
        # Crear combinaciones de hiperparámetros SARIMA
        p = q = P = Q = range(0, max_order + 1)
        d = D = [0, 1]  # Diferenciación posible
        orders = list(itertools.product(p, d, q))
        seasonal_orders = list(itertools.product(P, D, Q, [seasonal_periods]))

        best_params = None
        best_error = float("inf")

        for order in orders:
            for seasonal_order in seasonal_orders:
                try:
                    # Configurar modelo SARIMAX
                    model = SARIMAX(serie, order=order, seasonal_order=seasonal_order, enforce_stationarity=False, enforce_invertibility=False)
                    results = model.fit(disp=False)

                    # Métrica de error: validación cruzada o MSE simple
                    if backtesting:
                        errors = []
                        folds = 5  # Número de folds
                        step_size = len(serie) // (folds + 1)
                        for i in range(folds):
                            train = serie[:-(step_size * (i + 1))]
                            test = serie[-(step_size * (i + 1)): -(step_size * i)]
                            if len(test) > 0:
                                model = SARIMAX(train, order=order, seasonal_order=seasonal_order, enforce_stationarity=False, enforce_invertibility=False)
                                results = model.fit(disp=False)
                                predictions = results.forecast(steps=len(test))
                                errors.append(mean_squared_error(test, predictions))
                        error = sum(errors) / len(errors)
                    else:
                        error = mean_squared_error(serie, results.fittedvalues)

                    # Guardar mejores parámetros
                    if error < best_error:
                        best_error = error
                        best_params = {'order': order, 'seasonal_order': seasonal_order, 'error': best_error}
                except Exception as e:
                    continue  # Ignorar combinaciones no válidas

        print("Hiperparámetros óptimos encontrados:", best_params)
        return best_params
    except Exception as e:
        print(f"Error en find_sarima_order: {e}")
        return None



def fit_sarimax(serie, params):
    """
    Ajusta un modelo SARIMAX con los hiperparámetros proporcionados.

    Args:
        serie (pd.Series): Serie temporal.
        params (dict): Parámetros óptimos ('order', 'seasonal_order').

    Returns:
        SARIMAXResults: Resultados del modelo ajustado.
    """
    try:
        if not params or 'order' not in params or 'seasonal_order' not in params:
            raise ValueError("Parámetros inválidos para el modelo SARIMAX.")

        # Ajustar el modelo
        model = SARIMAX(serie, order=params['order'], seasonal_order=params['seasonal_order'], enforce_stationarity=False, enforce_invertibility=False)
        results = model.fit(disp=False)

        print(results.summary())
        print("Modelo ajustado exitosamente.")
        return results
    except Exception as e:
        print(f"Error en fit_sarimax: {e}")
        return None


def forecast_sarimax(results, steps=12):
    """
    Realiza pronósticos con un modelo SARIMAX ajustado.

    Args:
        results (SARIMAXResults): Resultados del modelo ajustado.
        steps (int): Número de pasos a predecir (default=12).

    Returns:
        pd.DataFrame: Predicciones con intervalos de confianza.
    """
    try:
        if not results or not hasattr(results, "forecast"):
            raise ValueError("El modelo no está ajustado correctamente.")

        forecast = results.get_forecast(steps=steps)
        forecast_df = forecast.summary_frame(alpha=0.05)  # Intervalo de confianza al 95%

        print("Pronósticos realizados exitosamente.")
        return forecast_df
    except Exception as e:
        print(f"Error en forecast_sarimax: {e}")
        return None
    

#==================================================


def grid_search_sarimax(serie, seasonal_periods=12, max_order=2, n_splits=5):
    """
    Realiza una búsqueda en cuadrícula (GridSearch) para encontrar la mejor combinación de parámetros SARIMAX.

    Args:
        serie (pd.Series): Serie temporal.
        seasonal_periods (int): Periodo estacional (default=12).
        max_order (int): Máximo valor de p, q, P, Q a evaluar (default=2).
        n_splits (int): Número de divisiones para validación cruzada (default=5).

    Returns:
        dict: Mejor combinación de parámetros y su error medio.
    """
    try:
        # Generar combinaciones de parámetros SARIMAX
        p = q = P = Q = range(0, max_order + 1)
        d = D = [0, 1]
        orders = list(itertools.product(p, d, q))
        seasonal_orders = list(itertools.product(P, D, Q, [seasonal_periods]))

        best_params = None
        best_error = float("inf")

        # Dividir la serie en validación cruzada de series temporales
        tscv = TimeSeriesSplit(n_splits=n_splits)

        for order in orders:
            for seasonal_order in seasonal_orders:
                errors = []
                for train_index, test_index in tscv.split(serie):
                    train, test = serie[train_index], serie[test_index]
                    try:
                        model = SARIMAX(train, order=order, seasonal_order=seasonal_order, enforce_stationarity=False, enforce_invertibility=False)
                        results = model.fit(disp=False)
                        predictions = results.forecast(steps=len(test))
                        errors.append(mean_squared_error(test, predictions))
                    except Exception as e:
                        continue

                mean_error = np.mean(errors)
                if mean_error < best_error:
                    best_error = mean_error
                    best_params = {'order': order, 'seasonal_order': seasonal_order, 'error': best_error}

        print("Mejores parámetros encontrados con GridSearch:", best_params)
        return best_params
    except Exception as e:
        print(f"Error en grid_search_sarimax: {e}")
        return None




def random_search_sarimax(serie, seasonal_periods=12, max_order=2, n_iter=10):
    """
    Realiza una búsqueda aleatoria (RandomSearch) para encontrar la mejor combinación de parámetros SARIMAX.

    Args:
        serie (pd.Series): Serie temporal.
        seasonal_periods (int): Periodo estacional (default=12).
        max_order (int): Máximo valor de p, q, P, Q a evaluar (default=2).
        n_iter (int): Número de iteraciones para la búsqueda aleatoria (default=10).

    Returns:
        dict: Mejor combinación de parámetros y su error medio.
    """
    try:
        # Generar todas las combinaciones posibles de parámetros
        p = q = P = Q = range(0, max_order + 1)
        d = D = [0, 1]
        orders = list(itertools.product(p, d, q))
        seasonal_orders = list(itertools.product(P, D, Q, [seasonal_periods]))

        best_params = None
        best_error = float("inf")

        for _ in range(n_iter):
            order = random.choice(orders)
            seasonal_order = random.choice(seasonal_orders)

            errors = []
            tscv = TimeSeriesSplit(n_splits=5)
            for train_index, test_index in tscv.split(serie):
                train, test = serie[train_index], serie[test_index]
                try:
                    model = SARIMAX(train, order=order, seasonal_order=seasonal_order, enforce_stationarity=False, enforce_invertibility=False)
                    results = model.fit(disp=False)
                    predictions = results.forecast(steps=len(test))
                    errors.append(mean_squared_error(test, predictions))
                except Exception as e:
                    continue

            mean_error = np.mean(errors)
            if mean_error < best_error:
                best_error = mean_error
                best_params = {'order': order, 'seasonal_order': seasonal_order, 'error': best_error}

        print("Mejores parámetros encontrados con RandomSearch:", best_params)
        return best_params
    except Exception as e:
        print(f"Error en random_search_sarimax: {e}")
        return None





def optimize_hyperparameters_sarimax(serie, seasonal_periods=12, max_order=2):
    """
    Optimiza los hiperparámetros del modelo SARIMAX combinando GridSearch y RandomSearch.

    Args:
        serie (pd.Series): Serie temporal.
        seasonal_periods (int): Periodo estacional (default=12).
        max_order (int): Máximo valor de p, q, P, Q a evaluar (default=2).

    Returns:
        dict: Mejor combinación de parámetros y su error medio.
    """
    # Primero intenta GridSearch para encontrar una buena región de parámetros
    best_grid_params = grid_search_sarimax(serie, seasonal_periods, max_order)
    
    # Luego realiza RandomSearch en torno a los parámetros encontrados
    best_random_params = random_search_sarimax(serie, seasonal_periods, max_order)
    
    # Comparar los resultados de GridSearch y RandomSearch y devolver el mejor
    if best_grid_params['error'] < best_random_params['error']:
        print("Optimizando con GridSearch.")
        return best_grid_params
    else:
        print("Optimizando con RandomSearch.")
        return best_random_params


def evaluate_sarimax_model(serie, best_params):
    """
    Evalúa el modelo SARIMAX con los mejores parámetros encontrados, realizando predicciones y calculando errores.

    Args:
        serie (pd.Series): Serie temporal.
        best_params (dict): Mejor combinación de parámetros.

    Returns:
        dict: Resultados del modelo.
    """
    try:
        model = SARIMAX(serie, order=best_params['order'], seasonal_order=best_params['seasonal_order'], enforce_stationarity=False, enforce_invertibility=False)
        results = model.fit(disp=False)
        predictions = results.forecast(steps=len(serie))
        
        error = mean_squared_error(serie, predictions)
        print("Modelo evaluado exitosamente.")
        return {'predictions': predictions, 'error': error}
    except Exception as e:
        print(f"Error en evaluate_sarimax_model: {e}")
        return None





