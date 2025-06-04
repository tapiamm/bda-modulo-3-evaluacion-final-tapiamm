# EVALUACIÓN MÓDULO 3 


### ✈️ Análisis de Datos de Clientes y Actividad de Vuelos

Este proyecto consiste en la exploración, limpieza, visualización y análisis estadístico de un conjunto de datos de clientes pertenecientes a un programa de fidelización de vuelos. El objetivo es comprender mejor su comportamiento y características, así como responder a ciertas preguntas de negocio mediante herramientas de análisis y visualización en Python.

#### 🧰 Creación Funciones

Con el objetivo de reutilizar el código y mantener una estructura más limpia en el proyecto, se ha creado un archivo .py llamado etl_funciones.py. En él se definen funciones específicas para las tareas de Extracción, Transformación y Carga (ETL), como la limpieza de datos, tratamiento de nulos, cambio de tipos de datos, fusiones de tablas y guardar los datos en distintos formatos.

Estas funciones permiten aplicar los mismos procesos de forma eficiente en distintas etapas del análisis, especialmente en la fase exploratoria y en la preparación de datos para los análisis estadísticos posteriores.

#### 📂 Datos utilizados

Se han utilizado dos archivos CSV por separado y combinados en un único DataFrame llamado customer_info, que contiene información sobre:

* Datos demográficos de los clientes

* Su historial de vuelos

* Puntos acumulados y redimidos

* Tipo de tarjeta de fidelidad y detalles de inscripción

### 🔍 Fase 1: Exploración y Limpieza

#### 🧭 Exploración inicial

Se identificaron valores nulos en variables como año/mes de cancelación.

Se observaron registros duplicados debido a que cada cliente aparece una vez por mes.

Se realizó un análisis con info(), describe(), y value_counts() para conocer la estructura y calidad de los datos.

#### 🧹 Limpieza de datos
Se eliminaron o gestionaron los nulos según la relevancia de las columnas.

Se agruparon registros por Loyalty Number cuando fue necesario para evitar duplicados en análisis por cliente.

Se convirtieron columnas a tipos de datos más eficientes como category o Int64 para optimizar memoria y claridad.

### 📊 Fase 2: Visualización

Se realizaron diferentes visualizaciones con matplotlib y seaborn en los para responder a las siguientes preguntas de la forma más eficiente evitando duplicados.

#### 📅 ¿Cómo se distribuye la cantidad de vuelos reservados por mes?

Se agruparon los vuelos por mes del año.

Gráfico de barras para observar estacionalidad o tendencias.

#### ✈️ ¿Existe una relación entre distancia de vuelo y puntos acumulados?

Se agruparon los datos por cliente.

Se utilizó un gráfico de dispersión con regresión (regplot) para mostrar correlación positiva entre ambas variables.

#### 🗺️ ¿Cuál es la distribución de clientes por provincia?

Se consideraron clientes únicos (Loyalty Number).

Se usó countplot con orden descendente de provincias.

#### 💸 ¿Cómo varía el salario medio según el nivel educativo?

Se agruparon los salarios por nivel de educación.

Se usaron gráficos de barras y cajas para observar medias y dispersión.

#### 💳 ¿Qué proporción de clientes tiene cada tipo de tarjeta de fidelidad?

Se graficó la proporción usando pieplot agrupando por tarjeta de fidelidad.

#### ❤️ ¿Cómo se distribuyen los clientes por estado civil y género?

Gráfico de barras agrupado (hue='Gender') para comparar visualmente ambos factores.

### 🎓 BONUS: Evaluación de diferencias por educación

#### 🎯 Objetivo:

Determinar si existen diferencias significativas en el número de vuelos reservados según el nivel educativo.

#### 1️⃣ Preparación

Se agruparon los datos por Loyalty Number para sumar los vuelos mensuales por cliente.

Se filtraron únicamente las columnas Flights Booked y Education.

#### 2️⃣ Análisis descriptivo

Se calcularon la media, desviación estándar y percentiles para cada grupo educativo.

#### 3️⃣ Pruebas estadísticas

* Normalidad: Se aplicó la prueba de Shapiro-Wilk o Kolmogorov-Smirnov (según tamaño muestral) → los datos no son normales.

* Homogeneidad de varianzas: Se asumió que las varianzas no son homogéneas (los datos no son normales).

* Prueba de hipótesis: Se aplicó el test no paramétrico de Kruskal-Wallis, concluyendo que no existen diferencias significativas entre los grupos educativos en cuanto a vuelos reservados.

### 📤 Exportación

Inicialmente se realizaron todos estos pasos en Jupyter Notebook pero también se exportan a Python, para poder reutilizar este código si fuera necesario, ya que el Jupyter no esta diseñado para ello. En este caso se tuvieron que cambiar algunas funciones de ETL porque contenían código especificífico de Jupyter (display por ejemplo).

### 🧪 Conclusión

El análisis permitió identificar patrones relevantes en el comportamiento de los clientes. Además, el estudio estadístico confirmó que el nivel educativo mo influye significativamente en la cantidad de vuelos reservados. Esto puede ser relevante para estrategias de marketing. Dado que todos los niveles educativos presentan un comportamiento similar en cuanto a reservas, los recursos pueden enfocarse en otras variables más influyentes, como el tipo de tarjeta de fidelidad, la frecuencia de vuelos, el historial de puntos acumulados o el CLV (Customer Lifetime Value). Esta información ayuda a tomar decisiones más eficientes en cuanto a personalización de ofertas, fidelización y diseño de estrategias comerciales que realmente impacten en la actividad del cliente.
