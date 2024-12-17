#==========================
#-- Importacion de paquetes
#==========================

from packages import pd,glob 
from packages import pd 

#==========================
#--- Rutas de los archivos
#==========================

path_data_historica = r'C:\Users\SSN0609\OneDrive - Stanley Black & Decker\Dashboard Marketing\Sales'
path_data_product = r'C:\Users\SSN0609\OneDrive - Stanley Black & Decker\Master Data\Master Data Products Reclasif.xlsx'
path_data_country = r'C:\Users\SSN0609\OneDrive - Stanley Black & Decker\Dashboard Marketing\LAG Report\Codes _ PBI.xlsx'

#=====================================
#-- Se cargan y procesan archivos
#=====================================

#==========================
# --- Load date Sharepint
#==========================
def sales_sharepoint(path_data_historica, path_data_product, path_data_country):
    """ Función para procesar los datos de ventas desde archivos XLSX alojados en SharePoint 
    y cruzarlos con datos maestros de productos y codigo de pais.
    """
    # -------------------------------
    # 1. Leer y procesar los archivos de ventas
    # -------------------------------
    print('Inicializa lectura de xlsx de sales')
    all_files_sales = glob.glob(path_data_historica + "/*Sales*.xlsx")
    filtered_files_sales = [file for file in all_files_sales if "path" not in file]

    lst_sales = []
    for filename in filtered_files_sales:
        df = pd.read_excel(filename, index_col=None, header=0, dtype=str)
        lst_sales.append(df)
    
    df_sales = pd.concat(lst_sales, axis=0, ignore_index=True)
    print('se crea df_sales')

    # ----------------------------------------------------
    # 2. Leer el archivo maestro de productos - country y fx rate
    # ----------------------------------------------------
    print('inicializa lectura archivos xlsx')
    try:
         df_products = pd.read_excel(path_data_product, sheet_name='Master Product')
         df_country = pd.read_excel(path_data_country, sheet_name='Country Code')
         print('se cargan los archivos de products, country y fx rate')
    except Exception as e:
         print(f"Error al leer los archivos: {e}")
         return
    print('se leen los archivos xlsx')

    # -------------------------------
    # 3. Cruzar ventas con productos
    # -------------------------------
    df_sales_and_product = pd.merge(
        df_sales,
        df_products,
        how='left',
        left_on='Country Material',
        right_on='SKU',
        suffixes=('_sales', '_products')
    )
    print("se cruzo sales con products")
    print(f'len(df_sales): {len(df_sales)}')
    print(f'len(df_sales_and_product): {len(df_sales_and_product)}')

    # -------------------------------
    # 3.1. Crear columna de Date
    # -------------------------------
    dict_month = {
        'jan': '01', 'feb': '02', 'mar': '03', 'apr': '04', 'may': '05', 
        'jun': '06', 'jul': '07', 'aug': '08', 'sep': '09', 'oct': '10', 
        'nov': '11', 'dec': '12', '1': '01'
    }

    df_sales_and_product['Date'] = pd.to_datetime(
        df_sales_and_product['Fiscal Year'] + '-' + 
        df_sales_and_product['Fiscal Period'].str.lower().map(dict_month) + '-01',
        format='%Y-%m-%d'
    )
    print('se crea Date')
    # -----------------------------------------
    # 4. Cruzar sales_products con Country
    # ----------------------------------------
    df_sales_and_product['key_country'] = df_sales_and_product['Country Code'] + df_sales_and_product['Destination Country']

    df_sales_and_product = pd.merge(
       df_sales_and_product,
        df_country,
        how='left',
        left_on='key_country',
        right_on='Country Code Concat',
        suffixes=('_sales_products', '_country')
    )
    print("se cruzo sales_products con country")

        # -------------------------------
    # 4.1. Seleccionar columnas clave
    # -------------------------------
    df_sales_and_product.columns = df_sales_and_product.columns.str.strip()
    colum_sales=[
        # products
        'SKU', 'SKU Base', 'SKU Description', 'Brand', 'GPP Division Code',
        'GPP Division Reclasif', 'GPP Category Reclasif', 'GPP Portfolio',
        'SBU', 'Super SBU', 'GPP SBU', 'GPP SBU Description', 'Brand + SBU', 'Corded / Cordless', 'Category Group',
        # sales
        'Date', 'Fiscal Year', 'Fiscal Period', 'Sold-To Customer Code',
        'Total Sales', 'Total Cost', 'Units Sold',
        #Country
        'Country', 'Region'

    ]
    df_sales_and_product=df_sales_and_product[colum_sales]  
    print("se seleccionan columnas")
    # -------------------------------
    # . Limpieza final
    # -------------------------------
    df_sales_and_product = df_sales_and_product.sort_values(by=['Date', 'Country', 'Brand'], ascending=[True, False, False])
    df_sales_and_product['Total Sales'] = pd.to_numeric(df_sales_and_product['Total Sales'])
    df_sales_and_product = df_sales_and_product[df_sales_and_product['Total Sales'] > 0]
    #Se exporta csv a ruta de onedrive
    ruta_csv = r'C:\Users\SSN0609\OneDrive - Stanley Black & Decker\Dashboards LAG\Proyects\Forecast\sales_historical.csv'
    df_sales_and_product.to_csv(ruta_csv, index=False)

    print("se ejecuto correctamente sales_sharepoint")
    print("-------------------------------------------------------------------------------\n")

#sales_sharepoint(path_data_historica, path_data_product, path_data_country)


#******************************************************************

#==========================
# Load data CSV
#==========================

#ruta=r'/home/sebastian/Documentos/programas/Forescast Work/sales_historical.csv'
def historical_sales(ruta):
    """
    Carga y procesa los datos históricos de ventas desde un archivo CSV.

    Args:
        file_path (str): Ruta al archivo CSV con la información de ventas.

    Returns:
        pd.DataFrame: DataFrame con las ventas mensuales procesadas, organizadas por fecha, país y categoría.

    Notes:
        - Elimina registros con ventas negativas o nulas.
        - Convierte la columna 'Date' al formato datetime.
        - Ordena los datos por fecha, país y categoría.
    """
    #Lectura de csv
    df_sales_and_product=pd.read_csv(ruta,index_col=None, header=0,dtype=str)

    #Elimina espacios en los nombres del col
    df_sales_and_product.columns=df_sales_and_product.columns.str.strip()

    #Date en formato adecuado
    df_sales_and_product['Date']=pd.to_datetime(df_sales_and_product['Date'],format='%Y-%m-%d')
    
    #Filtra por ventas brutas
    df_sales_and_product['Total Sales']=pd.to_numeric(df_sales_and_product['Total Sales'])
    df_sales_and_product=df_sales_and_product[df_sales_and_product['Total Sales']>0]

    #Ordena por date, country and brand
    df_sales_and_product = df_sales_and_product.sort_values(
        by=['Date', 'Country', 'Brand'],
        ascending=[True, False, False])
    
    print("Se ejecuto correctamenteHistoricalSales")
    print("-------------------------------------------------------------------------------\n")
    return df_sales_and_product

#df_SalesAndProduct=HistoricalSales(ruta)
#print(df_SalesAndProduct.head())
    