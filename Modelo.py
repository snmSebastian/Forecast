from sales_loader import historical_sales
from devoluciones import devolucion
from series_graphs import graph_line
from time_series_processing import time_serie, seasonalize_series
from data_segmentation import data_model
from parameters_auto_arima import best_parameters_auto_arima
from param_grid_generator import generate_param_grid
from sarimax_model_selection import sarimax_models
from models import model_sarima
from data_segmentation import select_data

#ruta=r'/home/sebastian/Documentos/programas/Forescast Work/sales_historical.csv'   
ruta=r'/home/sebastian/Documentos/programas/Forescast Work/sales_historical_prueba.csv'
df_sales_and_product=historical_sales(ruta)


#--- Filtra los datos de ventas según los filtros especificados y devuelve una serie de tiempo.
filtros={
'Brand':[''],
'Country Code':[''],
'GPP Division Code':[]

}
serie,serie_sales=time_serie(df_sales_and_product,{'Category Group':'Clamps'})

#--- Estacionariza la serie
serie=seasonalize_series(serie)


#--- Segmenta una serie en conjuntos de entrenamiento, validación y prueba, y genera versiones estacionalizadas.
data_train_original, data_validation_original,\
      data_train_estacionalizado,data_validation_estacionalizado=data_model(serie_sales,serie)

#--- Define si los conjuntos de train y test pertencer a la serie estacionariaza o la original
train_data, test_data = select_data(serie_sales,serie,\
                 data_train_original, data_validation_original,\
                      data_train_estacionalizado, data_validation_estacionalizado)

#--- Obtener los mejores parametros para:p,d,q,P,D,Q,s
p_range, d_range, q_range, P_range, D_range, Q_range, s=best_parameters_auto_arima(train_data)
#--- Genera todas las combinaciones posibles de hiperparámetros para el modelo SARIMAX.
param_grid = generate_param_grid(p_range, d_range, q_range, P_range, D_range, Q_range, s)

#Evalúa todos los modelos SARIMAX generados a partir de un param_grid y selecciona el mejor modelo según el MAE.
best_params, best_mae = sarimax_models(param_grid, train_data, test_data)

#--- Ajusta y evalúa un modelo SARIMAX con parámetros específicos para la serie temporal, 
#    calculando el error medio absoluto (MAE) de las predicciones.
model_sarima(best_params,
                 train_data,test_data)
print("-------------------------------------------------------------------------------")