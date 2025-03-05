from fastapi import FastAPI, Response
from pydantic import BaseModel
from typing import List, Dict
import matplotlib.pyplot as plt
import io

app = FastAPI()

# Modelo para la parte "moda", donde "count" es un entero
class Moda(BaseModel):
    range: str
    count: int  # Ahora es entero

# Modelo para las estadísticas usando el modelo Moda
class Statistics(BaseModel):
    moda: Moda
    mediaPonderada: str
    desviacionEstandar: str
    total: int

# Modelo para cada ítem de resultado
class ResultItem(BaseModel):
    source: str
    ranges: Dict[str, int]
    statistics: Statistics

# Modelo para el input completo, que debe tener una clave "data" con "results"
class DataInput(BaseModel):
    data: Dict[str, List[ResultItem]]

@app.post("/graph")
def generate_graph(payload: DataInput):
    """
    Recibe el JSON en el formato:
    {
      "data": {
        "results": [
          {
            "source": "Mp9",
            "ranges": { ... },
            "statistics": { ... }
          },
          ...
        ]
      }
    }
    Genera un gráfico de barras comparando el total de mediciones por fuente y devuelve la imagen PNG.
    """

    # Extraer el array "results"
    results = payload.data.get("results", [])
    if not results:
        return {"error": "No se recibieron resultados"}

    # Preparar listas para las fuentes y totales
    fuentes = []
    totales = []
    for item in results:
        fuentes.append(item.source)
        totales.append(item.statistics.total)

    # Crear el gráfico con matplotlib
    plt.figure(figsize=(6, 4))
    plt.bar(fuentes, totales, color=["blue", "green", "red"])
    plt.title("Comparación de Totales por Fuente")
    plt.xlabel("Fuente")
    plt.ylabel("Total Mediciones")

    # Guardar la figura en un buffer en formato PNG
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()  # Cerrar la figura para liberar memoria
    buf.seek(0)
    img_bytes = buf.getvalue()

    # Retornar la imagen directamente con las cabeceras adecuadas
    return Response(content=img_bytes,
                    media_type="image/png",
                    headers={"Content-Disposition": "attachment; filename=graph.png"})


