#df_sales_and_product=historical_sales(ruta)

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