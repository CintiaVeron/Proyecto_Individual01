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
merged_df = pd.read_parquet("Archivos_API/PlayTimeGenre.parquet")



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








if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)  # Ejecutar la aplicación con Uvicorn