A ideia da pasta de domain é ter os dados crus minimamente tratados.
Para esse projeto especificamente, acho que vamos precisar de algumas bases:


## Balanço
Base simples com os resultados finais de cada mes em cada CONTA CORRENTE
Por questões especificas, eu tenho varias contas em alguns paises, então é util ter esses detalhes

| DATA | NOME_CONTA | VALOR | MOEDA | NOME_PAIS


## Movimentos
Basicamente uma base de cashflow para cada conta. Idealmente, montaremos a base de BALANCO a partir dessa base. Para investimentos, eles devem entrar apenas quando realizados

| DATA | NOME_MOVIMENTO | CATEGORIA_MOVIMENTO | NOME_CONTA | VALOR | MOEDA


## Portfólio
Mes a mes a foto de cada investimento, seu rendimento e valor aplicado


## Orçamento
Planejamento. Vai ser usado para as projeções de custo quando não tivermos dados atuais.
Teremos tanto custos mensais como possiveis compras que ainda não foram realizadas (exemplo, TV aqui no apt novo de Amsterdam ou compra de um APT no futuro quando voltarmos para São Paulo)


Acho que juntando tudo isso, da pra fazer projeções e comparações interessantes, mas é preciso ter isso primieiro
