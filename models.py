from pydantic import BaseModel

class Restaurante(BaseModel):
    id: int
    nome: str
    categoria: str
    desc: str
    end: str
    cnpj: str

class Pedido(BaseModel):
    id: int
    itens: list[str]
    desc: str
    restaurante_id: int
    end: str
    codigo: int
