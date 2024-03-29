from fastapi import FastAPI,HTTPException
from fastapi.responses import JSONResponse
import pandas as pd
import pyarrow.parquet as pq 
import uvicorn  


app = FastAPI(title='API Steam Games')

#Mensaje de bienvenida
@app.get("/")
async def root():
    return {"Mensaje": "Bienvenidos a mi proyecto individual del bootcamp SoyHenry"}




# Cargar los datos si es necesario
df_UsersRecommend = pd.read_parquet("Archivos_API/UsersRecommend.parquet")



# Definir tu aplicación FastAPI
app = FastAPI()

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
    


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)  # Ejecutar la aplicación con Uvicorn