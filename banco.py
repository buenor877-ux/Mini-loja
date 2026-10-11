
import sqlite3
from pathlib import Path


CAMINHO_BANCO = Path(__file__).with_name("loja.db")


def conectar():
    conexao = sqlite3.connect(CAMINHO_BANCO)
    conexao.row_factory = sqlite3.Row
    return conexao


def inicializar_banco():
    with conectar() as conexao:
        conexao.execute("""
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                preco REAL NOT NULL CHECK (preco >= 0),
                estoque INTEGER NOT NULL DEFAULT 0
                    CHECK (estoque >= 0)
            )
        """)

        quantidade = conexao.execute(
            "SELECT COUNT(*) FROM produtos"
        ).fetchone()[0]

        if quantidade == 0:
            produtos_iniciais = [
                ("Notebook", 75.00, 10),
                ("Mouse Gamer", 20.00, 10),
                ("Teclado Mecânico", 30.00, 10)
            ]

            conexao.executemany("""
                INSERT INTO produtos (nome, preco, estoque)
                VALUES (?, ?, ?)
            """, produtos_iniciais)


def listar_produtos():
    with conectar() as conexao:
        produtos = conexao.execute("""
            SELECT id, nome, preco, estoque
            FROM produtos
            ORDER BY id
        """).fetchall()

        return [dict(produto) for produto in produtos]


def buscar_produto(produto_id):
    with conectar() as conexao:
        produto = conexao.execute("""
            SELECT id, nome, preco, estoque
            FROM produtos
            WHERE id = ?
        """, (produto_id,)).fetchone()

        return dict(produto) if produto else None


if __name__ == "__main__":
    inicializar_banco()

    for produto in listar_produtos():
        print(produto)

