import copy
import pytest
from src.pedidos import processar_pedido


def item(sku='A', preco=1000, quantidade=1):
    return {'sku': sku, 'preco_centavos': preco, 'quantidade': quantidade}


def test_subtotal_quantidade():
    assert processar_pedido([item(preco=4000, quantidade=2)], {'A': 5}) == {
        'subtotal_centavos': 8000, 'desconto_centavos': 0,
        'frete_centavos': 1500, 'total_centavos': 9500}


def test_multiplos_itens():
    r = processar_pedido([item('A', 2500, 2), item('B', 1500, 1)], {'A': 3, 'B': 2})
    assert r['subtotal_centavos'] == 6500


def test_sku_repetido_ultrapassa_estoque():
    with pytest.raises(ValueError):
        processar_pedido([item(quantidade=2), item(quantidade=2)], {'A': 3})


def test_estoque_igual_pedido():
    assert processar_pedido([item(quantidade=2)], {'A': 2})['subtotal_centavos'] == 2000


@pytest.mark.parametrize('qtd', [0, -1, True, 1.5])
def test_quantidade_invalida(qtd):
    with pytest.raises(ValueError):
        processar_pedido([item(quantidade=qtd)], {'A': 5})


@pytest.mark.parametrize('desconto', [-1, 31, True, 2.5])
def test_desconto_invalido(desconto):
    with pytest.raises(ValueError):
        processar_pedido([item()], {'A': 2}, desconto)


def test_desconto_limiar():
    r = processar_pedido([item(preco=10000)], {'A': 2}, 10)
    assert r['desconto_centavos'] == 1000
    assert r['total_centavos'] == 10500


def test_arredondamento_desconto():
    r = processar_pedido([item(preco=10050)], {'A': 2}, 3)
    assert r['desconto_centavos'] == 301


def test_frete_apos_desconto():
    r = processar_pedido([item(preco=8000, quantidade=2)], {'A': 3}, 10)
    assert r['frete_centavos'] == 1500
    assert r['total_centavos'] == 15900


def test_frete_gratis_no_limite():
    r = processar_pedido([item(preco=15000)], {'A': 2})
    assert r['frete_centavos'] == 0


def test_entradas_inalteradas():
    itens, estoque = [item()], {'A': 2}
    original = copy.deepcopy((itens, estoque))
    processar_pedido(itens, estoque)
    assert (itens, estoque) == original


def test_sem_itens():
    with pytest.raises(ValueError):
        processar_pedido([], {'A': 2})


def test_sku_desconhecido():
    with pytest.raises(ValueError):
        processar_pedido([item()], {'B': 5})
