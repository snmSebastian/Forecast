from packages import pd

#  ruta del archivo CSV principal que contiene los datos históricos.
ruta_csv=r'/home/sebastian/Documentos/programas/Forescast Work/sales_historical.csv'

#  ruta para guardar el archivo CSV filtrado.
ruta_csv_prueba=r'/home/sebastian/Documentos/programas/Forescast Work/sales_historical_prueba.csv'

# lista con las categorías que se desean filtrar en los datos.
lst_category=['Pliers','Clamps','Hardlines']


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


csv_prueba(ruta_csv,lst_category)