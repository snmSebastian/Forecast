"""
Funciones de visualización de series temporales:

1. **graph_box(serie)**: 
   Genera un boxplot para visualizar la distribución de una serie y detecta valores atípicos (outliers) 
   utilizando el rango intercuartílico (IQR). Imprime los outliers detectados.

2. **graph_line(serie)**: 
   Divide la serie temporal (original y estacionalizada) en conjuntos de entrenamiento y prueba, 
   y grafica ambas divisiones para observar su comportamiento.

3. **graph_tendence(serie_sales)**: 
   Ajusta modelos de regresión lineal para calcular y graficar la tendencia de la serie temporal 
   en su forma original y estacionalizada, mostrando las pendientes asociadas.

Estas funciones permiten analizar diferentes aspectos de una serie temporal, como su distribución, 
tendencia y comportamiento en períodos definidos.
"""

from packages import plt
from packages import np
from packages import LinearRegression

from time_series_processing import seasonalize_series
#================================================================
def graph_tendence(serie_sales):

    """
    Ajusta modelos de regresión lineal para analizar y graficar la tendencia de una serie temporal 
    en su forma original y estacionalizada. Calcula y muestra las pendientes de ambas tendencias.

    Parámetro:
    - `serie_sales` (pandas.Series): Serie sin estacionalizar
    """
    X1 = np.arange(len(serie_sales)).reshape(-1, 1)  # Índices de tiempo como variable independiente
    y1 = serie_sales.values.reshape(-1, 1)           # Ventas totales como variable dependiente
    model_serie_orginal = LinearRegression().fit(X1,y1)       # -> Ajustar el modelo lineal 
    trend1 = model_serie_orginal.predict(X1)                  # Predicción de la tendencia

    #Serie estacionalizada

    serie_estacionalizada=seasonalize_series(serie_sales)            #-> estacionariza la serie
    X2  = np.arange(len(serie_estacionalizada)).reshape(-1, 1)    # Índices de tiempo como variable independiente
    y2 = serie_estacionalizada.values.reshape(-1, 1)              # Ventas totales como variable dependiente
    model_serie_estacional = LinearRegression().fit(X2,y2)                          # Ajustar el modelo lineal
    trend2 = model_serie_estacional.predict(X2)                                     # Predicción de la tendencia 




    # Crear una figura con dos subplots en una columna
    fig, axs = plt.subplots(2, 1, figsize=(12, 12))  # Ajusta el tamaño según tus necesidades

    # Primer subplot: Serie original y tendencia sin estacionalidad
    axs[0].plot(serie_sales.values, label="Serie Original", alpha=0.5)
    axs[0].plot(trend1, label="Tendencia Lineal", color="green", linewidth=2)
    axs[0].set_title("Serie de Tiempo con Tendencia Lineal Ajustada (Sin Estacionalidad)")
    axs[0].set_xlabel("Fecha")
    axs[0].set_ylabel("Ventas Totales")
    axs[0].legend()
    axs[0].grid()

    # Segundo subplot: Serie diferenciada y tendencia
    axs[1].plot(serie_estacionalizada.values, label="Serie Diferenciada", alpha=0.5)
    axs[1].plot(trend2, label="Tendencia Lineal", color="green", linewidth=2)
    axs[1].set_title("Serie de Tiempo Diferenciada con Tendencia Lineal Ajustada")
    axs[1].set_xlabel("Fecha")
    axs[1].set_ylabel("Ventas Totales")
    axs[1].legend()
    axs[1].grid()


    # Coeficiente de la tendencia
    coef_tendencia_serie_original = model_serie_orginal.coef_[0][0]
    print(f"Pendiente de la tendencia: {coef_tendencia_serie_original:.2f}")

    coef_tendencia_serie_estacional = model_serie_estacional.coef_[0][0]
    print(f"Pendiente de la tendencia: {coef_tendencia_serie_estacional:.2f}")
    print("Se ejecuto correctamente: graph_tendence")

#=========================================================================

def graph_line(serie):
    """
    graph_line(serie)

    Divide la serie temporal original y estacionalizada en conjuntos de entrenamiento y prueba, 
    y grafica ambas divisiones para visualizar su comportamiento.

    Parámetro:
    - `serie` (pandas.Series): Serie sin estacionalizar.


    """
    num_reg=int(len(serie)*0.5)
    data_train=serie[:num_reg]
    data_test=serie[num_reg-1:]

    #Serie estacionalizada
    serie_estacional=seasonalize_series(serie)
    num_reg2=int(len(serie_estacional)*0.5)
    data_train2=serie_estacional[:num_reg2]
    data_test2=serie_estacional[num_reg2-1:]

    
    fig, ax = plt.subplots(figsize=(7, 3))
    data_train.plot(ax=ax, label='train', marker='o')  # Agregamos marker='o'
    data_test.plot(ax=ax, label='test', marker='o')  # Agregamos marker='o'
    ax.set_title('Serie original')
    ax.legend()

    fig, ax = plt.subplots(figsize=(7, 3))
    data_train2.plot(ax=ax, label='train', marker='o')  # Agregamos marker='o'
    data_test2.plot(ax=ax, label='test', marker='o')  # Agregamos marker='o'
    ax.set_title('Serie estacionariazada')
    ax.legend()

    plt.show()
    print("Se ejecuto correctamente: graph_line")

#====================================================================
def graph_box(serie):
    """
    graph_box(serie)

    Genera un boxplot para visualizar la distribución de la serie y detecta valores atípicos (outliers) 
    usando el rango intercuartílico (IQR). Imprime los outliers detectados.

    Parámetro:
    - `serie` (pandas.Series): Serie de datos a analizar.
    """
    # Create a boxplot and extract outlier information
    plt.figure(figsize=(8, 6))
    plt.boxplot(serie)
    plt.title('Boxplot de Ventas Mensuales')
    plt.ylabel('Ventas')
    plt.show()

    # Calculate quartiles and IQR
    Q1 = serie.quantile(0.25)
    Q3 = serie.quantile(0.75)
    IQR = Q3 - Q1

    # Define outlier thresholds
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # Identify outliers
    outliers = serie[(serie < lower_bound) | (serie > upper_bound)]

    print("Valores Atípicos (Outliers):\n")
    print(outliers)
    print("Se ejecuto correctamente: graph_box")    