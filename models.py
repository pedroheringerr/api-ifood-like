from sqlalchemy import Integer, Text, ForeignKey
from sqlalchemy.orm import declarative_base, mapped_column, Mapped, relationship


Base = declarative_base()


class Categoria(Base):
    __tablename__ = 'CATEGORIAS'
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome = mapped_column(Text)


class Restaurantes(Base):
    __tablename__ = 'RESTAURANTES'
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    local = mapped_column(Text)
    categoria_id = mapped_column(ForeignKey('CATEGORIAS.id'))
    categoria: Mapped['Categoria'] = relationship(back_populates='post')
