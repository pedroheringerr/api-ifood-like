from fastapi import FastAPI

from fastapi.staticfiles import StaticFiles

from models import Restaurante
from models import Pedido

app = FastAPI(title="98food")
app.mount("/static", StaticFiles(directory="./static"))

pedidos = []
restaurantes: list[Restaurante] = []

@app.get("/restaurantes")
def obter_restaurantes():
    """
    Listar Restaurantes
    """
    return restaurantes

@app.post("/restaurantes")
def criar_restaurante(restaurante: Restaurante) -> Restaurante:
    restaurantes.append(restaurante)
    return restaurante

@app.put("/restaurantes/{id}")
def atualizar_restaurante(id: int, restaurante: Restaurante):
    for i in restaurantes:
        if i.id == id:
            i = restaurante
            return "OK"
    return "Não foi acahdo um restaurante com esse id"




@app.post("/pedido")
def criar_pedido(pedido: Pedido) -> str:
    """
    Criar pedidos
    """
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
