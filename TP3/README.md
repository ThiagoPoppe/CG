# Trabalho Prático 3 (Animação utilizando Shape Interpolation)

- Aluno: Thiago Martin Poppe
- Matrícula: 2017014324
<br>

## 1) Introdução
- Foram utilizados os sites http://tfc.duke.free.fr/old/models/md2.htm e http://tfc.duke.free.fr/coding/src/md2.c como referência para a construção do código em Python3 que lê um arquivo .md2, renderiza o modelo utilizando OpenGL (nesse caso, PyOpenGL) e anima o modelo utilizando shape interpolation. Como extra, utilizei um shader previamente feito para realizar uma iluminação no nosso modelo. Optei por utilizar o Phong Shading, e pretendia colocar comandos no teclado para que o usuário escolha o tipo de iluminação feita (flat, gouraud ou phong).


- Para executar o código, basta rodarmos o arquivo ___animation.py___ passando como argumento o caminho para o arquivo .md2 a ser renderizado. Dentro do .zip temos uma pasta __models__ que possui os modelos usados bem como suas texturas em um arquivo .pcx.


- O código utiliza tanto a biblioteca da OpenGL quanto a da GLFW, recomendo ter ambas instaladas para evitar erros.

## 2) Detalhes da implementação
- No código original, o autor implementa uma função que coloca uma textura em nosso modelo. Tentei o mesmo utilizando a biblioteca Pillow para ler o arquivo .pcx contento a textura, porém a OpenGL reportou um erro que aparentemente faltava coordenadas de textura. Provavelmente, fiz alguma coisa errada no shader e decidi deixar essa implementação de lado e focar na implementação da animação em si.


- O código conta com um dicionário contento as possíveis animações do modelo, chamado de animations. Basta definirmos a animação que queremos antes do loop principal do glfw, por exemplo: animations['RUN']. Por padrão, a animação escolhida é a de __STAND__.


- Visto que o código original é em C/C++, o mesmo utiliza fortemente ponteiros para ler o arquivo .md2, que por sua vez é binário. Pelo fato de Python não possuir ponteiros, optei por utilizar a função "unpack" da biblioteca __struct__. Dado uma string em binário, i.e. b'', e uma formatação, a função "converte" os bytes para os tipos desejados. No próprio site usado como referência, o autor mostra o tamanho em bytes de cada tipo, bem como a ordem de leitura dos bytes, que nesse caso é little-endian.

## 3) Resultados obtidos
- O modelo foi renderizado, animado e iluminado com sucesso. Utilizei como teste o modelo Ogros.md2, e inseri na pasta __images__, imagens do modelo renderizado usando os diferentes tipos de shading (flat, gouraud e phong).


- Percebi que a animação fica um pouco lenta algumas vezes. Não sei se foi por conta do Phong Shading, que dos três shadings utilizados é o mais pesado, ou pelo fato de estarmos utilizando Python para implementar tal animação. Percebi que ao mudar o shading a animação fica mais suave, logo, creio que o motivo seja o shader utilizado.