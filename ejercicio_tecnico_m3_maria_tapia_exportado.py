# %%
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

# Librerías de funciones creadas
# -----------------------------------------------------------------------
import funciones_ETL_II as etl

# Configuración
# -----------------------------------------------------------------------
pd.set_option('display.max_columns', None)

# %%
actividad= etl.lectura_datos('Customer_Flight_Activity.csv')
perfil= etl.lectura_datos('Customer_Loyalty_History.csv')
print('=====================================================================================')
etl.exploracion_datos(actividad, nombre= 'Customer_Flight_Activity')
etl.exploracion_datos(perfil, nombre= 'Customer_Loyalty_History')
print('=====================================================================================')
etl.resumen_general(actividad, nombre= 'Customer_Flight_Activity')
etl.resumen_general(perfil, nombre= 'Customer_Loyalty_History')
print('=====================================================================================')
etl.valores_unicos(actividad, nombre= 'Customer_Flight_Activity')
etl.valores_unicos(perfil, nombre= 'Customer_Loyalty_History')
print('=====================================================================================')
perfil.loc[perfil['Salary'] < 0, 'Salary'] *= -1 # Cambio los salarios que están en negativo ya que no son valores lógico
print('=====================================================================================')
etl.nulos_totales(actividad, nombre= 'Customer_Flight_Activity')
etl.nulos_totales(perfil, nombre= 'Customer_Loyalty_History') # Solo encuentro nulos en este df
etl.nulos_numericos(perfil) # Solo trato los nulos de Salary porque los de Cancellation Year/Month suponen que siguen activos (una pista es que son el mismo número de nulos) 
etl.imputar_nulos_numericos(perfil, ['Salary'], metodo= 'media') # Imputo por la media ya que hay bajo porcentaje y el perfil es simétrico
print('=====================================================================================')
etl.duplicados_columnas(actividad, nombre= 'Customer_Flight_Activity')
etl.duplicados_columnas(perfil, nombre= 'Customer_Loyalty_History')
perfil= etl.eliminar_duplicados(perfil, columnas= ['Country'], nombre= 'Customer_Loyalty_History') # Elimino la columna Country porque es igual para todos, Canadá
print('=====================================================================================')
etl.transformacion_datos(perfil, columna= ['Gender', 'Enrollment Type', 'Education', 'Marital Status', 'Loyalty Card'], tipo= 'category', nombre= 'Customer_Loyalty_History') # Los datos de estas columnas pueden categorizarse, hay poca variabilidad entre los clientes
print(f'💭 Transformando las columnas ''Cancellation Year'' y ''Cancellation Month'' en ''Customer_Loyalty_History'' a tipo int')
perfil['Cancellation Year'] = perfil['Cancellation Year'].astype('Int64') # Transformo esta columna en número entero en el formato que soporta los NaN
perfil['Cancellation Month'] = perfil['Cancellation Month'].astype('Int64') # Transformo esta columna en número entero en el formato que soporta los NaN
perfil.dtypes
print('=====================================================================================')
print(f'💭 Uniendo todos los datos en un único DataFrame Customer Info...' )
customer_info= perfil.merge(actividad, how='left', on='Loyalty Number') # Uno al df perfil el df actividad con un left_join ya que quiero toda la información de los clientes, tengan o no vuelos, a través de Loyalty Number
# Exploro toda la información del df nuevo para confirmar que todo es coherente según la limpieza que he hecho
etl.exploracion_datos(customer_info, nombre= 'Customer_Info')
etl.resumen_general(customer_info, nombre= 'Customer_Info')
# Creo diccionario para aplicar mis funciones de estadisticas básicas a los 3 df
data = {
    'Customer_Flight_Activity': actividad,
    'Customer_Loyalty_History': perfil,
    'Customer_Info': customer_info
}
print(f'💭 Creando estadísticas básicas de los DataFrames...')
for nombre_df, df in data.items():
    etl.estadisticas_numericas(df, nombre= nombre_df)

for nombre_df, df in data.items():
    etl.frecuencias_categoricas(df, nombre= nombre_df)
print('=====================================================================================')
# Creo diccionario para aplicar mis función de guardado a los 3 df
data = {
    'Customer_Flight_Activity_limpio': actividad,
    'Customer_Loyalty_History_limpio': perfil,
    'Customer_Info': customer_info
}
print(f'💭 Guardando todos los datos...')
for nombre_df, df in data.items():
    etl.guardar_df(df, nombre_archivo= nombre_df, formato= 'csv')



