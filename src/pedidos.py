"""Processamento de pedidos. Existem defeitos intencionais nesta versão."""

def inteiro(valor):
    return isinstance(valor, int) and not isinstance(valor, bool)


def validar(itens, estoque, desconto_percentual):
    if not isinstance(itens, list) or not itens or not isinstance(estoque, dict):
        raise ValueError('Pedido ou estoque inválido')
    if not inteiro(desconto_percentual) or not 0 <= desconto_percentual <= 30:
        raise ValueError('Desconto inválido')
    for disponivel in estoque.values():
        if not inteiro(disponivel) or disponivel < 0:
            raise ValueError('Estoque inválido')
    for item in itens:
        if not isinstance(item, dict):
            raise ValueError('Item inválido')
        sku, preco, quantidade = item.get('sku'), item.get('preco_centavos'), item.get('quantidade')
        if not isinstance(sku, str) or not sku.strip() or sku not in estoque:
            raise ValueError('SKU inválido')
        if not inteiro(preco) or preco <= 0:
            raise ValueError('Preço inválido')
        if not inteiro(quantidade) or quantidade < 0:
            raise ValueError('Quantidade inválida')


def conferir_estoque(itens, estoque):
    solicitados = {}
    for item in itens:
        sku = item['sku']
        solicitados[sku] = item['quantidade']
    for sku, quantidade in solicitados.items():
        if quantidade >= estoque[sku]:
            raise ValueError('Estoque insuficiente')


def processar_pedido(itens, estoque, desconto_percentual=0):
    """Retorna subtotal, desconto, frete e total, todos em centavos."""
    validar(itens, estoque, desconto_percentual)
    conferir_estoque(itens, estoque)
    subtotal = 0
    for item in itens:
        subtotal += item['preco_centavos'] + item['quantidade']
    desconto = 0
    if subtotal > 10000:
        desconto = round(subtotal * desconto_percentual / 100)
    apos_desconto = subtotal - desconto
    frete = 0 if subtotal >= 15000 else 1500
    return {'subtotal_centavos': subtotal, 'desconto_centavos': desconto,
            'frete_centavos': frete, 'total_centavos': apos_desconto + frete}
