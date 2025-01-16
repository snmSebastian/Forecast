#====================
#--- Paquetes
#====================
from preprocessing import preprocess_series

from .parameter_generation import generate_initial_param_grid
from .model_training import get_best_sarimax_parameters, perform_grid_search, run_backtesting
from .prediction import fit_final_model_and_predict
from results import inverse_transform

#============================================
#--- Modelo Sarimax
#============================================
def sarimax_model(serie):
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


