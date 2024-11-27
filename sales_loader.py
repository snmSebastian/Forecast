from packages import pd

#ruta=r'/home/sebastian/Documentos/programas/Forescast Work/Sales_History.csv'
def historical_sales(ruta):
    '''lectura del csv con la inf de venta historica:  este archivo csv es el resultado de unificar todos los xlsx de sharepoint,
      filtrando las columnas de interes para el modelo
    
    Arg: ruta con la ubicacion del archivo csv con la informacion historica de venta
    
    return: dataframe(df_SalesAndProduct) agrupando la venta mensual, organizada por data,country y brand
            y filtrando los valores positivos para realizar un pronostico de venta bruta
    '''

    df_sales_and_product=pd.read_csv(ruta,index_col=None, header=0,dtype=str)

    '''Date en formato adecuado
    Elimina espacios en los nombres del col
    Se ordena por Date Country Code Brand
    '''
    df_sales_and_product['Date']=pd.to_datetime(df_sales_and_product['Date'],format='%Y-%m-%d')
    for col in df_sales_and_product.columns:
        df_sales_and_product.rename(columns={col: col.strip()}, inplace=True)

    df_sales_and_product = df_sales_and_product.sort_values(by=['Date', 'Country Code', 'Brand'], ascending=[True, False, False])
    df_sales_and_product['Total Sales']=pd.to_numeric(df_sales_and_product['Total Sales'])
    df_sales_and_product=df_sales_and_product[df_sales_and_product['Total Sales']>0]

    print("Se ejecuto correctamenteHistoricalSales")
    print("-------------------------------------------------------------------------------\n")
    return df_sales_and_product

#df_SalesAndProduct=HistoricalSales(ruta)
#print(df_SalesAndProduct.head())
    