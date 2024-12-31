from data import historical_sales,historical_sales_and_predicts
from main_code import filtros
from preprocessing import time_serie
from models.model_sarimax import sarimax_model
from results import concat_result


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