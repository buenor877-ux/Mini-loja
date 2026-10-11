
from flask import Flask, render_template, abort
import banco

app = Flask(__name__)


@app.route("/")
def inicio():
    produtos = banco.listar_produtos()

    return render_template(
        "index.html",
        produtos=produtos
    )


@app.route("/comprar/<int:produto_id>")
def comprar(produto_id):
    produto = banco.buscar_produto(produto_id)

    if produto is None:
        abort(404)

    return render_template(
        "compra.html",
        produto=produto
    )


@app.errorhandler(404)
def pagina_nao_encontrada(erro):
    return render_template("404.html"), 404


if __name__ == "__main__":
    banco.inicializar_banco()
    app.run(debug=True)
