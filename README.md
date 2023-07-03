# Lucro Sem Esforço

Objetivo é identificar qualquer ativo de mercado que está precificado muito abaixo ou acima do preço de mercado, simplesmente observando os valores de conversão 

Assumimos que:
- O preço do ativo não vai mudar muito radicalmente dentro do período da análise
  - Mas vamos pegar também a taxa de variação média deste ativo para fatorar o risco de se comprar-lo. Quanto mais volátil, mais perigoso. 

Onde estaria o lucro então?
- Note como o estado atual do mercado pode fazer com que algum ativo esteja mal precificado se comparado a outro ativo.
- Se ativo A está barato demais que ativo B se tentasse comprar com uma cadeia de compras `A -> X -> Y -> ... -> Z -> B`, compraríamos ativo B por um preço mais baixo do que custa (será consertado).
  

Se aplicarmos uma `detecção de ciclos negativos`, podemos encontrar um exemplo disso.