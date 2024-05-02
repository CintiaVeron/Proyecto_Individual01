
from fastapi import FastAPI,HTTPException
from fastapi.responses import JSONResponse
import pandas as pd
from typing import List
import uvicorn


app = FastAPI(title='API Steam Games')

#Mensaje de bienvenida
@app.get("/")
async def root():
    return {"Mensaje": "Bienvenidos a mi proyecto individual del bootcamp SoyHenry"}




# Cargar los datos si es necesario
merged_df = pd.read_csv("Archivos_API/funcion1_2.csv")
df_ml=pd.read_csv("Archivos_API/df_ml.csv")
df_t=pd.read_csv("Archivos_API/top_100_juegos.csv")

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


def get_top_similar_games(item_id: int) -> str:
    try:
        # Corregimos el index para que sea el item_id
        df = df_ml.set_index('item_id')

        # Buscamos los juegos similares para el id dado
        juegos_similares = df.loc[item_id].sort_values(ascending=False)

        # Filtramos por los primeros 5, desde la posicion 1 ya que el primer lugar corresponde a uno mismo
        top_juegos_similares = juegos_similares.iloc[1:].nlargest(5)

        # Buscamos los id's de dichos juegos y los convertimos en una lista
        lista_de_ids = top_juegos_similares.index.astype(int).tolist()

        # Buscamos los titulos de los juegos
        titulos_top = df_t.loc[df_t['item_id'].isin(lista_de_ids), 'titulo'].values.tolist()

        # Construimos el mensaje con los juegos recomendados
        mensaje = f"Los juegos recomendados según el Item ID {item_id} son: {', '.join(titulos_top)}"
        return mensaje
    except KeyError:
        raise HTTPException(status_code=404, detail="El ID del juego no se encontró en la base de datos")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@app.get('/recomendacion_juego/{item_id}')
def recomendacion_juego_endpoint(item_id: int) -> str:
    return get_top_similar_games(item_id)
