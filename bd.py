import sqlite3
import json
from typing import Any
from models import Restaurante, Pedido

def obter_conexao() -> sqlite3.Connection:
    con = sqlite3.connect("98food.db")
    return con

def criar_base(con: sqlite3.Connection) -> None:
    con.execute("""
    CREATE TABLE IF NOT EXISTS CATEGORIAS (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome VARCHAR(50) UNIQUE
    );
    """)

    con.execute("""
    CREATE TABLE IF NOT EXISTS RESTAURANTES (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome VARCHAR(50) NOT NULL,
        local VARCHAR(200) NOT NULL,
        id_categoria VARCHAR(200),
        cnpj VARCHAR(18) NOT NULL,
        desc VARCHAR(200),
        FOREIGN KEY (id_categoria) REFERENCES CATEGORIAS (id)
    );
    """)

    con.execute("""
    CREATE TABLE IF NOT EXISTS PEDIDOS (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        itens TEXT NOT NULL,
        desc TEXT,
        restaurante_id INTEGER NOT NULL,
        end VARCHAR(200) NOT NULL,
        codigo INTEGER NOT NULL,
        FOREIGN KEY (restaurante_id) REFERENCES RESTAURANTES (id)
    );
    """)
    con.commit()

def garantir_categoria(nome_categoria: str, con: sqlite3.Connection) -> int:
    """Busca o ID da categoria ou cria uma nova se não existir."""
    cursor = con.execute("SELECT id FROM CATEGORIAS WHERE nome = ?", (nome_categoria,))
    row = cursor.fetchone()
    if row:
        return row[0]
    
    cursor = con.execute("INSERT INTO CATEGORIAS (nome) VALUES (?)", (nome_categoria,))
    con.commit()
    return cursor.lastrowid or 0

def obter_restaurantes(con: sqlite3.Connection) -> list[tuple[Any, ...]]:
    cursor = con.execute("""
        SELECT r.id, r.nome, r.local, c.nome, r.cnpj, r.desc 
        FROM RESTAURANTES r LEFT JOIN CATEGORIAS c ON r.id_categoria = c.id
    """)
    return cursor.fetchall()

def obter_restaurante(con: sqlite3.Connection, id_restaurante: int) -> tuple[Any, ...] | None:
    cursor = con.execute(f"""
        SELECT r.id, r.nome, r.local, c.nome, r.cnpj, r.desc 
        FROM RESTAURANTES r
        LEFT JOIN CATEGORIAS c ON r.id_categoria = c.id
        WHERE r.id = {id_restaurante}
    """)
    return cursor.fetchall()

def inserir_restaurante(con: sqlite3.Connection, restaurante: Restaurante) -> int:
    dados = (restaurante.nome, restaurante.end, 0, restaurante.cnpj, restaurante.desc)
    cursor = con.execute("""
        INSERT INTO RESTAURANTES (nome, local, id_categoria, cnpj, desc) 
        VALUES (?, ?, ?, ?, ?)
    """, dados)
    con.commit()
    return cursor.lastrowid or 0

def atualizar_restaurante_db(con: sqlite3.Connection, id: int, restaurante: Restaurante) -> bool:
    id_cat = garantir_categoria(con, restaurante.categoria)
    dados = (restaurante.nome, restaurante.end, id_cat, restaurante.cnpj, restaurante.desc, id)
    cursor = con.execute("""
        UPDATE RESTAURANTES 
        SET nome = ?, local = ?, id_categoria = ?, cnpj = ?, desc = ?
        WHERE id = ?
    """, dados)
    con.commit()
    return cursor.rowcount > 0

# --- FUNÇÕES DE PEDIDO ---
def obter_pedidos(con: sqlite3.Connection) -> list[tuple[Any, ...]]:
    cursor = con.execute("SELECT id, itens, desc, restaurante_id, end, codigo FROM PEDIDOS")
    return cursor.fetchall()

def obter_pedido(con: sqlite3.Connection, id_pedido: int) -> tuple[Any, ...] | None:
    cursor = con.execute("SELECT id, itens, desc, restaurante_id, end, codigo FROM PEDIDOS WHERE id = ?", (id_pedido,))
    return cursor.fetchone()

def inserir_pedido(con: sqlite3.Connection, pedido: Pedido) -> int:
    itens_json = json.dumps(pedido.itens) # Transforma a lista de itens em String (JSON)
    dados = (itens_json, pedido.desc, pedido.restaurante_id, pedido.end, pedido.codigo)
    
    try:
        cursor = con.execute("""
            INSERT INTO PEDIDOS (itens, desc, restaurante_id, end, codigo) 
            VALUES (?, ?, ?, ?, ?)
        """, dados)
        con.commit()
        return cursor.lastrowid or 0
    except sqlite3.IntegrityError:
        # Retorna 0 se o restaurante_id não existir (erro da chave estrangeira)
        return 0

# Executado ao importar o arquivo para garantir que as tabelas existem
connection = obter_conexao()
criar_base(connection)
