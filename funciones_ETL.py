
# Tratamiento de datos
# -----------------------------------------------------------------------
import pandas as pd
import numpy as np

# Imputación de nulos usando métodos avanzados estadísticos
# -----------------------------------------------------------------------
from sklearn.impute import SimpleImputer
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.impute import KNNImputer

# Librerías de visualización
# -----------------------------------------------------------------------
import seaborn as sns
import matplotlib.pyplot as plt

# 1. Lectura datos
# -----------------------------------------------------------------------

def lectura_datos (ruta_archivo):
    # Configuro para que me muestre el máximo número de columnas
    pd.set_option('display.max_columns', None) 
    # Fijo las condiciones de lectura sefún el tipo de archivo
    if ruta_archivo.endswith('.csv'):
        df = pd.read_csv(ruta_archivo)
    elif ruta_archivo.endswith('.xlsx') or ruta_archivo.endswith('.xls'):
        df = pd.read_excel(ruta_archivo)
    elif ruta_archivo.endswith('.json'):
        df = pd.read_json(ruta_archivo)
    else:
        raise ValueError("❌ Formato no soportado. Usa .csv, .xlsx, .xls o .json") # Cubro el caso de que haya formatos diferentes  
    
    # Muestro las primeras filas para comprobar que se ha abierto correctamente
    print(f'📄 El DataFrame obtenido desde {ruta_archivo}')
    print(df.head())
    # Retornar el DataFrame para más adelante
    return df

# 2. Exploración datos
# -----------------------------------------------------------------------

def exploracion_datos (df):
    # Array que me da info del nº de filas y columnas
    print('📐 Dimensiones del DataFrame:', df.shape)
    print('-----------------------------------------')
    # Lista de nombres de columnas
    print('🧾El DataFrame tiene las siguientes columnas', df.columns.tolist())
    print('-----------------------------------------') 
    # Información general del DataFrame
    print('🧠La información que podemos obtener de este DataFrame')
    try: 
        df.info()
    except Exception as e:
        print(f"❌ Error al obtener info(): {e}")
    print('-----------------------------------------') 
   # Tipos de datos
    print('🔢Los tipos de datos son')
    print(df.dtypes)

def resumen_general(df):
    # Resumen para ver rápidamente los puntos más importantes del df
    print("📊 Resumen general del DataFrame")
    print(f"➡️ Filas: {df.shape[0]}, Columnas: {df.shape[1]}")
    print("\n🔢 Tipos de datos:")
    print(df.dtypes)
    print("\n❔ Valores nulos:")
    print(df.isnull().sum())
    print("\n🔁 Valores únicos:")
    print(df.nunique())


# 3. Estandarizacion de nombres de variables y transformación tipo datos
# -----------------------------------------------------------------------

# df.columns = df.columns.str.lower()        Minúsculas
# df.columns = df.columns.str.strip()        Quitar espacios
# df.columns = df.columns.str.replace(" ", "_")  Reemplazar espacios con "_"

def transformacion_datos(df, columna, tipo):
    # Ver tipos actuales
    print('Los tipos de datos son')
    print(df.dtypes)
    # Cambio el tipo de dato
    print(f"🔁 Transformando columna '{columna}' a tipo {tipo}")
    df[columna] = df[columna].astype(tipo)
    # Retornar el  df para más adelante
    return df


# 4. Identificación y gestión de nulos
# -----------------------------------------------------------------------

def nulos_totales (df):
    # Conteo de nulos por columna
    print("📉 Nulos por columna:")
    print(df.isnull().sum()) 
    print('-----------------------------') 
    # Porcentaje de nulos por columna
    print("\n📊 Porcentaje de nulos:")
    nulos = df.isnull().sum()/df.shape[0]*100
    # Variables que tienen algún nulo
    nulos = nulos[nulos > 0]
    # Ordenados de menor a mayor
    print(nulos.sort_values(ascending=False))
    print('------------------------------')
    # Columnas con tipo object que tienen al menos un nulo
    columnas_obj = [col for col in df.select_dtypes(include=['object', 'bool']).columns if df[col].isna().sum() > 0]
    # Columnas con tipo float/int o int que tienen al menos un nulo
    columnas_num = [col for col in df.select_dtypes(include=['float64', 'int64']).columns if df[col].isna().sum() > 0]
    # Columnas con tipo bool que tienen al menos un nulo
    columnas_bool = [col for col in df.select_dtypes(include=['bool']).columns if df[col].isna().sum() > 0]
    print('------------------------------')
    print("🧾 Columnas object con nulos:", columnas_obj)
    print("🔢 Columnas numéricas con nulos:", columnas_num)
    print("🆗 Columnas numéricas con nulos:", columnas_bool)

