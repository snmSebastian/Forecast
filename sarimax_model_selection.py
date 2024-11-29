
from packages import SARIMAX
from packages import mean_absolute_error
from packages import plt
from evaluate_mode import evaluate_sarimax

def sarimax_models(param_grid, train_data, test_data):
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

    best_predictions=None
    best_params = None
    best_mae = float('inf')  # Inicializar con un valor alto
    
    train_end = len(train_data) - 1
    test_start = len(train_data)
    test_end = test_start + len(test_data) - 1
    
    for params in param_grid:
        try:
            mae, predictions = evaluate_sarimax(params, train_data, test_data)
            
            # Actualizar si se encuentra un mejor modelo
            if mae < best_mae:
                best_mae = mae
                best_params = params  
                best_predictions = predictions        
        except Exception as e:
            print(f"Error con parámetros {params}: {e}")
    
    mae_percentage = (best_mae / test_data.mean()) * 100 
    print(f"El mae: {best_mae} representa un porcentaje de error del: {mae_percentage:.2f}%")
    
    plt.figure(figsize=(10, 5))
    plt.plot(test_data, label="Real")
    plt.plot(best_predictions, label="Predicciones")
    plt.title(f"Mejor modelo SARIMAX: {best_params}")
    plt.legend()
    plt.show()
    return best_params, best_mae

    print("Se ejecuto correctamente: sarimax_models")   
    print("-------------------------------------------------------------------------------\n")