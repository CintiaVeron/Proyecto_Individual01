![Logo de mi proyecto]("(th.jpg")


   
# PROYECTO INDIVIDUAL N°1

Machine Learning Operations (MLOps): Sistema de Recomendación de Videojuegos para Usuarios de Steam

## Descripción del Proyecto:

Empezamos a trabajar como Data Scientist en Steam, una plataforma multinacional de videojuegos. Steam pide que nos encarguemos de crear un sistema de recomendación de videojuegos para usuarios.

En este proyecto, trabajamos con tres conjuntos de datos en formato JSON, los cuales presentan una estructura anidada. Debemos extraer información para la creación de un sistema de recomendación a través de un proceso de ETL (Extracción, Transformación y Carga).

### Fuente de datos:

- [Dataset](https://drive.google.com/drive/folders/1HqBG2-sUkz_R3h1dZU5F2uAzpRn7BSpj): Carpeta con el archivo que requieren ser procesados, tengan en cuenta que hay datos que están anidados (un diccionario o una lista como valores en la fila).
- [Diccionario de datos](https://docs.google.com/spreadsheets/d/1-t9HLzLHIGXvliq56UE_gMaWBVTPfrlTf2D9uAtLGrk/edit?usp=drive_link): Diccionario con algunas descripciones de las columnas disponibles en el dataset.: Diccionario con algunas descripciones de las columnas disponibles en el dataset.

## Etapas de Proyecto:

1. ETL (Extracción, Transformación y Carga):

Como primer paso en el proceso de ETL, se crearon dos funciones para poder trabajar con los archivos json que tenían columnas anidadas, para hacer más eficiente el rendimiento de los recursos de la PC.

- Se descargan de manera local los archivos del dataset descripto anteriormente y con las funciones se leen los archivos 'australian_users_items.json' y 'australian_user_reviews.json'.
- En ambos casos se tratan los valores nulos, duplicados, se desanidan las columnas json (reviews e ítems) y se quitan las columnas innecesarias.
- En el caso del archivo 'output_steam_games.json', no fue necesario desanidar columnas, por lo que se procede a leer el archivo de manera convencional. De la misma manera, se eliminaron filas con valores nulos, duplicados, se modificó el formato en las columnas año de lanzamiento y precio y se dejaron las columnas necesarias para poder trabajar.
- Para finalizar se guardan los dataframes resultantes en csv, los cuales los pueden encontrar en la carpeta csv. Todos los pasos los pueden ver en el Jupyter Notebook 'ETL'.

2. EDA (Exploratory Data Analysis):

Como segundo paso hicimos un Exploratory data analysis (EDA):

- Lectura de datos: Se leyó el archivo 'output_steam_games.json' utilizando la librería Pandas en Python para cargar los datos en un DataFrame.
- Selección de columnas: Se seleccionaron columnas específicas del DataFrame, incluyendo género, nombre de la aplicación, título, año de lanzamiento, precio, ID de contenido y desarrollador.

En el archivo 'EDA' se evidencian los siguientes procesos:

- Visualización de la nube de palabras: Se creó una nube de palabras utilizando los géneros de los juegos para visualizar las categorías más comunes en el conjunto de datos.
- Identificación de outliers: Se utilizó el método del rango intercuartílico (IQR) para identificar outliers en la columna de precios del DataFrame.
- Visualización de outliers: Se creó un diagrama de caja para visualizar la distribución de los precios y identificar outliers visualmente.
- Visualización de la distribución de años de lanzamiento: Se creó un histograma para visualizar la distribución de los años de lanzamiento de los juegos en el conjunto de datos.
- Visualización de la relación entre dos variables: Se creó un gráfico de dispersión para visualizar la relación entre dos variables, como el precio y el año de lanzamiento, lo que proporciona información sobre cómo una variable podría afectar a otra en el conjunto de datos.
- Resumen estadístico de las columnas numéricas: Se utilizó la función describe() para obtener un resumen estadístico de las columnas numéricas del DataFrame, como el recuento, la media, la desviación estándar, los percentiles, etc.
- Valores únicos en una columna específica: Se utilizó la función unique() para obtener los valores únicos en una columna específica del DataFrame, como los géneros de los juegos, proporcionando una comprensión de la variedad y diversidad de las categorías.

Todos los pasos los pueden ver en el Jupyter Notebook 'EDA'.

3. Feature Engineering:

En el dataset user_reviews se incluyen reseñas de juegos hechos por distintos usuarios. Debes crear la columna 'sentiment_analysis' aplicando análisis de sentimiento con NLP con la siguiente escala: debe tomar el valor '0' si es malo, '1' si es neutral y '2' si es positivo. Esta nueva columna debe reemplazar la de user_reviews.review para facilitar el trabajo de los modelos de machine learning y el análisis de datos. De no ser posible este análisis por estar ausente la reseña escrita, debe tomar el valor de 1.

El código hace uso de las siguientes bibliotecas: pandas para la manipulación y análisis de datos, y nltk para el análisis de sentimientos de texto utilizando el algoritmo VADER (Valence Aware Dictionary and sEntiment Reasoner).

El algoritmo VADER proporciona análisis de sentimientos de texto mediante el análisis de la polaridad de las palabras y frases en el texto.

El código define una función de análisis de sentimientos que asigna valores de sentimiento (positivo, neutral o negativo) a las reseñas de usuarios en un DataFrame llamado user_reviews. Luego, aplica esta función a la columna de reseñas, asignando valores de sentimiento basados en la polaridad del texto.

El DataFrame actualizado, que incluye los valores de sentimiento asignados, se guarda en un archivo CSV llamado user_reviews_with_sentiment.csv. Este proceso proporciona una forma de analizar y etiquetar las reseñas de los usuarios en función de su contenido para su posterior procesamiento y análisis.

Todos los pasos los pueden ver en el Jupyter Notebook 'analisis_sentimiento'.

4. Funciones de Consultas:

Todos los pasos los pueden ver en el Jupyter Notebook 'Endpoints'.

Las funciones para los endpoints que se consumirán en la API son las siguientes:

1. `PlayTimeGenre(genero: str)`: Devuelve el año con más horas jugadas para dicho género.
   - Ejemplo de retorno: {"Año de lanzamiento con más horas jugadas para Género X" : 2013}

2. `UserForGenre(genero: str)`: Devuelve el usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año.
   - Ejemplo de retorno: {"Usuario con más horas jugadas para Género X" : us213ndjss09sdf, "Horas jugadas":[{Año: 2013, Horas: 203}, {Año: 2012, Horas: 100}, {Año: 2011, Horas: 23}]}

3. `UsersRecommend(año: int)`: Devuelve el top 3 de juegos MÁS recomendados por usuarios para el año dado.
   - Ejemplo de retorno: [{"Puesto 1" : X}, {"Puesto 2" : Y},{"Puesto 3" : Z}]

4. `UsersNotRecommend(año: int)`: Devuelve el top 3 de juegos MENOS recomendados por usuarios para el año dado.
   
5. `sentiment_analysis(año: int)`: Según el año de lanzamiento, se devuelve una lista con la cantidad de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento.
   - Ejemplo de retorno: {Negative = 182, Neutral = 120, Positive = 278}

5. API:

Ruta del Deploy de la API: [https://proyecto-individual01-2etz.onrender.com/docs](https://proyecto-individual01-2etz.onrender.com/docs)

Se muestra la función `UsersRecommend` que devuelve el top 3 de juegos MÁS recomendados por usuarios para el año dado. 

Como ejemplo:

- Ejemplo de retorno: [{"Puesto 1" : X}, {"Puesto 2" : Y},{"Puesto 3" : Z}]

6. VIDEO
"""
