# Lucro Sem Esforço (DP)

Objetivo é identificar qualquer ativo de mercado que está precificado muito abaixo ou acima do preço de mercado, simplesmente observando os valores de conversão e encontrando ciclos negativos.

**Número da Lista**: 5 T02<br>
**Conteúdo da Disciplina**: Programação Dinâmica<br>

## Alunos

| Matrícula | Aluno                |
| --------- | -------------------- |
| 180027239 | Renato Britto Araujo |

## Sobre 

Assumimos que:
- Mercado é um grafo onde cada ativo do mercado é um nó, e cada aresta direcional é o preço de uma transação entre 2 ativos. 
- Não existe custo de transação 
  - pra simplificar, senão o mercado não teria ciclos negativos
  - se tivesse, alguém iria perceber e "abusar" deste o mais rápido possível
  - e os vendedores de cada um dos ativos no ciclo negativo iria aumentar o preço de venda para lucrar com o ciclo, de forma a destruir o próprio ciclo.
- O preço do ativo não vai mudar muito radicalmente dentro do período da análise
  - Mas vamos pegar também a taxa de variação média deste ativo para fatorar o risco de se comprar-lo. Quanto mais volátil, mais perigoso. 
- Um ativo que foi detectado uma vez será detectado de novo, ou seja, se vimos petróleo no ciclo, então é de se assumir que será possível encontrar petróleo de novo.

Onde estaria o lucro então?
- Note como o estado atual do mercado pode fazer com que algum ativo esteja mal precificado se comparado a outro ativo.
- Se ativo A está barato demais que ativo B se tentasse comprar com uma cadeia de compras `A -> X -> Y -> ... -> Z -> B`, compraríamos ativo B por um preço mais baixo do que custa (será consertado).
  
Se aplicarmos uma `detecção de ciclos negativos`, podemos encontrar um exemplo disso.

### Objetivo do sistema

Processo carteira:

0. Monta estado de carteira
   - Incialmente todos os ativos estão igual a zero (apenas um arquivo `.json`).
   - O valor da banca inicial é definido (dólares).
   - Define valor A (fração da banca) pra usar em novas "apostas".
1. Monitora estado dos ciclos negativos
2. Se algum ciclo negativo novo de compra ser detectado, compra `A` valor do ativo e guarda esse ciclo para análise futura.
3. Se algum ciclo negativo novo de venda ser detectado de um ativo que **já está na carteira**, vende `A` valor do ativo por outro ativo.

Processo dados:

1. Baixa dados de ativos por APIs públicas pela taxa de conversão entre eles
   - Exemplo:
     - $ 50,00 (dólares) por 1 barril de petróleo
     - 0,03 Bitcoin por 1 ação de empresa X
     - 6 ações da empresa X por 1 barril de petróleo
     - $ 120.000,00 (dólares) por ₿ 1 (bitcoin).
2. Monta ou atualiza grafo onde cada nó é um ativo, e cada aresta direcionada é o preço de compra de um ativo custando X de outro ativo.
3. Rodar um algoritmo detector de ciclos negativos, todo os novos ciclos são guardados.
4. Repetir passo 1.


## Screenshots

## Vídeo


## Instalação 
**Linguagem**: Python<br>
**Framework**: <br>

## Uso 


## Outros