# %%
# 1. ¿Cómo se distribuye la cantidad de vuelos reservados por mes durante el año?
# Gráfico de barras agrupando por años y meses contando los vuelos realizados por cliente. Los datos puedo obtenerlos del df Customer_Flight_Activity_limpio (actividad)
datos_anuales= actividad.groupby(['Year', 'Month'])['Flights Booked'].sum().reset_index()

plt.figure(figsize=(8,5))
sns.barplot(data= datos_anuales, 
            x= 'Month', 
            y= 'Flights Booked', 
            hue='Year', 
            palette= ['green', 'red'])
plt.title('Vuelos reservados por mes durante los años')
plt.xlabel('Mes')
plt.ylabel('Número de vuelos reservados')
plt.legend(title='Año')
plt.show()

# Con el gráfico de barras podemos observar que los meses en los que más vuelos se reservan son Junio y Julio (verano), independientemente del año. 
# En Agosto y Diciembre hay gran actividad también porque son periodos típicamente vacacionales.
# En el año 2018 se han reservado más vuelos que en 2017 durante todos los meses.


# %%
# 2. ¿Existe una relación entre la distancia de los vuelos y los puntos acumulados por los cliente?
# Con un regplot puedo saber si las variables se correlacionan o no. Uso los datos del df Customer_Flight_Activity_limpio (actividad) agrupandolos por clientes
datos_clientes= actividad.groupby('Loyalty Number')[['Distance', 'Points Accumulated']].sum().reset_index()
sns.regplot(x = 'Distance', 
            y = 'Points Accumulated', 
            data = datos_clientes, 
            marker = 'o', 
            line_kws = {"color": "black", "linewidth": 1}, 
            scatter_kws = {"color": "blue", "s": 1}
            )


plt.xlabel("Distancia recorrida")
plt.ylabel("Puntos acumulados")


plt.title("Relación entre la distancia recorrida y los puntso acumulados por cliente")


plt.gca().spines['right'].set_visible(False) 
plt.gca().spines["top"].set_visible(False)

# Con este gráfico podemos confirmar que los puntos acumulados por los clientes aumentan en función de las millas recorridas, por lo que ambas tienen relación.

# %%
# 3. ¿Cuál es la distribución de los clientes por provincia o estado?

# El sns.countplot() cuenta el nº de clientes por provincia. Uso el df Customer_Loyalty_History_limpio (perfil) y de ahí saco el conteo por provincias.

# Contar los valores y ordenarlos de mayor a menor
orden_provincia = perfil['Province'].value_counts().index

sns.countplot(data= perfil, 
              x= 'Province',
              order= orden_provincia,
             color= 'violet')

# Girar las etiquetas del eje X
plt.xticks(rotation=45)

plt.xlabel('Provincia')
plt.ylabel('Nº clientes')

plt.show()

# En el gráfico podemos observar que Ontario es el estado/provincia con mayor nº clientes, es el estado donde se ecuentra la ciudad con más habitantes, Toronto, y la capital, Ottawa.
# Prince Eward Island es la que menor ya que es pequeña y poco poblada, tiene sentido
# Despúes de Ontario, las 3 provincias que le siguen también tienen un gran n1 de habitantes con lo cuál es normal que también tengan más clientes
# El resto son centros culturales/estratégicos importantes en Canadá

# %%
# 4. ¿Cómo se compara el salario promedio entre los diferentes niveles educativos de los clientes?
# En este caso uso un barplot para ver facilmente que grupo tiene mayor/menor salario. Hay que agruparlos por eduación y sacar la media de salario desde el df Customer_Loyalty_History_limpio (perfil)
# También puedo añadir un boxplot para entender mejor la distribución de los datos por categoría.

fig, axes = plt.subplots(1, 2, figsize=(16, 6), sharey=True)

# Barplot

salario_medio = perfil.groupby('Education', observed= True)['Salary'].mean().reset_index()

sns.barplot(data=salario_medio, 
            x='Education', 
            y='Salary', 
            hue= 'Education',
            palette='pastel',
            legend= False,
            ax= axes[0])

axes[0].set_title('Barplot: Salario promedio por nivel educativo')
axes[0].tick_params(axis='x', rotation=45)

# Boxplot

medias = perfil.groupby('Education', observed= True)['Salary'].mean()
medianas = perfil.groupby('Education', observed= True)['Salary'].median()

sns.boxplot(x= 'Education', 
                 y= 'Salary', 
                 hue= 'Education',
                 data= perfil,
                 palette= 'pastel',
                 legend= False,
                 ax= axes[1])

