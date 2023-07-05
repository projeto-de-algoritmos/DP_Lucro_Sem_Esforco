# Lucro Sem Esforço (DP)

Objetivo é identificar qualquer ativo de mercado que está precificado muito abaixo ou acima do preço de mercado, simplesmente observando os valores de conversão e encontrando ciclos negativos.

**Número da Lista**: 5 T02<br>
**Conteúdo da Disciplina**: Programação Dinâmica<br>

## Alunos

| Matrícula | Aluno                |
| --------- | -------------------- |
| 180027239 | Renato Britto Araujo |

## Sobre 

### Exemplo

Suponha que o mercado financeiro é um grafo onde cada ativo do mercado é um nó, e cada aresta direcional é o preço de uma transação entre 2 ativos

Imagine que existam moedas (ativos) A, B e C

Você tem 10 unidades de A

Quantos 'A's você precisa pra comprar um 'B' é representado com A/B

A/B  =  2    (B/A = 0.5)
A/C  =  3    (C/A = 0.3333)
B/C  =  1.2  (C/B = 0.8333)

Podemos encontrar um ciclo interessante:
1. Se pegar 10 A -> 3.33 C -> 4 B -> 8.0 A 
2. Se pegar 10 A -> 5 B -> 4.16 C -> 12.5 A

Ou seja, você pode multiplicar a quantidade de 'A' incial em 25% se você pegar o caminho 2.

Isso poderia ser encontrando analiticamente levando em conta que:
 B/A   *  C/B   *   A/C    = 1.25 (> 1.0)
(A->B)   (B->C)    (C->A)

 C/A   *  B/C   *   A/B    = 0.80 (< 1.0)
(A->C)   (C->B)    (B->A)

Ou seja, se analisarmos algum ciclo que começa e termina em algum nó sendo que a fração final de transação é `> 1`, temos um "ciclo infinito" de dinheiro, no sentido de que seria vantajoso colocar a maior quantidade de recursos possíveis por esse ciclo.

Se o mercado fosse perfeitamente eficiente, nenhum conversão desse tipo por definição jamais resultaria em algum valor diferente de 1. Ou seja, são falhas de mercado.

### Solução

Suponha que G é um grafo onde cada ativo do mercado é um nó, e cada aresta direcional é o preço de uma transação entre 2 ativos.

Imaginemos uma árvore V a partir de um grafo G, onde cada aresta de V representa a quantidades de 'A' que seria possível ser convertida a partir de 1 unidade do ativo atual (claramente, o nó do ativo A resultaria em 1 unidade do próprio A).

Para fica claro, o grafo G no exemplo mostrado acima seria:

```
Nós: 
- A
- B
- C

Arestas:
- A - B: 2    
- A - C: 3    
- B - C: 1.2    
- B - A: 0.5
- C - A: 0.3333
- C - B: 0.83333
```

Agora o grafo V

```
Nós: nodes(G)

Arestas:
- A -> A: 1
- A -> B: 1
- A -> C: 1
- B -> A: 1
- B -> B: 1
- B -> C: 1.083331666
- C -> A: 1
- C -> B: 0.9
- C -> C: 1
```

Note como é possível precificar, em termos de 'A' essa conversão de 'B' pra 'C' e de 'C' pra 'B'.

No caso:
- existe um ganho de valor quando conversão 'B' pra 'C' é realizada de 8,3%
- existe uma perda de valor quando conversão 'C' pra 'B' é realizada de -10%

Podemos pegar o esse valor de cada aresta em V e simplesmente converter em perda ou ganha percentual. Ficaria:

```
Nós: nodes(G)

Arestas:
- A -> A: 0.0%
- A -> B: 0.0%
- A -> C: 0.0%
- B -> A: 0.0%
- B -> B: 0.0%
- B -> C: 8.3332%
- C -> A: 0.0%
- C -> B: -10.0%
- C -> C: 0.0%
```

Vamos desenhar pra ficar super óbvio o que está acontecendo aqui.

| Rota             | Grafo                                                   |
| ---------------- | ------------------------------------------------------- |
| A -> C -> B -> A | <div style="width:200px"><img src="figs/Screenshot%20from%202023-07-05%2010-56-05.png"></div> |
| A -> B -> C -> A | <div style="width:200px"><img src="figs/Screenshot%20from%202023-07-05%2011-00-07.png"></div> |

Com isso, a solução fica clara:
1. Calcular o grafo V
2. Transforma todos os valores do grafo acima em seu negativo (`x := - x`, de forma que o ciclo negativo seja o ciclo lucrativo)
3. Encontra o maior ciclo negativo para cada ativo em sua carteira pode fazer parte
4. Realize as transações!

### Objetivo do sistema

Vamos modelar esse fenômeno seguindo algumas regras

Assumimos que:
- Mercado é um grafo onde cada ativo do mercado é um nó, e cada aresta direcional é o preço de uma transação entre 2 ativos. 
- Não existe custo de transação 
  - pra simplificar, senão o mercado não teria ciclos negativos
  - se tivesse, alguém iria perceber e "abusar" deste o mais rápido possível
  - e os vendedores de cada um dos ativos no ciclo negativo iria aumentar o preço de venda para lucrar com o ciclo, de forma a destruir o próprio ciclo
  
Programa:
1. Se houverem dados baixados, pule o próximo passo
2. Baixa dados de ativos por APIs públicas pela taxa de conversão entre eles
   - Exemplo:
     - $ 50,00 (dólares) por 1 barril de petróleo
     - 0,03 Bitcoin por 1 ação de empresa X
     - 6 ações da empresa X por 1 barril de petróleo
     - $ 120.000,00 (dólares) por ₿ 1 (bitcoin).
3. Atribua valor incial pra carteira (eg. $ 50 dólares)
4. Mercado virtual com preços virtuais é atualizado
5. Monta ou atualiza grafo onde cada nó é um ativo, e cada aresta direcionada é o preço de compra de um ativo custando X de outro ativo
6. Rodar um algoritmo detector de ciclos negativos, todo os novos ciclos são guardados
7. Completar um ciclo inteiro para cada ativo que possuir na carteira, usando o ciclo mais lucrativo. **Apenas um ciclo por ativo**.
8. Repetir passo 4
9. <div style="width:100px"><img src="figs/problem.jpg"></div>

## Screenshots

## Vídeo


## Instalação 
**Linguagem**: Python<br>
**Framework**: <br>

O arquivo que monta dataset `get_ativos.py` original usa uma API key do `polygon.io`.
Sem essas chaves, não dá pra puxar dados, mas eles já são carregados por padrão ao executar o app.

## Uso 


## Outros