def nulos_objeto(df):
    # Columnas con tipo object tienen al menos un nulo
    print("🧾Las columnas objeto con nulos")
    columnas_obj = [col for col in df.select_dtypes(include=['object']).columns if df[col].isna().sum() > 0]
    print(columnas_obj)
    # Proporción de valores entre cada categoría de las variables categóricas
    for col in columnas_obj:
        print(f"📊 Distribución de '{col}':")
        display(df[col].value_counts() / df.shape[0])  # display es una función utilizada para mostrar objetos de manera más legible en Jupyter Notebooks o entornos similares. 
        print("----------------------------")

def nulos_numericos(df):
    # Columnas con tipo object tienen al menos un nulo
    print("🔢Las columnas numéricas con nulos")
    columnas_num = [col for col in df.select_dtypes(include=['float64', 'int64']).columns if df[col].isna().sum() > 0]
    print(columnas_num)
    print('📈La distribución de las categorías para cada una de ellas')
    for col in list(columnas_num):
        plt.figure(figsize=(8, 5))
        plt.hist(df[col].dropna(), bins=30, color='skyblue', edgecolor='black')
        plt.title(f'Histograma de {col}')
        plt.xlabel(col)
        plt.ylabel('Frecuencia')
        plt.show()

def nulos_bool(df):
    # Columnas con tipo bool tienen al menos un nulo
    print("🆗Las columnas objeto con nulos")
    columnas_bool = [col for col in df.select_dtypes(include=['bool']).columns if df[col].isna().sum() > 0]
    print(columnas_bool)
    # Proporción de valores entre cada categoría de las variables bool
    for col in columnas_bool:
        print(f"📊 Distribución de '{col}':")
        display(df[col].value_counts() / df.shape[0])  # display es una función utilizada para mostrar bool de manera más legible en Jupyter Notebooks o entornos similares. 
        print("----------------------------")

def imputar_nulos_objetos(df, columnas, metodo='moda', nueva_categoria='Unknown'):
    # Cubro los errores que puedan generarse si no extisten o no son del tipo adecuado
    for col in columnas:
        if col not in df.columns:
            print(f"❌La columna '{col}' no existe en el DataFrame.")
            continue

        if df[col].dtype != 'object':
            print(f"⚠️'{col}' no es de tipo object. Se omite.")
            continue
        # Según el método de imputqación que haya decidido y cubro los errores que se peudan generar
        if metodo == 'moda':
            try:
                moda_col = df[col].mode(dropna=True)[0]
                df[col] = df[col].fillna(moda_col)
                print(f"✅'{col}': imputada con la moda → '{moda_col}'")
            except IndexError:
                print(f"❌'{col}': no se pudo calcular la moda (columna vacía).")
        elif metodo == 'nueva_categoria':
            df[col] = df[col].fillna(nueva_categoria)
            print(f"✅'{col}': imputada con nueva categoría → '{nueva_categoria}'")
        else:
            print(f"⚠️Método no reconocido: '{metodo}' (usa 'moda' o 'nueva_categoria')")

    return df

def imputar_nulos_numericos(df, columnas, metodo='mediana'):
    # Cubro los errores que puedan generarse si no extisten o no son del tipo adecuado
    for col in columnas:
        if col not in df.columns:
            print(f"❌ La columna '{col}' no existe en el DataFrame.")
            continue
        
        if not pd.api.types.is_numeric_dtype(df[col]):
            print(f"⚠️'{col}' no es numérica. Se omite.")
            continue
        # Según el método de imputación que haya decidido y cubro los errores que se puedan generar
        if metodo == 'moda':
            try:
                moda_col = df[col].mode(dropna=True)[0]
                df[col] = df[col].fillna(moda_col)
                print(f"✅'{col}': imputada con la moda → {moda_col}")
            except IndexError:
                print(f"❌'{col}': no se pudo calcular la moda (columna vacía).")
        elif metodo == 'mediana':
            mediana_col = df[col].median()
            df[col] = df[col].fillna(mediana_col)
            print(f"✅'{col}': imputada con la mediana → {mediana_col}")
        else:
            print(f"⚠️ Método no reconocido: '{metodo}' (usa 'moda' o 'mediana')")

    return df

