from fastapi import FastAPI, Response
from pydantic import BaseModel
from typing import List, Dict
import matplotlib.pyplot as plt
import io

app = FastAPI()

class Moda(BaseModel):
    range: str
    count: int

class Statistics(BaseModel):
    moda: Moda
    mediaPonderada: str
    desviacionEstandar: str
    total: int

class ResultItem(BaseModel):
    source: str
    ranges: Dict[str, int]
    statistics: Statistics

class DataInput(BaseModel):
    data: Dict[str, List[ResultItem]]

@app.post("/graph-subplots")
def generate_graph_subplots(payload: DataInput):
    results = payload.data.get("results", [])
    if not results:
        return {"error": "No se recibieron resultados"}

    # Crear la figura con subplots
    fig, axs = plt.subplots(1, len(results), figsize=(6 * len(results), 5))

    if len(results) == 1:
        axs = [axs]

    for i, item in enumerate(results):
        x = list(item.ranges.keys())
        y = list(item.ranges.values())
        axs[i].bar(x, y, color="skyblue")
        axs[i].set_title(f"Distribución de {item.source}")
        axs[i].set_xlabel("Rango de Temperaturas")
        axs[i].set_ylabel("Número de Mediciones")
        axs[i].tick_params(axis='x', rotation=45)

    plt.tight_layout()

    # Convertir la figura a PNG en memoria
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)

    # **Asegurar que se devuelve en binario correctamente**
    return Response(
        content=buf.getvalue(),
        media_type="image/png",
        headers={"Content-Disposition": "inline; filename=subplots.png"}
    )
