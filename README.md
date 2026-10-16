# Experimento — Tarefa de Correção de Defeitos

**Tempo máximo: 25 minutos.** Receba o código Python existente de uma loja virtual e corrija os defeitos de processamento de pedidos. Não implemente interface, banco de dados ou acesso à internet.

## Interface

`processar_pedido(itens, estoque, desconto_percentual=0)` em `src/pedidos.py`.

- `itens`: lista de dicionários `{"sku": str, "preco_centavos": int, "quantidade": int}`.
- `estoque`: dicionário `{sku: quantidade_disponivel}`.
- `desconto_percentual`: inteiro de 0 a 30.
- Resultado: dicionário com `subtotal_centavos`, `desconto_centavos`, `frete_centavos`, `total_centavos` (inteiros).
- Valores monetários são representados em **centavos**: 10000 = R$ 100,00.

## Requisitos funcionais

| ID | Comportamento esperado |
|---|---|
| RF01 | Calcular o subtotal somando preço em centavos multiplicado pela quantidade de cada item. |
| RF02 | Somar quantidades de todas as entradas com o mesmo SKU ao validar o estoque. |
| RF03 | Aceitar a quantidade exatamente igual ao estoque e rejeitar apenas pedidos que o excedam. |
| RF04 | Levantar `ValueError` para lista vazia, formato de item inválido, SKU vazio/inexistente no estoque, preço e quantidade não inteiros positivos, estoque não inteiro não negativo, desconto não inteiro ou fora de 0–30; `bool` não deve ser aceito como inteiro. |
| RF05 | Aplicar desconto somente para subtotal ≥ 10000, calculado por `subtotal * desconto_percentual // 100` (arredondar para baixo). |
| RF06 | Dar frete grátis quando o valor **após o desconto** for ≥ 15000; caso contrário cobrar 1500. |
| RF07 | Retornar o total calculado como subtotal − desconto + frete, com valores monetários inteiros. |
| RF08 | Não modificar `itens` nem `estoque` recebidos. |

## Critérios de conclusão

| Código | Evidência objetiva |
|---|---|
| CC01 | Subtotal correto para pedidos com múltiplos itens e quantidades variadas. |
| CC02 | SKU repetido é somado antes da verificação de estoque. |
| CC03 | Quantidade igual ao estoque é aceita; acima é recusada. |
| CC04 | Entradas inválidas especificadas em RF04 geram `ValueError`. |
| CC05 | Desconto aplicado no limite e com arredondamento correto. |
| CC06 | Frete calculado sobre valor após desconto nos limites previstos. |
| CC07 | Total reconcilia corretamente os três componentes. |
| CC08 | Argumentos continuam iguais após a chamada. |

## Exemplos de entrada e saída

```python
processar_pedido([{'sku':'LIVRO','preco_centavos':4000,'quantidade':2}], {'LIVRO':5})
# {'subtotal_centavos':8000, 'desconto_centavos':0, 'frete_centavos':1500, 'total_centavos':9500}

processar_pedido([{'sku':'FONE','preco_centavos':8000,'quantidade':2}], {'FONE':2}, 10)
# {'subtotal_centavos':16000, 'desconto_centavos':1600, 'frete_centavos':1500, 'total_centavos':15900}

processar_pedido([{'sku':'CABO','preco_centavos':1000,'quantidade':2},
                  {'sku':'CABO','preco_centavos':1000,'quantidade':2}], {'CABO':3})
# ValueError (estoque insuficiente)
```

## Restrições

1. Utilizar Python 3.10+ e somente sua biblioteca padrão na solução.
2. Preservar assinatura e campos de retorno de `processar_pedido`.
3. Corrigir `src/pedidos.py`, sem editar os testes para contornar falhas.
4. Não usar resultados fixos ou trocar o contrato da função.
5. Respeitar as regras de uso do Copilot informadas pelo pesquisador.
6. Não compartilhar código ou soluções durante a rodada.
7. Fazer commit aos **15 minutos** e outro aos **25 minutos**, conforme solicitação do pesquisador.

## Como executar

Na pasta `projeto`, execute:

```bash
python -m pip install -r requirements.txt
python -m pytest -q
```

O código entregue tem **defeitos intencionais**, portanto é esperado que testes falhem inicialmente. Seu objetivo é corrigir as causas, não modificar os testes. Os critérios CC01–CC08 serão avaliados para os commits dos 15 e 25 minutos.
