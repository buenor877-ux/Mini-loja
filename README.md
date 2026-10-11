
# Mini-Loja

Aplicação web de uma mini loja virtual desenvolvida para praticar programação, desenvolvimento web e integração entre tecnologias.

## Funcionalidades

- Listagem de produtos cadastrados no banco de dados.
- Visualização dos detalhes de cada produto.
- Carrinho de compras interativo.
- Adição, remoção e alteração da quantidade de produtos.
- Cálculo automático de subtotais e total do carrinho.
- Persistência do carrinho no navegador.
- Validação dos produtos e das quantidades no servidor.
- Registro de pedidos no banco de dados SQLite.
- Atualização do estoque após a confirmação do pedido.
- Página personalizada para endereços não encontrados.
- Interface responsiva para diferentes tamanhos de tela.

## Tecnologias utilizadas

- Python
- Flask
- SQLite
- HTML5
- CSS3
- JavaScript

## Estrutura do projeto

- `app.py`: aplicação Flask e rotas.
- `banco.py`: acesso ao banco de dados, validações e registro de pedidos.
- `loja.db`: banco de dados SQLite.
- `templates/`: páginas HTML.
- `static/`: arquivos CSS e JavaScript.
- `requirements.txt`: dependências Python.
- `.gitignore`: arquivos ignorados pelo Git.

## Como executar

1. Instale o Python.
2. Abra o terminal na pasta do projeto.
3. Instale as dependências:

   `python -m pip install -r requirements.txt`

4. Inicie a aplicação:

   `python app.py`

5. Acesse no navegador:

   `http://127.0.0.1:5000`

## Como funciona a compra

1. Selecione os produtos desejados.
2. Ajuste as quantidades no carrinho.
3. Clique em "Finalizar pedido".
4. O servidor valida os produtos e o estoque.
5. O pedido é registrado no SQLite e o estoque é atualizado.
6. Após a confirmação, o carrinho é limpo e uma mensagem informa o resultado.

## Observações

Este é um projeto de estudo. Os pedidos são registrados no banco de dados, mas não existe integração com meios de pagamento nem processamento real de entregas.

## Objetivo do projeto

Praticar Python, Flask, SQLite, HTML, CSS, JavaScript, operações CRUD, validação de dados e integração entre front-end e back-end.
