from packages import pd,glob #tratamiento de dato

#paht_data_historica=r'C:\Users\SSN0609\OneDrive - Stanley Black & Decker\Dashboard Marketing\Sales'
#paht_data_product=r'C:\Users\SSN0609\OneDrive - Stanley Black & Decker\Master Data\Master Data Products Reclasif.xlsx' 

def sales_sharepoint(paht_data_historica,paht_data_product):
    

    """ Función para procesar los datos de ventas desde archivos XLSX alojados en SharePoint 
    y cruzarlos con datos maestros de productos.

    Pasos:
    1. Leer todos los archivos de ventas en la ruta especificada (`paht_data_historica`).
    2. Unificar los datos de ventas en un único DataFrame (`df_sales`).
    3. Leer el archivo maestro de productos desde la ruta especificada (`paht_data_product`).
    4. Seleccionar columnas clave de ventas y productos.
    5. Cruzar las ventas con los productos para agregar clasificaciones por SKU.
    6. Agregar una columna de fecha a partir del año fiscal y periodo fiscal.
    7. Retornar el DataFrame final procesado.

    Args:
    paht_data_historica (str): Ruta a la carpeta con archivos de ventas en formato XLSX.
    paht_data_product (str): Ruta al archivo maestro de productos en formato XLSX.

    Returns:
    pd.DataFrame: DataFrame combinado de ventas y productos.
    """
    # -------------------------------
    # 1. Leer y procesar los archivos de ventas
    # -------------------------------
    # Lista de archivos en la carpeta que contienen "Sales" en el nombre
    all_files_sales = glob.glob(paht_data_historica + "/*Sales*.xlsx")
    
    #Filtrar archivos que no contengan "path" en el nombre
    filtered_files_sales = [file for file in all_files_sales if "path" not in file]

    # Leer y unificar los datos de ventas
    lst_sales=[]
    for filename in filtered_files_sales:
        df = pd.read_excel(filename, index_col=None, header=0,dtype=str)
        lst_sales.append(df)
    
    # Concatenar los datos de ventas en un solo DataFrame
    df_sales= pd.concat(lst_sales,axis=0,ignore_index=True)

    # -------------------------------
    # 2. Leer el archivo maestro de productos
    # -------------------------------
    df_products=pd.read_excel(paht_data_product,index_col=None,header=0,dtype=str)

    # -------------------------------
    # 3. Seleccionar columnas clave
    # -------------------------------

    Columns_products=['SKU', 'SKU Base', 'SKU Description', 'Brand ', 'GPP Division Code',
    'GPP Division Reclasif', 'GPP Category Reclasif', 'GPP Portfolio ',
    'SBU', 'Super SBU', 'GPP SBU', 'GPP SBU Description']
    df_products=df_products[Columns_products]

    columns_sales=['Fiscal Year', 'Fiscal Period', 'Country Code', 
    'Sold-To Customer Code','Country Material', 'Total Sales', 'Total Cost', 'Units Sold']
    df_sales=df_sales[columns_sales]

    # -------------------------------
    # 4. Cruzar ventas con productos
    # -------------------------------

    df_sales_and_product=pd.merge(
    df_sales,
    df_products,
    how='left',
    left_on='Country Material',
    right_on='SKU'
    )

    print(f'len(df_sales): {len(df_sales)}')
    print(f'len(df_salesProdu): {len(df_sales_and_product)}')
    #-------------------------------
    #---- Date
    #-------------------------------
    dict_month = {
    'jan': '01', 'feb': '02', 'mar': '03', 'apr': '04', 'may': '05', 
    'jun': '06', 'jul': '07', 'aug': '08', 'sep': '09', 'oct': '10', 
    'nov': '11', 'dec': '12', '1': '01'
    }

    # Función para convertir año fiscal y periodo fiscal en una fecha
    def mes(row):
        month = row['Fiscal Period'].lower()
        month_num = dict_month[month]
        year = row['Fiscal Year']
        date_str = month_num + '-' + year
        return date_str

    # Aplicar la función para crear la columna 'Date'
    df_sales_and_product['Date']=df_sales_and_product.apply(mes,axis=1) 
    df_sales_and_product['Date']=pd.to_datetime(df_sales_and_product['Date'],format='%Y-%m-%d')
    #df_SalesAndProduct.head()

    # -------------------------------
    # 6. Limpieza final
    # -------------------------------
    for col in df_sales_and_product.columns:
        df_sales_and_product.rename(columns={col: col.strip()}, inplace=True)
    
    df_sales_and_product = df_sales_and_product.sort_values(by=['Date', 'Country Code', 'Brand'], ascending=[True, False, False])
    df_sales_and_product['Total Sales']=pd.to_numeric(df_sales_and_product['Total Sales'])
    df_sales_and_product=df_sales_and_product[df_sales_and_product['Total Sales']>0]
    print("se ejecuto correctamente sales_sharepoint")
    print("-------------------------------------------------------------------------------\n")

    return df_sales_and_product