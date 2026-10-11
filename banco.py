
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

        conexao.execute("""
            CREATE TABLE IF NOT EXISTS pedidos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data_criacao TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                total REAL NOT NULL CHECK (total >= 0)
            )
        """)

        conexao.execute("""
            CREATE TABLE IF NOT EXISTS itens_pedido (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pedido_id INTEGER NOT NULL,
                produto_id INTEGER NOT NULL,
                nome_produto TEXT NOT NULL,
                preco_unitario REAL NOT NULL,
                quantidade INTEGER NOT NULL CHECK (quantidade > 0),
                subtotal REAL NOT NULL,
                FOREIGN KEY (pedido_id) REFERENCES pedidos(id),
                FOREIGN KEY (produto_id) REFERENCES produtos(id)
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


def registrar_pedido(itens):
    if not isinstance(itens, list) or not itens:
        raise ValueError("O carrinho está vazio.")

    with conectar() as conexao:
        produtos_pedido = []
        ids_processados = set()
        total = 0

        for item in itens:
            produto_id = item.get("id")
            quantidade = item.get("quantidade")

            if (
                not isinstance(produto_id, int)
                or isinstance(produto_id, bool)
                or not isinstance(quantidade, int)
                or isinstance(quantidade, bool)
                or quantidade <= 0
            ):
                raise ValueError("Produto ou quantidade inválidos.")

            if produto_id in ids_processados:
                raise ValueError("Há produtos duplicados no carrinho.")

            ids_processados.add(produto_id)

            produto = conexao.execute("""
                SELECT id, nome, preco, estoque
                FROM produtos
                WHERE id = ?
            """, (produto_id,)).fetchone()

            if produto is None:
                raise ValueError("Um dos produtos não foi encontrado.")

            if quantidade > produto["estoque"]:
                raise ValueError(
                    f"Estoque insuficiente para {produto['nome']}."
                )

            subtotal = round(produto["preco"] * quantidade, 2)
            total = round(total + subtotal, 2)

            produtos_pedido.append({
                "id": produto["id"],
                "nome": produto["nome"],
                "preco": produto["preco"],
                "quantidade": quantidade,
                "subtotal": subtotal
            })

        cursor = conexao.execute("""
            INSERT INTO pedidos (total)
            VALUES (?)
        """, (total,))

        pedido_id = cursor.lastrowid

        for produto in produtos_pedido:
            atualizacao = conexao.execute("""
                UPDATE produtos
                SET estoque = estoque - ?
                WHERE id = ? AND estoque >= ?
            """, (
                produto["quantidade"],
                produto["id"],
                produto["quantidade"]
            ))

            if atualizacao.rowcount != 1:
                raise ValueError(
                    f"Estoque insuficiente para {produto['nome']}."
                )

            conexao.execute("""
                INSERT INTO itens_pedido (
                    pedido_id,
                    produto_id,
                    nome_produto,
                    preco_unitario,
                    quantidade,
                    subtotal
                )
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                pedido_id,
                produto["id"],
                produto["nome"],
                produto["preco"],
                produto["quantidade"],
                produto["subtotal"]
            ))

        return {
            "pedido_id": pedido_id,
            "total": total,
            "itens": produtos_pedido
        }


if __name__ == "__main__":
    inicializar_banco()

    for produto in listar_produtos():
        print(produto)

