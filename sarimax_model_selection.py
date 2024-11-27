
from packages import SARIMAX
from packages import mean_absolute_error
from packages import plt
def sarimax_models(serie_sales,serie,param_grid,
                    data_train_original,data_validation_original,
                    data_train_estacionalizado,data_validation_estacionalizado):
    """
    Evalúa todos los modelos SARIMAX generados a partir de un param_grid y selecciona el mejor modelo según el MAE.
    
    Parámetros:
    - param_grid: Combinaciones de parámetros.
    - y_train: Datos de entrenamiento.
    - y_test: Datos de prueba.
    
    Retorna:
    - best_params: Los mejores parámetros encontrados.
    - best_mae: El MAE más bajo obtenido.
    """
    
    #Identifica si se esta trabajando con la serie original o la estacionarizada, con base en esto elige el conjunto train
    #con el cual entrenar el modelo autorima
    print("seleccion modelo sarimax")
    if len(serie)<len(serie_sales):
        print("se trabajo con serie estacionalizada")
        train_data=data_train_estacionalizado
        test_data=data_validation_estacionalizado
    else:
        print("se trabajo con serie orginal")
        train_data=data_train_original
        test_data=data_validation_original

    best_params = None
    best_mae = float('inf')  # Inicializar con un valor alto
    
    train_end = len(train_data) - 1
    test_start = len(train_data)
    test_end = test_start + len(test_data) - 1
    
    for params in param_grid:
        try:
            # Desempaquetar los parámetros
            p, d, q, P, D, Q, s = params
            
            # Entrenar el modelo
            model = SARIMAX(
                train_data,
                order=(p, d, q),
                seasonal_order=(P, D, Q, s),
                enforce_stationarity=False,
                enforce_invertibility=False,
            ).fit(disp=False)
            
            # Generar predicciones
            predictions = model.predict(start=test_start, end=test_end)
            
            # Calcular MAE
            mae = mean_absolute_error(test_data, predictions)
            
            # Actualizar si se encuentra un mejor modelo
            if mae < best_mae:
                best_mae = mae
                best_params = params
            
        except Exception as e:
            print(f"Error con parámetros {params}: {e}")
    
    mae_percentage = (best_mae / test_data.mean()) * 100 
    print(f"El mae: {best_mae} representa un porcentaje de error del: {mae_percentage:.2f}%")
    print("Se ejecuto correctamente: sarimax_models") 
    print("-------------------------------------------------------------------------------\n")
    plt.plot(test_data, label="Real")
    plt.plot(predictions, label="Predicciones")
    plt.legend()
    plt.show()
    return best_params, best_mae