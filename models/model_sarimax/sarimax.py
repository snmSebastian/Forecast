#====================
#--- Paquetes
#====================
from preprocessing import preprocess_series

from .parameter_generation import generate_initial_param_grid,best_parameters_auto_arima
from .model_training import get_best_sarimax_parameters, perform_grid_search, run_backtesting
from .prediction import fit_final_model_and_predict,fit_final_model_and_predict_basico
from results import inverse_transform

#============================================
#--- Modelo Sarimax
#============================================
def sarimax_model(serie):
    '''
    Recibe una serie sin procesamiento y realiza
        1 transformacion de la serie mediante log
        2 Genera una cuadricula de parametros alrededor de la semilla generada por autoarima
        3 Realiza una búsqueda de rejilla (Grid Search) para encontrar las mejores combinaciones de parámetros 
          para un modelo SARIMAX utilizando validación cruzada.
        4 Selecciona las combinaciones de parámetros más prometedoras (basadas en el MAE) 
          del Grid Search.
        5 Realiza backtesting con todas las opciones de parámetros en top_params y devuelve el diccionario 
          con los mejores resultados (MAE).
        6  Ajusta el modelo final con los mejores parámetros y realiza predicciones.
        7  Reconvierte las predicciones preprocesadas a la escala original de la serie temporal.

    return
        dataframe con las predicciones y sus parametros
    ''' 
    transfor_serie,diff_serie_tendencia,diff_serie_estacionalidad=preprocess_series(serie)
    param_grid=generate_initial_param_grid(transfor_serie)
    #print("generate_initial_param_grid")
    resultados_grid=perform_grid_search(transfor_serie,param_grid)
    #print("perfom_:grid_search")
    top_params=get_best_sarimax_parameters(resultados_grid)
    #print("get best sarimaz")
    best_results_backtesting=run_backtesting(transfor_serie, top_params)
    #print("backstesting")
    predictions=fit_final_model_and_predict(transfor_serie, best_results_backtesting)
    #print("final model")
    df_predict=inverse_transform(serie,diff_serie_tendencia,diff_serie_estacionalidad,predictions)
    
    return df_predict,best_results_backtesting



#============================================
#--- Modelo Sarimax basico
#============================================
def sarimax_model_basico(serie):
    '''
    Recibe una serie sin procesamiento y realiza
        1 transformacion de la serie mediante log
        2 obtiene parametros mediante autoarima
        3 realiza el pronostico del modelo con los parametros encontrados
        4  Reconvierte las predicciones preprocesadas a la escala original de la serie temporal.

    return
        dataframe con las predicciones
    ''' 
    transfor_serie,diff_serie_tendencia,diff_serie_estacionalidad=preprocess_series(serie)
    best_params_arima,best_seasonal_params_arima=best_parameters_auto_arima(transfor_serie)
  
    predictions=fit_final_model_and_predict_basico(transfor_serie, best_params_arima,best_seasonal_params_arima)
    #print("final model")
    df_predict=inverse_transform(serie,diff_serie_tendencia,diff_serie_estacionalidad,predictions)
    
    return df_predict


