from fastapi import FastAPI

from fastapi.staticfiles import StaticFiles

from models import Restaurante
from models import Pedido

app = FastAPI(title="Ifood")
app.mount("/static", StaticFiles(directory="./static"))

pedidos: list[Pedido] = []
restaurantes: list[Restaurante] = []

@app.get("/restaurantes")
def obter_restaurantes():
    """
    Listar Restaurantes
    """
    return restaurantes

@app.post("/restaurantes")
def criar_restaurante(restaurante: Restaurante) -> Restaurante:
    restaurante.id = len(restaurantes) + 1
    restaurantes.append(restaurante)
    return restaurante

@app.put("/restaurantes/{id}")
def atualizar_restaurante(id: int, restaurante: Restaurante):
    for i, r in enumerate(restaurantes):
        if r.id == id:

            restaurante.id = id

            restaurantes[i] = restaurante
            return restaurante
    return {"erro": "Restaurante não encontrado"}

@app.post("/pedido")
def criar_pedido(pedido: Pedido):
    """
    Criar pedidos
    """
    restaurante_existe = False
    for r in restaurantes:
        if r.id == pedido.restaurante_id:
            restaurante_existe = True
            break

    if not restaurante_existe:
        return {"erro": "O restaurante informado não existe."}

    pedido.id = len(pedidos) + 1
    pedidos.append(pedido)
    return pedido

@app.get("/pedido")
def obter_pedido():
    """
    Listar pedidos
    """
    return pedidos

@app.get("/pedido/{id}")
def obter_pedido_id(id: int):
    """
    Obter pedidos
    """
    for pedido in pedidos:
        if pedido.id == id:
            return pedido
    return "Error"
