from packages import product

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