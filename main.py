from fastapi import FastAPI,HTTPException
from fastapi.responses import JSONResponse
import pandas as pd



app = FastAPI(title='API Steam Games')

#Mensaje de bienvenida
@app.get("/")
async def root():
    return {"Mensaje": "Bienvenidos a mi proyecto individual del bootcamp SoyHenry"}




# Cargar los datos si es necesario
merged_df = pd.read_parquet("Archivos_API/PlayTimeGenre.parquet")
df_UsersRecommend= pd.read_parquet('Archivos_API/UsersRecommend.parquet')
df_UsersnotRecommend= pd.read_parquet('Archivos_API/UsernotRecommend.parquet')
reviews_df= pd.read_parquet('Archivos_API/sentiment_analysis.parquet')
# Definir tu aplicación FastAPI
app = FastAPI()

# Definir la función PlayTimeGenre con manejo de errores
#PlayTimeGenre
@app.get("/PlayTimeGenre/{genero :str}")
async def PlayTimeGenre(genero):
    try:
        # Filtrar por género
        merged_df_genero = merged_df[merged_df['genero'].str.contains(genero, case=False)]

        # Si no hay datos para el género, lanzar una excepción HTTP 404
        if merged_df_genero.empty:
            raise HTTPException(status_code=404, detail=f"No se encontraron datos para el género {genero}")

        # Calcular las horas jugadas por año de lanzamiento
        horas_por_anio = merged_df_genero.groupby('anio_lanzamiento')['playtime_forever'].sum()

        # Encontrar el año con más horas jugadas
        año_max_horas = horas_por_anio.idxmax()

        # Devolver el resultado
        return {f"Año de lanzamiento con más horas jugadas para {genero}": año_max_horas}
    
    except HTTPException as e:
        # Si ya es una excepción HTTP, solo relanzarla
        raise e
    except Exception as e:
        # En caso de cualquier otro error, lanzar una excepción HTTP 500
        raise HTTPException(status_code=500, detail=str(e))




# Definir la función para UserForGenre 


@app.get("/UserForGenre/{genero :str}")
async def UserForGenre(genero):
    try:
        # Filtrar por género
        merged_df_genero = merged_df[merged_df['genero'].str.contains(genero, case=False)]

        # Si no hay datos para el género, lanzar una excepción HTTP 404
        if merged_df_genero.empty:
            raise HTTPException(status_code=404, detail=f"No se encontraron datos para el género {genero}")

        # Encontrar el usuario que acumula más horas jugadas
        user_max_horas = merged_df_genero.groupby('user_id')['playtime_forever'].sum().idxmax()
    
        # Calcular la acumulación de horas jugadas por año
        horas_por_anio = merged_df_genero.groupby('anio_lanzamiento')['playtime_forever'].sum().reset_index()
        horas_por_anio = horas_por_anio.rename(columns={'anio_lanzamiento': 'Año', 'playtime_forever': 'Horas'})
        horas_por_anio = horas_por_anio.to_dict(orient='records')

        # Devolver el resultado
        return {
        f"Usuario con más horas jugadas para {genero}": user_max_horas,
        "Horas jugadas": horas_por_anio
    }
    
    except HTTPException as e:
        # Si ya es una excepción HTTP, solo relanzarla
        raise e
    except Exception as e:
        # En caso de cualquier otro error, lanzar una excepción HTTP 500
        raise HTTPException(status_code=500, detail=str(e))








# Definir la función UserRecommend con manejo de errores
@app.get("/UserRecommend/{año:int}")
async def UserRecommend(año: int):
    try:
        # Filtrar las recomendaciones para el año dado y recomendaciones positivas/neutrales
        recomendaciones = df_UsersRecommend[df_UsersRecommend['posted'] == año]

        # Si no hay datos para el año, lanzar una excepción HTTP 404
        if recomendaciones.empty:
            raise HTTPException(status_code=404, detail=f"No hay recomendaciones para el año {año}")

        # Ordenar en orden descendente por la cantidad de recomendaciones
        recomendaciones = recomendaciones.sort_values('recommend', ascending=False)

        # Crear una única línea de resultado con los tres primeros juegos recomendados
        resultado = {
            "Puesto 1": recomendaciones.iloc[0]['app_name'],
            "Puesto 2": recomendaciones.iloc[1]['app_name'],
            "Puesto 3": recomendaciones.iloc[2]['app_name']
        }

        # Devolver el resultado
        return {
            f"El top 3 de los juegos más recomendados para el año {año} son": resultado
        }

    except HTTPException as e:
        # Si ya es una excepción HTTP, solo relanzarla
        raise e
    except Exception as e:
        # En caso de cualquier otro error, lanzar una excepción HTTP 500
        raise HTTPException(status_code=500, detail=str(e))
    

# Definir la función UsernotRecommend con manejo de errores
@app.get("/UsernotRecommend/{año:int}")
async def UsernotRecommend(año: int):
    try:
        # Filtrar las recomendaciones para el año dado y recomendaciones falsas/negativas
        recomendaciones = df_UsersnotRecommend[df_UsersnotRecommend['posted'] == año]

        # Si no hay datos para el año, lanzar una excepción HTTP 404
        if recomendaciones.empty:
            raise HTTPException(status_code=404, detail=f"No hay recomendaciones para el año {año}")

        # Ordenar en orden descendente por la cantidad de recomendaciones
        recomendaciones = recomendaciones.sort_values('recommend', ascending=False)

        # Crear una única línea de resultado con los tres primeros juegos recomendados
        resultado = {
            "Puesto 1": recomendaciones.iloc[0]['app_name'],
            "Puesto 2": recomendaciones.iloc[1]['app_name'],
            "Puesto 3": recomendaciones.iloc[2]['app_name']
        }

        # Devolver el resultado
        return {
            f"El top 3 de los juegos menos recomendados para el año {año} son": resultado
        }

    except HTTPException as e:
        # Si ya es una excepción HTTP, solo relanzarla
        raise e
    except Exception as e:
        # En caso de cualquier otro error, lanzar una excepción HTTP 500
        raise HTTPException(status_code=500, detail=str(e))



@app.get("/sentiment_analysis/{año:int}")
def sentiment_analysis(año: int):
    try:
        # Filtrar el DataFrame de reseñas por el año dado
        filtered_reviews = reviews_df[reviews_df['posted'] == año]

        if filtered_reviews.empty:
            raise HTTPException(status_code=404, detail=f"No hay reseñas para el año {año}")

        # Convertir los valores de la columna sentiment_analysis a tipo entero
        filtered_reviews['sentiment_analysis'] = filtered_reviews['sentiment_analysis'].astype(int)

        # Contar la cantidad de registros para cada categoría de análisis de sentimiento
        sentiment_counts = filtered_reviews['sentiment_analysis'].value_counts()

        # Crear un diccionario para almacenar los resultados
        result = {
            "La cantidad de registros categorizados con un análisis de sentimiento para ese año es:": {
                'Negative': int(sentiment_counts.get(0, 0)),  # 0 para negativo
                'Neutral': int(sentiment_counts.get(1, 0)),   # 1 para neutral
                'Positive': int(sentiment_counts.get(2, 0))   # 2 para positivo
            }
        }

        return result
    
    except HTTPException as e:
        # Si ya es una excepción HTTP, solo relanzarla
        raise e
    except Exception as e:
        # En caso de cualquier otro error, lanzar una excepción HTTP 500
        raise HTTPException(status_code=500, detail=str(e))




