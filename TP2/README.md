# Trabalho Prático 2 (Implementação de um ray tracer)

- Aluno: Thiago Martin Poppe
- Matrícula: 2017014324
<br>

## 1) Introdução
- Foi utilizado o livro _Ray Tracing in One Weekend_, do Peter Shirley, para a implementação desse ray tracer escrito em Python 3. Utilizo a ideia das classes e código tal qual está presente no livro, com a diferença de que a cena final gerada possui 200 esferas ao invés de 500. Optei por menos esferas apenas por conta do tempo de execução, visto que o código foi implementado em Python ao invés de C++. No entanto, mesmo com menos esferas, o resultado final é bastante interessante e condiz com a imagem esperada.
<br><br>
- Fora as bibliotecas padrões do Python, utilizo a biblioteca numpy para fazer cálculos envolvendo vetores, visto que, não implemento a classe _vec3_.
<br><br>
- Foi implementado os efeitos de Depth of Field, tais quais visto em sala, e também o de anti-aliasing que promove uma imagem mais suave e menos serrilhada. Modifiquei a função do livro que retorna um ponto aleatório em uma esfera unitária para a função vista em sala de aula, que não utiliza o método de rejeição, fazendo com que o código seja um pouco mais rápido.
<br><br>
- Para utilizar o código, devemos passar como argumento o nome do arquivo de saída com a terminação .ppm na hora da execução do mesmo. Também podemos passar como parâmetros opcionais as dimensões da imagem a ser gerada (largura e altura, respectivamente). Caso não sejam passadas as dimensões, o valor default será 340x480. Optei também por passar um 4º parâmetro opcional que será o número de esferas pequenas geradas na cena final. Caso não seja passado esse número, o valor padrão será de 200 esferas.
<br><br>
- No total temos 7 classes implementadas (retirando as classes abstratas), as quais explicarei a seguir.

## 2) Classes
### 2.1) Ray
- A classe Ray será responsável por modelar os nossos raios disparados. Nela, temos como parâmetros o ponto de origem do raio, bem como a sua direção. Implementamos também uma função que dado um parâmetro _t_ retorna um ponto pertencente ao raio. Usaremos essa função para sabermos o ponto de interseção com os objetos em nossa cena.

### 2.2) Camera
- A classe Camera será responsável por modelar a nossa câmera na cena. Nela, temos como parâmetros o ponto de origem da mesma, bem como para onde estaremos olhando, orientação vertical, field of view (também conhecido como _fov_), o "aspect ratio" (em outras palavras, a "proporção da tela", e.g 16:9), a abertura da lente da câmera e a distância focal da mesma. Esses dois últimos parâmetros são os responsáveis pelo efeito de Depth of Field presente em várias câmeras reais.
<br><br>
- Na classe, temos também uma função que dispara os raios para realizar o processo de Ray Tracing, com nome de shoot\_ray, que recebe como parâmetros as coordenadas _u_ e _v_ (no caso do programa, _s_ e _t_) que indicam onde iremos disparar o raio.
<br><br>
- Para finalizar, temos uma função auxiliar que escolhe aleatóriamente um ponto em um círculo (ou disco) unitário, a qual usaremos para realizar o efeito de Depth of Field. O livro implementa tal função utilizando o método de rejeição, que consiste em basicamente escolher um ponto aleatório e verificar se o mesmo pertence ao círculo ou não. Optei por modificar essa função para retornar valores de raio e ângulo que obtemos com o método de inversão da CDF (cumulative distribution function, ou no português: função distribuição acumulada), tornando assim essa parte um pouco mais rápida.

### 2.3) Sphere
- A classe Sphere será responsável por modelar as esferas presentes na cena. Nela, temos como parâmetros a posição do centro, o raio e o tipo de material da mesma, que pode ser lambertiano (difuso), metal (especular) ou vidro (dielétrico).
<br><br>
- Na classe, temos também uma função _hit_ que indica se um raio atingiu uma esfera e quais são os pontos. Para realizar esse cálculo, basta resolvermos uma equação de segundo grau e computar o parâmetro _t_ dado essa equação.
<br><br>
- Para finalizar, temos uma função auxiliar que escolhe aleatóriamente um ponto em uma esfera unitária, a qual usaremos para indicar a direção do raio de saída. O livro implementa tal função também utilizando o método de rejeição. Optei por modificar essa função tal qual foi explicado na parte da classe Camera.