# Añadir líneas para media y mediana en cada nivel educativo
for i, nivel in enumerate(medias.index):
    axes[1].plot([i - 0.3, i + 0.3], [medias[nivel], medias[nivel]], color='red', linewidth=2, label='Media' if i==0 else "")
    axes[1].plot([i - 0.3, i + 0.3], [medianas[nivel], medianas[nivel]], color='green', linewidth=2, linestyle='dashed', label='Mediana' if i==0 else "")

axes[1].set_title('Boxplot: Salario por nivel educativo ')
axes[1].legend()
axes[0].tick_params(axis='x', rotation=45)

# Muestra todo
plt.tight_layout()
plt.show()


# El salario medio es bastante similar para los niveles educativos más bajos. Para Doctor y Master (los más altos) hay bastante diferencia.
# En el bnoxplot podemos ver las dispersión de los datos, lo que permite hacernos a la idea de la representatividad de la media. 
    # En el caso de Doctor están más dispersos pero se ajustan bastante a la mediana (si fueran muy distintas sería más veráz la mediana debido a la dispersión).
    # College tiene la menor dispersión de datos.
# High School or below son los clientes con salarios más bajos, como cabe esperar.

# %%
# 5. ¿Cuál es la proporción de clientes con diferentes tipos de tarjetas de fidelidad?
# Para poder comprarar proporciones utilizaré un pie chart. Hay que contar la cantidad de por tipos de tarjeta desde el df Customer_Loyalty_History_limpio (perfil)
fidelidad= perfil['Loyalty Card'].value_counts()

plt.figure(figsize=(5, 3))
plt.pie(fidelidad, 
        labels=fidelidad.index, 
        autopct='%1.1f%%', 
        startangle=90, 
        colors=sns.color_palette('Set2'))
plt.title('Proporción de tipos de tarjetas de fidelidad')
plt.axis('equal')
plt.show()

# El plan Star es el que mayor cantidad de clientes presenta, el Aurora el que menos.
# No existe mucha diferenecia de % de clientes de uno a otro

# %%
# 6. ¿Cómo se distribuyen los clientes según su estado civil y género?
# Uso un barplot creando una tabla de frecuencias, agrupo por Marital Status y Gender. Los datos los saco de df Customer_Loyalty_History_limpio (perfil) 

tabla = perfil.groupby(['Marital Status', 'Gender'], observed= True).size().reset_index(name='count')

plt.figure(figsize=(6, 4))
sns.barplot(data=tabla, 
            x='Marital Status', 
            y='count', hue='Gender', 
            palette='bright')

plt.title('Distribución de clientes según Estado Civil y Género')
plt.ylabel('Número de clientes')
plt.xlabel('Estado Civil')
plt.xticks(rotation=45)
plt.legend(title='Género')
plt.tight_layout()
plt.show()

# Lo que podemos deducir de este gráfico es que para los clientes casados son los mayoritarios y hay la misma cantidad de hombres y mujeres. Puede que el ambos miembros de la pareja tengan la tarjeta.
# En el caso de divorciados (menor número), hay más mujeres. Para los solteros tambíen hay más mujeres. Para ambos casos no exiten muchas diferencias de género.

# %%
# ------- BONUS ------- #
# Como los clientes (Loyalty Number) aparecen más de una vez, tiene más sentido sumar todos sus registros ya que Flight Booked se refiere al mes.
vuelos_cliente= customer_info.groupby(['Loyalty Number', 'Education'], observed= True)['Flights Booked'].sum().reset_index()
# Selecciono las dos columnas, Flight Booked y Education del df customer_info.
filtro= vuelos_cliente[['Flights Booked', 'Education']]
filtro.head()
# El análisis estadítico de Flights Booked filtrando por Education.
estadisticas= filtro.groupby('Education', observed= True)['Flights Booked'].describe().T
estadisticas
# El máximo de registros se encuentra en Bachelor y el que menos tiene es Master. Cuantos más datos tengan (Bacherlor, College) más confiables serán las estadísticas.
# El mínimo de vuelos para todos los casos es 0. 
# Para el nivel Bachelor se obtienen las máximas reservas. 
# La media es similar en todos los casos.
# La desviación estándar (std) es similar para todos los niveles. Se puede deducir una dispersión similar, pero el volumen de datos no es el mismo para todos los niveles, hay que estudiarlo más en detalle.
# Los percentiles (25%, 50%, 75%) también se mueven en rangos bastantes similares, por lo que se puede deducir que la distribución de los datos para todos los niveles es parecida.

# %%
# Prueba de hipótesis: ¿Existe diferencia significativa entre los vuelos reservados por nivel educativo?
    # Independecia observaciones
    # Comprobación distribución normal de los datos (nivel significancia 0.05) --> H0: siguen distribución esperada // H1: no siguen distribución esperada
    
