from sales_loader import historical_sales
from devoluciones import devolucion
from series_graphs import graph_line
from time_series_processing import time_serie, seasonalize_series
from data_segmentation import data_model
from parameters_auto_arima import best_parameters_auto_arima
from param_grid_generator import generate_param_grid
from sarimax_model_selection import sarimax_models
from models import model_sarima

'''
ruta=r'/home/sebastian/Documentos/programas/Forescast Work/Sales_History.csv'
df_sales_and_product= historical_sales(ruta)
serie,series_sales=time_serie(df_sales_and_product,{'Country Code':'Mexico'})
serie=seasonalize_series(serie)
graph_line(serie)'''

'''lectura del csv con la inf de venta historica:  este archivo csv es el resultado de unificar todos los xlsx de sharepoint,
filtrando las columnas de interes para el modelo'''

ruta=r'/home/sebastian/Documentos/programas/Forescast Work/Sales_History.csv'   
df_sales_and_product=historical_sales(ruta)

'''
    Filtra los datos de ventas según los filtros especificados y devuelve una serie de tiempo.
    Estacionariza la serie
'''
filtros={
'Brand':[''],
'Country Code':[''],
'GPP Division Code':[]

}

serie,serie_sales=time_serie(df_sales_and_product,{'Country Code':'Mexico'})
seasonalize_series(serie)