
from flask import Flask, render_template, abort, request, jsonify
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


@app.route("/finalizar", methods=["POST"])
def finalizar():
    dados = request.get_json(silent=True)

    if not isinstance(dados, dict):
        return jsonify({"erro": "Dados do pedido inválidos."}), 400

    try:
        pedido = banco.registrar_pedido(dados.get("itens"))

        return jsonify({
            "mensagem": "Pedido registrado com sucesso!",
            "pedido_id": pedido["pedido_id"],
            "total": pedido["total"]
        }), 201

    except ValueError as erro:
        return jsonify({"erro": str(erro)}), 400


@app.errorhandler(404)
def pagina_nao_encontrada(erro):
    return render_template("404.html"), 404


if __name__ == "__main__":
    banco.inicializar_banco()
    app.run(debug=True)
