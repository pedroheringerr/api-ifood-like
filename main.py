from sqlite3 import Connection
import json
from fastapi import Depends, FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles

import bd  # pyright: ignore[reportImplicitRelativeImport]
from models import Restaurante, Pedido

app = FastAPI(title="Ifood")
app.mount("/static", StaticFiles(directory="./static"))

## RESTAURANTES

@app.get("/restaurantes", response_model=list[Restaurante])
def listar_restaurantes(con: Connection = Depends(bd.obter_conexao)):
    """ Listar Restaurantes """
    dados = bd.obter_restaurantes(con)
    return [
        Restaurante(id=id, nome=nome, end=end, categoria=categoria, cnpj=cnpj, desc=desc)
        for id, nome, end, categoria, cnpj, desc in dados
    ]

@app.get("/restaurantes/{id}", response_model=Restaurante)
def obter_restaurante_por_id(id: str, con: Connection = Depends(bd.obter_conexao)):
    """ Obter restaurante a partir do id """
    dados = bd.obter_restaurante(con, id)
    if not dados:
        raise HTTPException(status_code=404, detail="Restaurante não encontrado")
    
    return [Restaurante(
        id=dado[0], nome=dado[1], end=dado[2], 
        categoria=dado[3], cnpj=dado[4], desc=dado[5]
    )
        for dado in dados
    ]

@app.post("/restaurantes", response_model=Restaurante)
def criar_restaurante(restaurante: Restaurante, con: Connection = Depends(bd.obter_conexao)):
    """ Cria um restaurante e retorna os dados salvos """
    novo_id = bd.inserir_restaurante(con, restaurante)
    restaurante.id = novo_id
    return restaurante

@app.put("/restaurantes/{id}", response_model=Restaurante)
def atualizar_restaurante(id: int, restaurante: Restaurante, con: Connection = Depends(bd.obter_conexao)):
    """ Atualiza um restaurante """
    sucesso = bd.atualizar_restaurante_db(con, id, restaurante)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Restaurante não encontrado para atualização")
    
    restaurante.id = id
    return restaurante


# --- ENDPOINTS PEDIDOS ---

@app.get("/pedido", response_model=list[Pedido])
def listar_pedidos(con: Connection = Depends(bd.obter_conexao)):
    """ Listar Pedidos """
    dados = bd.obter_pedidos(con)
    return [
        Pedido(
            id=id, 
            itens=json.loads(itens_json), # Converte o texto JSON de volta para lista no Python
            desc=desc, 
            restaurante_id=rest_id, 
            end=end, 
            codigo=codigo
        )
        for id, itens_json, desc, rest_id, end, codigo in dados
    ]

@app.get("/pedido/{id}", response_model=Pedido)
def obter_pedido_por_id(id: int, con: Connection = Depends(bd.obter_conexao)):
    """ Obter pedido específico """
    dado = bd.obter_pedido(con, id)
    if not dado:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    
    return Pedido(
        id=dado[0], 
        itens=json.loads(dado[1]), 
        desc=dado[2], 
        restaurante_id=dado[3], 
        end=dado[4], 
        codigo=dado[5]
    )

@app.post("/pedido", response_model=Pedido)
def criar_pedido(pedido: Pedido, con: Connection = Depends(bd.obter_conexao)):
    """ Criar um pedido (Garante vínculo com restaurante) """
    novo_id = bd.inserir_pedido(con, pedido)
    
    if novo_id == 0:
        raise HTTPException(status_code=400, detail="Restaurante inexistente. Não é possível salvar o pedido.")
    
    pedido.id = novo_id
    return pedido
