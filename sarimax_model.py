#============================
#--- Paquetes
#============================

from data_loading import historical_sales
#from series_graphs import graph_line
from time_series_analysis import time_serie, seasonalize_series
from data_segmentation import data_model
from data_segmentation import select_data
from parameters_optimization import best_parameters_auto_arima
from parameters_optimization import generate_param_grid
from definition_training_models import training_sarimax
from defintion_final_models import model_sarima
from packages import plt
from packages import pd
from time_series_analysis import forecast_data
from packages import warnings
from definition_training_models import trainig_forecaster_sarimax
from packages import mean_squared_error,itertools,SARIMAX
from packages import random,TimeSeriesSplit,np
from data_segmentation import data_model2
#===================================================
#Se entrenan Sarimax en un rango de parametros 
#===================================================

#============================
#--- find_best_sarimax_params
#============================
def find_best_sarimax_params(param_grid, train_data, test_data):
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
    #Ignora los mensajes de alearta al entrenar el modelo
    warnings.filterwarnings("ignore")

    best_predictions=None
    best_params = None
    best_mae = float('inf')  # Inicializar con un valor alto
    
    for params in param_grid:
        try:
            mae, predictions = training_sarimax(params, train_data, test_data)
            #mae,predictions = trainig_forecaster_sarimax(params, train_data, test_data)
        
            # Actualizar si se encuentra un mejor modelo
            if mae < best_mae:
                best_mae = mae
                best_params = params  
                best_predictions = predictions  

        except Exception as e:
            print(f"Error con parámetros {params}: {e}")
        
        mae_percentage = (best_mae / test_data.mean()) * 100 
        print(f"El mae: {best_mae} representa un porcentaje de error del: {mae_percentage:.2f}%")
    return best_params, best_mae
    print("-------------------------------------------------------------------------------\n")
    
#======================================================
#--- Generate_models_by_category
#======================================================

def  generate_sarimax_by_category(df_sales_and_product,filtros,df_sales_forecast):
    """
    Genera y evalúa modelos SARIMAX para cada categoría en la lista proporcionada.

    Esta función toma un DataFrame con información de ventas y, para cada categoría especificada:
    - Filtra los datos de ventas.
    - Estacionariza la serie temporal.
    - Segmenta los datos en conjuntos de entrenamiento, validación y prueba.
    - Optimiza los hiperparámetros para un modelo SARIMAX.
    - Evalúa los modelos generados y selecciona el mejor.
    - Ajusta el modelo final y calcula el MAE.

    Args:
        df_sales_and_product (pd.DataFrame): DataFrame con datos de ventas.
        lst_category (list): Lista de categorías para las cuales se evaluarán y ajustarán modelos SARIMAX.

    Returns:
        None: La función imprime los resultados del modelo para cada categoría. 
        Los resultados incluyen el mejor modelo y el MAE asociado.

    Notas:
        - La función supone que las columnas necesarias (`Category Group`, `Date`, `Total Sales`, etc.) están presentes en `df_sales_and_product`.
        - Los modelos se ajustan para series estacionalizadas.
        - Requiere que las funciones auxiliares (time_serie, seasonalize_series, etc.) estén correctamente implementadas.
    """
     #Ignora los mensajes de alearta al entrenar el modelo
    warnings.filterwarnings("ignore")
   
    print("inicio generate sarimax by category")
    serie_sales_dict,series_dict = time_serie(df_sales_and_product, filtros)
    serie=None
    for category in filtros['Category Group']:
        print(f'for {category}')
        serie=series_dict[category]
        print("serie crea")
        #--- Estacionariza la serie
        serie=seasonalize_series(serie)

        #--- Define si los conjuntos de train y test pertencer a la serie estacionariaza o la original
        train_data, test_data = data_model2(serie)

        #--- Obtener los mejores parametros para:p,d,q,P,D,Q,s
        p_range, d_range, q_range, P_range, D_range, Q_range, s=best_parameters_auto_arima(train_data)
        #--- Genera todas las combinaciones posibles de hiperparámetros para el modelo SARIMAX.
        param_grid = generate_param_grid(p_range, d_range, q_range, P_range, D_range, Q_range, s)

        #Evalúa todos los modelos SARIMAX generados a partir de un param_grid y selecciona el mejor modelo según el MAE.
        best_params, best_mae = find_best_sarimax_params(param_grid, train_data, test_data)

        #--- Ajusta y evalúa un modelo SARIMAX con parámetros específicos para la serie temporal, 
        #    calculando el error medio absoluto (MAE) de las predicciones.
        print("se crea forecast")
        forecast=model_sarima(best_params,serie)
        forecast = forecast.to_frame(name='Total Sales').reset_index()
        forecast.rename(columns={'index': 'Date'}, inplace=True)
     

        forecast['Country']=filtros['Country']
        forecast['Category Group']=category
        forecast['Modelo']='Sarimax'
        forecast['mae']=best_mae
       # Asegurarse de que forecast tiene las mismas columnas que df_sales_forecast
        if not set(forecast.columns).issubset(df_sales_forecast.columns):
            raise ValueError("Las columnas de forecast no coinciden con las de df_sales_forecast")

        # Concatenar resultados
        df_sales_forecast = pd.concat([df_sales_forecast, forecast], ignore_index=True)

        print(df_sales_forecast.head(-5))
        print(f'finalizo el modelo para {category}\n')
    return df_sales_forecast
