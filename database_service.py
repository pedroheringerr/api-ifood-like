from sqlalchemy import create_engine, select, insert, update
from sqlalchemy.orm import sessionmaker

from models import Base, Restaurantes, Categoria # pyright: ignore[reportImplicitRelativeImport]

engine = create_engine("sqlite:///98food.db")
Base.metadata.create_all(engine)

def obter_banco_de_dados():
    db = sessionmaker(bind=engine)
    yield db
    db.close_all()

def obter_restaurantes():
    return select(Restaurantes)