def imputar_nulos_bool(df, columnas, metodo='moda', nueva_categoria='Unknown'):
    # Cubro los errores que puedan generarse si no extisten o no son del tipo adecuado
    for col in columnas:
        if col not in df.columns:
            print(f"❌La columna '{col}' no existe en el DataFrame.")
            continue

        if df[col].dtype != 'bool':
            print(f"⚠️'{col}' no es de tipo bool. Se omite.")
            continue
        # Según el método de imputqación que haya decidido y cubro los errores que se peudan generar
        if metodo == 'moda':
            try:
                moda_col = df[col].mode(dropna=True)[0]
                df[col] = df[col].fillna(moda_col)
                print(f"✅'{col}': imputada con la moda → '{moda_col}'")
            except IndexError:
                print(f"❌'{col}': no se pudo calcular la moda (columna vacía).")
        elif metodo == 'nueva_categoria':
            df[col] = df[col].fillna(nueva_categoria)
            print(f"✅'{col}': imputada con nueva categoría → '{nueva_categoria}'")
        else:
            print(f"⚠️Método no reconocido: '{metodo}' (usa 'moda' o 'nueva_categoria')")

    return df


# 5. Identificación y gestión de duplicados
# -----------------------------------------------------------------------

def duplicados (df, subset=None, eliminar=True):    
    try:
        # Busco duplicados según subset
        dups = df[df.duplicated(subset=subset)]

        if dups.empty:
            print("✅ No se encontraron duplicados.")
        else:
            print(f"🔁 Se encontraron {dups.shape[0]} filas duplicadas:")
            print(dups)

        # Elimino duplicados si lo especifíco (eliminar= True)
        if eliminar:
            df_sin_duplicados = df.drop_duplicates(subset=subset).copy()
            print("🧹 Duplicados eliminados del DataFrame.")
        else:
            df_sin_duplicados = df.copy()

        return dups, df_sin_duplicados
    # Cubro los posibles errores
    except Exception as e:
        print(f"❌ Error al buscar duplicados: {e}")
        return None, df

# 6. Limpieza y Transformación Dependiendo de Resultado Anterior
# -----------------------------------------------------------------------
# Quitar espacios
# df['col'] = df['col'].str.strip()    
# Pasar a minúsculas    
# df['col'] = df['col'].str.lower()
# Reemplazo de valores        
# df['col'].replace("antiguo", "nuevo")
# Eliminar columna innecesarias   
def eliminar_columnas (df, columnas):
    for col in columnas:
        if col in df.columns:
            df.drop(col, axis=1, inplace=True)
        # Por si no existe ya esa columna
        else:
            print(f"⚠️ La columna '{col}' no existe.")
    return df


# 7. Análisis exploratorio básico
# -----------------------------------------------------------------------

def estadisticas_numericas (df):
    columnas_num = df.select_dtypes(include=['int', 'float']).columns
    for col in columnas_num:
        if df[col].dtype == 'int' or df[col].dtype == 'float':
            print(f"📋Frecuencias para columna numérica '{col}':")
            print("--------------------------")
        else:
            print(f"⚠️'{col}' no es de tipo numérico. Se omite.")
            continue

def frecuencias_categoricas(df):
    columnas_obj = df.select_dtypes(include=['object', 'category']).columns
    for col in columnas_obj:
        if df[col].dtype == 'object' or df[col].dtype == 'category':
            print(f"📋Frecuencias para columna objeto '{col}':")
            print(df[col].value_counts())
            print("--------------------------")
        else:
            print(f"⚠️'{col}' no es de tipo objeto. Se omite.")
            continue

def valores_unicos(df):
    for col in df.columns:
        num_unicos = df[col].nunique()
        print(f"🔸{col}: {num_unicos} valores únicos")
        print('Estos valores unicos son')
        print(df[col].unique())
        print("----------------------------")

def visualizar_distribuciones(df, columnas=None):
    if columnas is None:
        columnas = df.select_dtypes(include=['float64', 'int64']).columns
    for col in columnas:
        plt.figure(figsize=(8, 5))
        sns.histplot(df[col].dropna(), kde=True, bins=30, color='skyblue')
        plt.title(f'📈 Distribución de {col}')
        plt.xlabel(col)
        plt.ylabel('Frecuencia')
        plt.show()

# 8. Guardar
# -----------------------------------------------------------------------

def guardar_df(df, nombre_archivo, formato='csv'):
    try:
        if formato == 'csv':
            df.to_csv(nombre_archivo, index=False)
        elif formato == 'excel':
            df.to_excel(nombre_archivo, index=False)
        else:
            print("❌ Formato no soportado (usa 'csv' o excel').")
            return
        print(f"✅ DataFrame guardado como {nombre_archivo}")
    except Exception as e:
        print(f"❌ Error al guardar archivo: {e}")