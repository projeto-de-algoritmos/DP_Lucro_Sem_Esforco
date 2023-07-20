# Lucro Sem Esforço (DP)

Objetivo é identificar qualquer ativo de mercado que está precificado muito abaixo ou acima do preço de mercado, simplesmente observando os valores de conversão e encontrando ciclos negativos.

**Número da Lista**: 5 T02<br>
**Conteúdo da Disciplina**: Programação Dinâmica<br>

## Alunos

| Matrícula | Aluno                |
| --------- | -------------------- |
| 180027239 | Renato Britto Araujo |

## Sobre 

Aprecie essa imagem:

![](figs/Screenshot%20from%202023-07-05%2022-29-57.png)

O mercado financeiro pode ser muito feio ou muito bonito, dependendo de como você observa ele.

Vamos tentar observar ele de uma forma bonita nesse projeto.

### Entendendo o problema

Suponha que o **mercado financeiro é um grafo** onde cada ativo do mercado é um nó, e cada aresta direcional é o preço de uma transação entre 2 ativos

Imagine que existam moedas (ativos) A, B e C. Você tem 10 unidades de A. Quantos 'A's você precisa pra comprar um 'B' é representado como A/B.

A/B  =  2    (B/A = 0.5)
A/C  =  3    (C/A = 0.3333)
B/C  =  1.2  (C/B = 0.8333)

Podemos encontrar um ciclo interessante:
1. Se pegar 10 A -> 3.33 C -> 4 B -> 8.0 A 
2. Se pegar 10 A -> 5 B -> 4.16 C -> 12.5 A

Ou seja, você pode multiplicar a quantidade de 'A' incial em 25% se você pegar o caminho 2.

Isso poderia ser encontrando analiticamente levando em conta que:
 B/A   *  C/B   *   A/C    = 1.25 (> 1.0)
 C/A   *  B/C   *   A/B    = 0.80 (< 1.0)

Ou seja, se analisarmos algum ciclo que começa e termina em algum nó sendo que a fração final de transação é `> 1`, temos um **"ciclo infinito" de dinheiro**, no sentido de que seria vantajoso colocar a maior quantidade de recursos possíveis por esse ciclo.

Se o mercado fosse perfeitamente eficiente, nenhum conversão desse tipo por definição jamais resultaria em algum valor diferente de 1. Ou seja, são falhas de mercado.

### Solucionando o problema

Suponha que G é um grafo onde cada ativo do mercado é um nó, e cada aresta direcional é o preço de uma transação entre 2 ativos.

Se nós conseguirmos achar qualquer caminho em G onde nós partimos de 'A', realizamos sucessivas compras terminando em 'A' de forma que o resultado final seja maior que 1 (compramos X > 1 unidades de A a partir de 1 única unidade), temos um ciclo.

Note como o valor X não faz diferença, desde que exista algum caminho mais rentável que 1 A.

Para fica claro, o grafo G no exemplo mostrado acima seria:

```
Nós: 
- A
- B
- C

Arestas:
- A - B: 2    
- A - C: 3    
- B - C: 1.25  
- B - A: 0.5
- C - A: 0.3333
- C - B: 0.8
```

Vamos explorar *parcialmente* esse grafo cíclico começando pelo A e terminando em A.

Um algoritmo imaginado será usado à seguir. 

É parecido com um dijkstra, mas o valor intermediário de qualquer passo é irrelevante sem se saber qual é o valor final de A que é possível se comprar. 

Portanto, não temos como saber qual é o melhor caminho sem explorar os subcaminhos, mas nenhum subcaminho é ignorável, algo que um simples dijsktra não poderia fazer:

```
[COMPRA]  com 1 A compramos 0.5 B
[COMPRA]  com 1 A compramos 0.333 C
[COMPRA]  com 0.333 C compramos 0.41625 B
[DISPUTA] a quantidade de B é max(0.5, 0.41625) = 0.5
[COMPRA]  com 0.5 B compramos 0.4 C
[DISPUTA] a quantidade de C é max(0.333, 0.4) = 0.4
[COMPRA]  com 0.4 C compramos 1.2 A
```

