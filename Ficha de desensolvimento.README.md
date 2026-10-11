# Mini-Loja

Aplicação web de uma mini loja virtual desenvolvida para praticar programação e integração entre tecnologias.

## Funcionalidades

- Listagem de produtos cadastrados no banco de dados.
- Visualização dos detalhes de cada produto.
- Carrinho de compras interativo.
- Adição e remoção de produtos do carrinho.
- Atualização de quantidades e cálculo automático do total.
- Persistência do carrinho no navegador.
- Página personalizada para endereços não encontrados.

## Tecnologias utilizadas

- Python
- Flask
- SQLite
- HTML5
- CSS3
- JavaScript

## Estrutura do projeto

- `app.py`: aplicação Flask e rotas.
- `banco.py`: operações de acesso ao banco de dados.
- `loja.db`: banco de dados SQLite.
- `templates/`: páginas HTML.
- `static/`: arquivos CSS e JavaScript.
- `requirements.txt`: dependências Python.
- `.gitignore`: arquivos ignorados pelo Git.

## Como executar

1. Instale o Python.
2. Abra o terminal na pasta do projeto.
3. Instale a dependência:

   `python -m pip install -r requirements.txt`

4. Inicie a aplicação:

   `python app.py`

5. Acesse no navegador:

   `http://127.0.0.1:5000`

## Observação

Este projeto é uma aplicação de estudo. O carrinho funciona no navegador, mas não há integração real com pagamentos ou processamento de pedidos.