print("-------------------------------------------------------------------------------")

ruta=r'/home/sebastian/Documentos/programas/Forescast Work/sales_historical_prueba.csv'
lst_category=['Pliers']
filtros={
'Brand':[''],
'Country':'Mexico',
'Category Group':lst_category
}
df_sales_and_product=historical_sales(ruta)
df_sales_forecast= forecast_data(df_sales_and_product)

generate_sarimax_by_category(df_sales_and_product,filtros,df_sales_forecast)



def  generate_sarimax_by_categoryf(df_sales_and_product,filtros,df_sales_forecast):
    """
    Genera y evalúa modelos SARIMAX para cada categoría en la lista proporcionada.

    Esta función toma un DataFrame con información de ventas y, para cada categoría especificada:
    - Filtra los datos de ventas.
    - Estacionariza la serie temporal.
    - Segmenta los datos en conjuntos de entrenamiento, validación y prueba.
    - Optimiza los hiperparámetros para un modelo SARIMAX.
    - Evalúa los modelos generados y selecciona el mejor.
    - Ajusta el modelo final y calcula el MAE.

    Args:
        df_sales_and_product (pd.DataFrame): DataFrame con datos de ventas.
        lst_category (list): Lista de categorías para las cuales se evaluarán y ajustarán modelos SARIMAX.

    Returns:
        None: La función imprime los resultados del modelo para cada categoría. 
        Los resultados incluyen el mejor modelo y el MAE asociado.

    Notas:
        - La función supone que las columnas necesarias (`Category Group`, `Date`, `Total Sales`, etc.) están presentes en `df_sales_and_product`.
        - Los modelos se ajustan para series estacionalizadas.
        - Requiere que las funciones auxiliares (time_serie, seasonalize_series, etc.) estén correctamente implementadas.
    """
     #Ignora los mensajes de alearta al entrenar el modelo
    warnings.filterwarnings("ignore")
   
    print("inicio generate sarimax by category")
    for category in filtros['Category Group']:
        print(f'for {category}')
        serie_sales,serie=time_serie(df_sales_and_product,{'Category Group':category})

        #--- Estacionariza la serie
        #serie=seasonalize_series(serie)

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
        #param_grid = generate_param_grid(p_range, d_range, q_range, P_range, D_range, Q_range, s)

        #Evalúa todos los modelos SARIMAX generados a partir de un param_grid y selecciona el mejor modelo según el MAE.
        #best_params, best_mae = find_best_sarimax_params(param_grid, train_data, test_data)










        #--- Ajusta y evalúa un modelo SARIMAX con parámetros específicos para la serie temporal, 
        #    calculando el error medio absoluto (MAE) de las predicciones.
        '''print("se crea forecast")
        forecast=model_sarima(best_params,serie)
        forecast = forecast.to_frame(name='Total Sales').reset_index()
        forecast.rename(columns={'index': 'Date'}, inplace=True)
     

        forecast['Country']=filtros['Country']
        forecast['Category Group']=category
        forecast['Modelo']='Sarimax'
        forecast['mae']=best_mae
       # Asegurarse de que forecast tiene las mismas columnas que df_sales_forecast
        if not set(forecast.columns).issubset(df_sales_forecast.columns):
            raise ValueError("Las columnas de forecast no coinciden con las de df_sales_forecast")

        # Concatenar resultados
        df_sales_forecast = pd.concat([df_sales_forecast, forecast], ignore_index=True)

        print(df_sales_forecast.head(-5))
        print(f'finalizo el modelo para {category}\n')'''
    return df_sales_forecast
print("-------------------------------------------------------------------------------")

#ruta=r'/home/sebastian/Documentos/programas/Forescast Work/sales_historical_prueba.csv'
#lst_category=['Pliers']
#filtros={
#'Brand':[''],
#'Country':'Mexico',
#'Category Group':lst_category
#}
#df_sales_and_product=historical_sales(ruta)
#df_sales_forecast= forecast_data(df_sales_and_product)
#generate_sarimax_by_categoryf(df_sales_and_product,filtros,df_sales_forecast)