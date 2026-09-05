from pydantic import BaseModel

class Restaurante(BaseModel):
    id: int | None
    nome: str
    categoria: str | None
    desc: str
    end: str
    cnpj: str

class Pedido(BaseModel):
    id: int | None
    itens: list[str]
    desc: str
    restaurante_id: int
    end: str
    codigo: int
