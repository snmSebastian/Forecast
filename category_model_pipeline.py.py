#============================
#--- Paquetes
#============================
from data_loading import historical_sales
#from series_graphs import graph_line
from sarimax_model import generate_sarimax_by_category
from time_series_analysis import forecast_data

def  generate_models_by_category(df_sales_and_product,filtros):
    '''Recibe informacion de ventas, y filtros de categorias, y evalua para cada categoria un modelo sarimax
    con los mejores parametros
    Arg: df_sales_and_product( dataframe de ventas)
        lst_category:lista de las categorias a las cuales se les realizara pronostico
    Out: dataframe con 12 registros mas correspondientes al pronostico
        columnas( sales, )
    '''
    df_sales_forecast= forecast_data(df_sales_and_product)

    generate_sarimax_by_category(df_sales_and_product,filtros,df_sales_forecast)
       
ruta=r'/home/sebastian/Documentos/programas/Forescast Work/sales_historical_prueba.csv'
lst_category=['Pliers','Clamps']
filtros={
#'Brand':[''],
'Country':['Mexico'],
'Category Group':lst_category
}
df_sales_and_product=historical_sales(ruta)
generate_models_by_category(df_sales_and_product,filtros)