### 2.4) HitableList
- A classe HitableList será responsável por guardar uma lista de instâncias dos objetos da cena.
<br><br>
- Na classe, temos também a função _hit_ que indica se um raio atingiu um objeto e quais são os pontos.

### 2.5) Lambertian
- A classe Lambertian será responsável por modelar materiais lambertianos, ou difusos. Nela, temos como parâmetro a cor do objeto no formato RGB (vermelho, verde e azul, respectivamente).
<br><br>
- Na classe, temos também uma função _scatter_ que modela como o raio se comportará dado esse material. No caso de um objeto lambertiano, temos que o raio disperso terá origem no ponto de interseção e direção igual a soma do ponto e normal no local de interseção mais um ponto aleatório em uma esfera unitária. Já a atenuação será igual ao albedo do objeto, i.e a cor do mesmo. Para esse tipo de material, temos que os raios sempre serão dispersados.

### 2.6) Metal
- A classe Metal será responsável por modelar materiais metálicos, ou especulares. Nela, temos como parâmetros a cor do objeto no formato RGB e a porcentagem de _fuzz_, ou seja, o quão "embaçado" será a reflexão.
<br><br>
- Na classe, temos também a função _scatter_ que modela como o raio se comportará dado esse material. No caso de um objeto metálico, temos que computar o raio refletido. Para tal, usamos a fórmula _v - 2 * dot(v, n) * n_, onde _v_ representa o raio de entrada e _n_ a normal da superfície. Sendo assim, temos que o raio disperso terá origem no ponto de interseção e direção igual ao raio refletido mais um ponto aleatório em uma esfera unitária vezes a quantidade de _fuzz_. Isso faz com que tenhamos uma reflexão "embaçada" a depender da quantidade de _fuzz_ que colocamos para a superfície. Já a atenuação será igual ao albedo do objeto. Para dizer se um raio será dispersado ou não, temos que isso será igual a expressão booleana _dot(dir, normal) > 0_, onde _dir_ representa a direção do raio dispersado.

### 2.7) Dielectric
- A classe Dielectric será responsável por modelar materiais dielétricos, a exemplo do vidro. Nela, temos como parâmetros o índice de refração do objeto.
<br><br>
- Na classe, temos também a função _scatter_ que modela como o raio se comportará dado esse material. No caso de um objeto dielétrico, isso já é um pouco mais complicado. Resumindo, utilizamos a Lei de Snell, que estabelece uma relação entre o ângulo de incidência de um raio e a refração do mesmo, para modelar a refração no nosso objeto. Aliado a isso, também utilizamos a aproximação de Schlick, que é amplamente usada em computação gráfica para aproximar a contribuição do fator de Fresnel (reflexão e transmição de luz) na reflexão especular de luz de uma superfície não condutora, em outras palavras, dielétrica.

# 3) Resultados obtidos
- A imagem final gerada com nome final_scene.png possui tamanho 320x240 com 200 esferas pequenas espalhadas pela cena, 1 esfera de cada material (difuso, especular e dielétrico) e 1 esfera grande que representa o chão. Como dito na introdução, optei por gerar menos esferas apenas para diminuir o tempo necessário na espera da execução do código, visto que implementamos em Python3 que por si só já é mais lento que C++, que foi a linguagem que o livro utilizou.
<br><br>
- Além da imagem final, gerei imagens para cada novo passo que dei no livro (todas com tamanho 200x100) e também a cena final sobre um outro ângulo de visão, modificando a posição da câmera. Essa cena, por sua vez, possui 200 esferas e tamanho 320x240.
<br><br>

# 4) Extras
- Com o adiamento do trabalho prático, implementei um motion blur na cena final. Basicamente, cada esfera agora possui um atributo _bounce_, que indica se ela tem a propriedade de quicar, e a sua velocidade. Usamos a velocidade para modificar a posição do centro da esfera e em seguida modificamos sua velocidade usando um vetor _gravity_ que basicamente vai diminuindo a velocidade aos poucos, até a mesma ficar negativa. Ao chegarmos no chão, voltamos a velocidade para o seu valor inicial, fazendo com que a esfera sofra um "impulso", retornando assim para o seu movimento vertical. Note que essa colisão será perfeitamente elástica, ou seja, a nossa esfera ficará quicando para sempre.