from scipy.stats import shapiro, kstest

# Función para comprobar la normalidad de las muestras por nivel educativo 
def check_normalidad(data):
        """
        Realiza la prueba de normalidad utilizando Shapiro-Wilk o Kolmogorov-Smirnov,
        dependiendo del tamaño de la muestra.
        
        Parámetros:
        - data: lista o array de datos numéricos
        
        Retorna:
        - Diccionario con el tipo de prueba, p-value y decisión sobre H0
        """
        n = len(data)
        
        # Condición para elegir la prueba
        if n <= 5000:
            # Usar Shapiro-Wilk para muestras pequeñas y medianas
            test_name = "Shapiro-Wilk"
            stat, p_value = shapiro(data)
        else:
            # Usar Kolmogorov-Smirnov para muestras grandes
            test_name = "Kolmogorov-Smirnov"
            stat, p_value = kstest(data, 'norm')

        # Decisión sobre la hipótesis nula
        if p_value > 0.05:
            decision = "✅ No se rechaza H0: Los datos parecen seguir una distribución normal."
        else:
            decision = "❌ Se rechaza H0: Los datos no siguen una distribución normal."
        
        # Retornar los resultados
        return {
            "🧪 Prueba": test_name,
            "📌 Estadístico": stat,
            "📌 p-value": p_value,
            "⚖️ Decisión": decision
        }    

# Creo diccionario para visualizar los resultados más tarde
resultados_norm= {}
# Los datos que quiero utilizar están en el filtro que cree anteriormente. 
for nivel, grupo in filtro.groupby('Education', observed=True):
     vuelos= grupo['Flights Booked'].dropna() # Para asegurarme de que no quedan nulos (si no el test no funciona), los elimino
     resultado= check_normalidad(vuelos) # Realizo la prueba de normalidad
     resultados_norm[nivel]= resultado # Añado al diccionario los resultados por nivel educativo obtenidos

resultados_norm # Hay que aplicar Test no paramétricos, se rechaza la H0 en todos los casos.

# %%
# Prueba de hipótesis: ¿Existe diferencia significativa entre los vuelos reservados por nivel educativo?
    # Independecia observaciones
    # Comprobación distribución normal de los datos--> H1: no siguen distribución esperada
    # Comprobación Homogeneidad de Varianza--> Como la distribución de los datos no es normal no sería necesario realizar este test, asumo que las varianzas nos on homogéneas
    # Test a realizar--> NO PARAMÉTRICO. Kruskal-Wallis Test: Alternativa no paramétrica al ANOVA, compruebo más de dos distribuciones no normales.

# Datos para el test: kruskal(muestra 1, muestra 2, muestra 3)
from scipy.stats import kruskal
# La hipótesis a estudio: H0: No existen diferencias significativas entre la cantidad de vuelos por nivel educativo // H1: Existen diferencias significativas entre la cantidad de vuelos por nivel educativo.
# Elijo el nivel de significancia (alpha): determina si acepto o no H0 comparando el p-value obtenido en el test--> alpha= 0.05, no necesitamos un nivel muy estricto para este estudio.
# Creo los grupos de las muestras por nivel educativo dentro de lo que ya tenía filtrado antes. Elimino los posibles Na que hayn podido pasarse para que funcione.
bachelor = filtro[filtro['Education'] == 'Bachelor']['Flights Booked'].dropna().values
college = filtro[filtro['Education'] == 'College']['Flights Booked'].dropna().values
doctor = filtro[filtro['Education'] == 'Doctor']['Flights Booked'].dropna().values
high_school = filtro[filtro['Education'] == 'High School or Below']['Flights Booked'].dropna().values
master = filtro[filtro['Education'] == 'Master']['Flights Booked'].dropna().values
# Aplico la prueba a estos grupo. Acepto H0 con un nivel de significancia del 0.05?
resultado = kruskal(bachelor, college, doctor, high_school, master)
# Muestro los resultados.
print(f'📌 El valor obtenido para Estadístico H: {round(resultado.statistic, 2)}')
print(f'📌 El valor obtenido para p-value (determina si aceptamos H0): {round(resultado.pvalue, 2)}')
# Comparo el p-value con el nivel de significancia elegido, 5% (alpha= 0.05)
if resultado.pvalue < 0.05:
    print("❌ Se rechaza H0: Existen diferencias significativas en el número de vuelos reservados entre los diferentes niveles educativos.")
else:
    print("✅ No se rechaza H0: No hay diferencias significativas en el número de vuelos reservados entre los diferentes niveles educativos.")


