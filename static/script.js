
"use strict";

const CHAVE_CARRINHO = "miniLojaCarrinho";

const botoesAdicionar = document.querySelectorAll(".adicionar");
const areaItens = document.getElementById("carrinhoItens");
const quantidadeCarrinho = document.getElementById("quantidadeCarrinho");
const quantidadeResumo = document.getElementById("Carrinho");
const totalCarrinho = document.getElementById("total");
const botaoLimpar = document.getElementById("limpar");
const botaoFinalizar = document.getElementById("finalizar");
const mensagemCarrinho = document.getElementById("mensagemCarrinho");

let carrinho = carregarCarrinho();


function carregarCarrinho() {
    try {
        const dados = JSON.parse(
            localStorage.getItem(CHAVE_CARRINHO) || "[]"
        );

        if (!Array.isArray(dados)) {
            return [];
        }

        return dados.filter(item =>
            Number.isInteger(item.id) &&
            typeof item.nome === "string" &&
            Number.isFinite(item.preco) &&
            Number.isInteger(item.quantidade) &&
            item.quantidade > 0
        );
    } catch {
        return [];
    }
}


function salvarCarrinho() {
    localStorage.setItem(
        CHAVE_CARRINHO,
        JSON.stringify(carrinho)
    );
}


function formatarMoeda(valor) {
    return valor.toLocaleString("pt-BR", {
        style: "currency",
        currency: "BRL"
    });
}


function mostrarMensagem(texto) {
    if (mensagemCarrinho) {
        mensagemCarrinho.textContent = texto;
    }
}


function adicionarProduto(botao) {
    const id = Number(botao.dataset.id);
    const nome = botao.dataset.nome;
    const preco = Number(botao.dataset.preco);
    const estoque = Number(botao.dataset.estoque);

    const existente = carrinho.find(item => item.id === id);

    if (estoque <= 0) {
        mostrarMensagem("Este produto está esgotado.");
        return;
    }

    if (existente) {
        existente.estoque = estoque;

        if (existente.quantidade >= estoque) {
            mostrarMensagem(
                "Você já adicionou todo o estoque disponível deste produto."
            );
            return;
        }

        existente.quantidade += 1;
    } else {
        carrinho.push({
            id,
            nome,
            preco,
            estoque,
            quantidade: 1
        });
    }

    salvarCarrinho();
    renderizarCarrinho();
    mostrarMensagem(`${nome} foi adicionado ao carrinho.`);
}


function alterarQuantidade(id, variacao) {
    const item = carrinho.find(produto => produto.id === id);

    if (!item) {
        return;
    }

    const novaQuantidade = item.quantidade + variacao;

    if (novaQuantidade <= 0) {
        removerProduto(id);
        return;
    }

    if (novaQuantidade > item.estoque) {
        mostrarMensagem(
            "A quantidade não pode ultrapassar o estoque exibido."
        );
        return;
    }

    item.quantidade = novaQuantidade;

    salvarCarrinho();
    renderizarCarrinho();
    mostrarMensagem("");
}


function removerProduto(id) {
    carrinho = carrinho.filter(item => item.id !== id);

    salvarCarrinho();
    renderizarCarrinho();
    mostrarMensagem("Produto removido do carrinho.");
}


function criarBotao(texto, classe, acao, rotulo) {
    const botao = document.createElement("button");

    botao.type = "button";
    botao.className = classe;
    botao.textContent = texto;
    botao.setAttribute("aria-label", rotulo);
    botao.addEventListener("click", acao);

    return botao;
}


function renderizarCarrinho() {
    if (!areaItens) {
        return;
    }

    areaItens.replaceChildren();

    let unidades = 0;
    let total = 0;

    if (carrinho.length === 0) {
        const vazio = document.createElement("p");

        vazio.className = "carrinho-vazio";
        vazio.textContent = "Seu carrinho está vazio.";

        areaItens.appendChild(vazio);
    }

    carrinho.forEach(item => {
        unidades += item.quantidade;
        total += item.preco * item.quantidade;

        const linha = document.createElement("article");
        linha.className = "item-carrinho";

        const detalhes = document.createElement("div");
        detalhes.className = "detalhes-item";

        const nome = document.createElement("h3");
        nome.textContent = item.nome;

        const preco = document.createElement("p");
        preco.className = "preco-item";
        preco.textContent = `${formatarMoeda(item.preco)} cada`;

        detalhes.append(nome, preco);

        const controles = document.createElement("div");
        controles.className = "controles-item";

        const diminuir = criarBotao(
            "−",
            "botao-quantidade",
            () => alterarQuantidade(item.id, -1),
            `Diminuir quantidade de ${item.nome}`
        );

        const numero = document.createElement("span");
        numero.className = "quantidade-item";
        numero.textContent = item.quantidade;

        const aumentar = criarBotao(
            "+",
            "botao-quantidade",
            () => alterarQuantidade(item.id, 1),
            `Aumentar quantidade de ${item.nome}`
        );

        const remover = criarBotao(
            "Remover",
            "botao-remover",
            () => removerProduto(item.id),
            `Remover ${item.nome} do carrinho`
        );

        controles.append(diminuir, numero, aumentar, remover);

        const subtotal = document.createElement("strong");
        subtotal.className = "subtotal-item";
        subtotal.textContent = formatarMoeda(
            item.preco * item.quantidade
        );

        linha.append(detalhes, controles, subtotal);
        areaItens.appendChild(linha);
    });

    if (quantidadeCarrinho) {
        quantidadeCarrinho.textContent = unidades;
    }

    if (quantidadeResumo) {
        quantidadeResumo.textContent = unidades;
    }

    if (totalCarrinho) {
        totalCarrinho.textContent = formatarMoeda(total);
    }

    if (botaoFinalizar) {
        botaoFinalizar.disabled = carrinho.length === 0;
    }

    if (botaoLimpar) {
        botaoLimpar.disabled = carrinho.length === 0;
    }
}


botoesAdicionar.forEach(botao => {
    botao.addEventListener("click", () => {
        adicionarProduto(botao);
    });
});


if (botaoLimpar) {
    botaoLimpar.addEventListener("click", () => {
        carrinho = [];

        salvarCarrinho();
        renderizarCarrinho();
        mostrarMensagem("Carrinho limpo.");
    });
}


if (botaoFinalizar) {
    botaoFinalizar.addEventListener("click", () => {
        if (carrinho.length === 0) {
            mostrarMensagem("Adicione um produto antes de finalizar.");
            return;
        }

        const resumo = carrinho
            .map(item => `${item.quantidade}x ${item.nome}`)
            .join("\n");

        const total = carrinho.reduce(
            (soma, item) => soma + item.preco * item.quantidade,
            0
        );

        alert(
            `Resumo do pedido:\n\n${resumo}\n\n` +
            `Total: ${formatarMoeda(total)}\n\n` +
            "Demonstração: nenhum pedido ou pagamento foi enviado."
        );
    });
}


renderizarCarrinho();
