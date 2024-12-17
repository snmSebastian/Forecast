from .parameter_generation import generate_initial_param_grid
from .model_training import get_best_sarimax_parameters, perform_grid_search, run_backtesting
from .prediction import fit_final_model_and_predict

def sarimax_model(serie):
    param_grid=generate_initial_param_grid(serie)
    print("generate_initial_param_grid")
    resultados_grid=perform_grid_search(serie,param_grid)
    print("perfom_:grid_search")
    top_params=get_best_sarimax_parameters(resultados_grid)
    print("get best sarimaz")
    resultados,best_results_backtesting=run_backtesting(serie, top_params)
    print("backstesting")
    predicciones=fit_final_model_and_predict(serie, best_results_backtesting)
    print("final model")
    return predicciones