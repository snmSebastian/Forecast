#===========================
#-- Paquetes
#===========================
from packages import pd

#  ruta del archivo CSV principal que contiene los datos históricos.
ruta_csv=r'/home/sebastian/Documentos/programas/Forescast Work/sales_historical.csv'

#  ruta para guardar el archivo CSV filtrado.
ruta_csv_prueba=r'/home/sebastian/Documentos/programas/Forescast Work/sales_historical_prueba.csv'



# lista con las categorías que se desean filtrar en los datos.
lst_category=['Pliers','Clamps','Hardlines']
lst_sbu=['ANF', 'BDK', 'FAS', 'HTS', 'OPG', 'OTH', 'PPT', 'PSD', 'PTA','SFW', 'TRD']
#=====================================================
#--- Filtrar sales por category group or/and sbu
#=====================================================
def csv_prueba(ruta_csv,lst_category):
    '''Crea un csv filtrando por los elementos de Category Group
    Arg: ruta_csv: ruta del archivo CSV principal que contiene los datos históricos
         lst_category: lista con las categorías que se desean filtrar en los datos.
    Out: df_prueba: csv con la data filtrada
    '''
    df_prueba=pd.read_csv(ruta_csv,index_col=None, header=0,dtype=str)
    df_prueba=df_prueba[df_prueba['Category Group'].isin( lst_category)]
    df_prueba.to_csv(ruta_csv_prueba)
    return df_prueba


#csv_prueba(ruta_csv,lst_category)


#===================================================
#---- Devoluciones
#===================================================
def devolucion(df_sales_and_product,year):

    """
    Analiza el porcentaje de registros que corresponden a devoluciones en un año específico
    y en el conjunto completo de datos. Esto permite evaluar la factibilidad de imputar
    las devoluciones en las series temporales.

    Args:
        df_sales_and_product (pd.DataFrame): DataFrame con columnas 'Date' y 'Total Sales'.
        año (int): Año para analizar las devoluciones.

    Returns:
        None
    """


    # Filtrar datos para el año proporcionado   
    df_year = df_sales_and_product[['Date', 'Total Sales']][df_sales_and_product['Date'].dt.year == year]

    # Calcular estadísticas
    num_reg = len(df_year)
    num_devoluciones = len(df_year[df_year['Total Sales'] < 0])
    venta = df_year['Total Sales'].sum()
    venta_devolucion = df_year[df_year['Total Sales'] < 0]['Total Sales'].sum()
    venta_NoDevolucion = venta - venta_devolucion

    # Imprimir resultados para el año
    print(f'total registros {year}: {num_reg}')
    print(f'num devoluciones {year}: {num_devoluciones}')
    print(f'% devoluciones: {num_devoluciones/num_reg:.3%}')
    print(f'venta total año {year}: {venta}')
    print(f'venta con devoluciones {year}: {venta_devolucion}')
    print(f'venta sin devoluciones {year}: {venta_NoDevolucion}')
    print(f'%venta devolucion: {venta_devolucion/venta:.3%}')
    print(f'%venta sin devolucion: {venta_NoDevolucion/venta:.3%}')


    # -------------------------------
    # Análisis global (todos los años)
    # -------------------------------

    # Calcular estadísticas globales
    df_SalesInf=df_sales_and_product[['Date','Total Sales']]
    num_reg=len(df_SalesInf)
    num_dev=len(df_SalesInf[df_SalesInf['Total Sales']<0])
    venta=df_SalesInf['Total Sales'].sum()
    venta_Nodevolucion=df_SalesInf[df_SalesInf['Total Sales'] >= 0]['Total Sales'].sum()
    venta_devolucin=venta-venta_Nodevolucion
    print("*------------------------\n")
    print(f'num registros: {num_reg}')
    print(f'num dev:{num_dev}')
    print(f'venta total: {venta}')
    print(f'% dev:{num_dev/num_reg:.3%}')
    print(f'% No dev:{(num_reg-num_dev)/num_reg:.3%}')
    print(f'venta sin devolucion: {venta_Nodevolucion}')
    print(f'venta devolucion: {venta_devolucin}')
    print(f'% venta sin devolucion: {venta_Nodevolucion/venta:.3%}')
    print(f'%venta con devolucion:{venta_devolucin/venta:.3%}')  
  
    print("\nSe ejecuto correctamente: devolucion")