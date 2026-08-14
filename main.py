from fastapi import FastAPI


app = FastAPI(title="98food")

pedidos = []
restaurantes = []

@app.get("/restaurantes")
def obter_restaurantes():
    """
    Listar Restaurantes
    """
    return restaurantes

@app.post("/restaurantes")
def criar_restaurante(num: int, nome: str, cnpj: str, endereco: str, desc: str, categoria: str) -> str:
    restaurante = {"Num": num, "Nome": nome, "Categoria": categoria, "Descrição": desc, "Endereco": endereco, "CNPJ": cnpj}
    restaurantes.append(restaurante)
    return "OK"

@app.post("/pedido")
def criar_pedido(num: int, comida: str, bebida: str) -> str:
    """
    Criar pedidos
    """
    pedido = {"Número": num, "Comida": comida, "Bebida": bebida}
    pedidos.append(pedido)
    return "OK"

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
    return pedidos[id-1]
