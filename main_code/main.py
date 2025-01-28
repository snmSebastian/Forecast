from data import historical_sales,historical_sales_and_predicts,historical_sales_and_predicts_country
from main_code import filtros,filtros_country
from preprocessing import time_serie
from models.model_sarimax import sarimax_model,sarimax_model_basico
from results import concat_result,concat_result_country,concat_result_country_basico

#===================================================
#--- Modelo por country y category group
#===================================================

'''
Este modelo realiza un pronostico por cada categoria existente por pais que satisfaga la condicion de tener al menos 70 registros
El modelo considera 3 filtros
    1 semilla autoarima
    2 grid search para generar una cuadricula con los mejores parametros alrededor de la semilla
    3 backtesting sobre  el top 10 la cuadricula 

Finalmente el modelo se entrena y pronostica con los mejores parametros encontrados, agregando los resultados junto con su mape

'''
ruta=r'/home/sebastian/Documentos/programas/Forescast Work/sales_historical.csv'
df_sales_and_product=historical_sales(ruta)
df_sales_and_predicts=historical_sales_and_predicts(df_sales_and_product)

for filters in filtros:
    print(f'entro al for: {filters}')
    country = filters['country']
    series_sales_dict,series_dict=time_serie(df_sales_and_predicts,filters)
    for category in list(series_dict.keys()):
        serie=series_dict[category]
        df_predict,best_results_backtesting=sarimax_model(serie)
        df_sales_and_predicts=concat_result(df_predict,df_sales_and_predicts,best_results_backtesting,country,category)
df_sales_and_predicts.to_csv('/home/sebastian/Documentos/programas/Forescast Work/sarimax.csv')



#===================================================
#--- Modelo por country 
#===================================================

'''
Este modelo realiza un pronostico por cada  pais que satisfaga la condicion de tener al menos 70 registros
El modelo considera 3 filtros
    1 semilla autoarima
    2 grid search para generar una cuadricula con los mejores parametros alrededor de la semilla
    3 backtesting sobre  el top 10 la cuadricula 

Finalmente el modelo se entrena y pronostica con los mejores parametros encontrados, agregando los resultados junto con su mape

'''
ruta=r'/home/sebastian/Documentos/programas/Forescast Work/sales_historical.csv'
df_sales_and_product=historical_sales(ruta)
df_sales_and_predicts=historical_sales_and_predicts_country(df_sales_and_product)
series_sales_dict,series_dict=time_serie(df_sales_and_predicts,filtros_country)
for country in list(series_dict.keys()):
    print(f'entro al for para: {country}')
    serie=series_dict[country]
    print(f'genero la serie para: {country}')
    df_predict,best_results_backtesting=sarimax_model(serie)
    print(f'realizo el modelo para {country}')
    df_sales_and_predicts=concat_result_country_basico(df_predict,df_sales_and_predicts,country)
    print(f'agrego los resultados para {country}')
df_sales_and_predicts.to_csv('/home/sebastian/Documentos/programas/Forescast Work/sarimax_country.csv')




#===================================================
#--- Modelo por country Basico
#===================================================

'''
Este modelo realiza un pronostico por cada categoria existente por pais que satisfaga la condicion de tener al menos 70 registros
El modelo considera solo 1 filtro 
    1 semilla autoarima

Finalmente el modelo se entrena y pronostica con los mejores parametros encontrados, agregando los resultados
'''

ruta=r'/home/sebastian/Documentos/programas/Forescast Work/sales_historical.csv'
df_sales_and_product=historical_sales(ruta)
df_sales_and_predicts=historical_sales_and_predicts_country(df_sales_and_product)
series_sales_dict,series_dict=time_serie(df_sales_and_predicts,filtros_country)
for country in list(series_dict.keys()):
    print(f'entro al for para: {country}')
    serie=series_dict[country]
    print(f'genero la serie para: {country}')
    df_predict,best_results_backtesting=sarimax_model_basico(serie)
    print(f'realizo el modelo para {country}')
    df_sales_and_predicts=concat_result_country(df_predict,df_sales_and_predicts,best_results_backtesting,country)
    print(f'agrego los resultados para {country}')
df_sales_and_predicts.to_csv('/home/sebastian/Documentos/programas/Forescast Work/sarimax_country_basico.csv')