Note como conseguimos comprar 1.2 A a partir de 1 A! 20% de **lucro, sem nenhum esforço**!

Além disso, toda vez que ocorre uma **disputa** no valor de algo, por exemplo no caso de B ou C, temos um erro no mercado que faz a paridade daquele ativo contigo mesmo ser diferente de 1:1. Se for possível comprar e vender aquele ativo em termos de A, é possível lucrar com ele.

A **estratégia ideal** seria realizar o **infinitas compras** desse ciclo.

### Tornando o problema mais interessante

Suponha agora que seja possível apenas **comprar ou vender** algum ativo **apenas uma única vez**, como se o estoque tivesse sido interamente comprado na loja. 

Como **nenhum nó pode ser revisitado**, o ciclo não pode ter infinitos passos.

Portanto, apenas uma solução, a melhor, deveria ser encontrada ao final desse processo.

Isso seria equivalente a um grafo direcionado: se você está no B, a subárvore dele não pode conter outro B. A única subárvore que pode conter outra instância de se própria é o A, que também é a raíz da árvore.

Quando uma **disputa é encontrada**, estamos escolhendo qual ramo da árvore vamos **explorar**, e qual **abandonar**.

Se computarmos dessa forma, é como se pudessemos **comparar o resultado de subproblemas** de múltiplas subárvores simultâneamente, tornando o resultado de outras subárvores inferiores em redundantes. 

Resumo rápido do que temos:
- Múltiplos problemas sobrepostos
- Reutilização de resultados
- Substruturas ótimas
- Evita redundância

Isso... é programação dinâmica!

### Objetivo do sistema

Vamos modelar esse fenômeno seguindo algumas regras

Assumimos que:
- Mercado é um grafo onde cada ativo do mercado é um nó, e cada aresta direcional é o preço de uma transação entre 2 ativos. 
- Não existe custo de transação 
  - pra simplificar, senão o mercado não teria ciclos negativos
  - se tivesse, alguém iria perceber e "abusar" deste o mais rápido possível
  - e os vendedores de cada um dos ativos no ciclo negativo iria aumentar o preço de venda para lucrar com o ciclo, de forma a destruir o próprio ciclo
- Todo ativo vale 1 de si mesmo

O algoritmo se encontra no arquivo `src/grafo.py`.

## Screenshots


### Um grafo aleatório com ciclo de lucro gerado pelo app

![](figs/Screenshot%20from%202023-07-05%2022-27-28.png)


Interpretação:
- COR VERMELHA REPRESENTA NÓ INICIAL
- COR VERDE REPRESENTA CAMINHO DE LUCRO OTIMO
- O CUSTO DE SE COMPRAR 1 UNIDADE DO ATIVO QUE RECEBE A SETA É SEU PESO, A "GORDURA" DA ARESTA
- Os simbolos a seguir são as moedas USD = Dolar, BTC = Bitcoin, EUR = Euro...

### Outro grafo aleatório com ciclo de lucro gerado pelo app 

![](figs/Screenshot%20from%202023-07-05%2022-27-51.png)

### Output local 

![](figs/Screenshot%20from%202023-07-05%2022-05-58.png)


## Vídeo

https://github.com/projeto-de-algoritmos/DP_Lucro_Sem_Esforco/blob/master/video.mp4

## Instalação 
**Linguagem**: Python<br>
**Framework**: <br>

O arquivo que monta dataset `get_ativos.py` original usa uma API key do `polygon.io`.
Sem essas chaves, não dá pra puxar dados, mas eles já são carregados por padrão ao executar o app.

## Uso 

Para rodar localmente:
```
python app.py local
```

Para rodar no browser, com visualização:
```
python app.py
```
E então acesse [http://localhost:8000](http://localhost:8000)


