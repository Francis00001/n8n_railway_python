from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict
import matplotlib.pyplot as plt
import io
import base64

app = FastAPI()

# Definimos modelos Pydantic para validar la estructura de "results"
class Statistics(BaseModel):
    moda: Dict[str, str]
    mediaPonderada: str
    desviacionEstandar: str
    total: int

class ResultItem(BaseModel):
    source: str
    ranges: Dict[str, int]
    statistics: Statistics

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
    """

    # Extraemos el array results
    results = payload.data.get("results", [])
    if not results:
        return {"error": "No se recibieron resultados"}

    # Ejemplo: Graficar la suma total de cada fuente (o lo que necesites)
    fuentes = []
    totales = []

    for item in results:
        fuentes.append(item.source)
        totales.append(item.statistics.total)

    # Crear la figura
    plt.figure(figsize=(6, 4))
    plt.bar(fuentes, totales, color=["blue", "green", "red"])
    plt.title("Comparación de Totales por Fuente")
    plt.xlabel("Fuente")
    plt.ylabel("Total Mediciones")

    # Convertir a imagen en base64
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    base64_img = base64.b64encode(buf.read()).decode("utf-8")
    plt.close()

    # Devolver el gráfico en base64
    return {"image_base64": base64_img}
