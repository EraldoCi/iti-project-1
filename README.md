# lzw-algorithm

> Primeiro projeto da disciplina de Introdução à Teoria da Informação,
> cujo o objetivo é implementar um compressor e descompressor utilizando o algoritmo LZW.

## Equipe

[Lucas Moreira](https://github.com/lucasmsa),
[Marismar Costa](https://github.com/marismarcosta),
[Gustavo Eraldo](https://github.com/EraldoCi)

## Introdução

Inventado por Lempel e Ziv, o LZW é um algoritmo de compressão baseado
em dicionário (também conhecido como _factor substitution_), que consiste em
substituir uma sequência de caracteres (ou _factor_) por um código mais curto que
o índice desse no dicionário.

Em geral, a objetivo do LZW é obter uma redução da entropia, não apenas em um único caracter, mas em todas as palavras.

A seguir é apresentado o [pseudocódigo do algoritmo de compressão e descompressão LZW](https://www.amazon.com/Foundations-Coding-Compression-Encryption-Correction/dp/1118881443).

### Algoritmo de compressão

```py
word="";
while not end of file;
    x=read next character;
    if word+x is in the dictionary
        word=word+x;
    else
        send the dictionary number for word
        add word +x to the dictionary
        word=x
end of while loop
```

### Algoritmo de descompressão

```py
read a character x from compressed file;
write x to uncompressed version;
word=x;

while not end of compressed file do begin
    read x
    look up dictionary element corresponding to x;
    output element
    add w + first char of element to the dictionary
    w  = dictionary element
endwhile
```

## Metodologia

Para realizar tanto a compressão quanto descompressão dos dados é necessário
se atentar ao modo de leitura dos arquivos, além da incialização e tamanho do dicionário.

Tendo isso em vista, para o primeiro caso foi estabelecido que todos arquivos
devem ser lidos no modo binário, assim, facilitando a leitura de qualquer tipo de
informação, seja texto, imagem ou vídeo.

O dicionário é inicializado, em ambos os modos de operação, com
os 256 símbolos da tabela [ASCII](https://www.rapidtables.com/code/text/ascii-table.html).

Por outro lado, o tamanho mínimo do dicionário será 2^9 = 512 bits. O _K_ é considerado um
parâmetro de entrada, com o intuito de observado o comportamento da **razão de compressão**
ao variar o tamanho do dicionário e dada uma mesma entrada. Além disso, o _K_ deve estar no intervalo 9 <= _K_ <= 16.

Para realizar a análise do comportamental do LZW, foram disponibilizados dois
arquivos em formato de texto e vídeo: [corpus16MB.txt](/data/test/) e
[disco.mp4](/data/test/) repectivamente.

Em relação ao algoritmo de compressão, foi realizada uma alteração na pesquisa
de palavras existentes, de modo que se pesquisa a maior
sequência presente no dicionário. Assim, o algoritmo de compressão tem
o seguinte funcionamento:

```py
indice = 0;

Enquanto != fim da mensagem, faça:
    simb_atual = mensagem[indice]
    prox_simb = mesagem[indice+1]

    Enquanto (simb_atual + prox_simb) estiver no dicionário:
        simb_atual = (simb_atual + prox_simb)

        Se (simb_atual + prox_simb) não estiver no dicionário:
            adiciona (simb_atual + prox_simb) no dicionário
            mensagem_codificada.append(simb_atual + prox_simb)
        ...
```

<!-- Definir o que é: Razão de compressão -->

<!-- A razao de compressao é uma métrica de desempenho utilizada em algoritmos de compressao para determinar o quão bom é o seu desempenho. RC pode ser calculada da seguinte forma: -->

<!-- RC_ideal = tamanho do arquivo original / tamanho arquivo compactado -->

<!--Contudo, caso você não consiga gerar o arquivo compactado exatamente com a quantidade de bytes correta, você pode estimar o tamanho do arquivo compactado com sendo: (quantIndices*k)/8. -->

## Análise de resultados

### Arquivo de texto

Foram utilizados dois arquivos para analisar o comportamento do LZW. Então, logo abaixo são apresentados a: **razão de compressão**, **quantidade de índices por K** e **tempo de processamento por K** para o arquivo corpus16MB.txt.

<p align="center">
  <img width="600px" src="./results/corpus/compression_rate_x_k.png">
  <img width="600px" src="./results/corpus/indices_x_k.png">
  <img width="600px" src="./results/corpus/time_x_k.png">
</p>

No gráfico de razão de compressão é notório o aumento da razão de compressão
a medida que é incrementado o _K_.

No segundo gráfico pode ser observado que q quantidade de índices necessários para
codificar a mensagem aumenta a medida que é incrementado o valor de _K_. E, este resultado é condizente com o **esperado**, pois quanto maior o dicionário, mais
sequências serão salvas e consequentemente uma menor quantidade de índices serão
necessários.

Já em relação ao tempo de processamento após variar o _K_, é possível observar
que o tempo de execução é maior para valores de _K_ menores que 12.

### Arquivo de vídeo

Já em relação aos resultados com o arquivo de vídeo, é possível observar os
comportamentos abaixo.

<p align="center">
  <img width="600px" src="./results/video/compression_rate_x_k.png">
  <img width="600px" src="./results/video/indices_x_k.png">
  <img width="600px" src="./results/video/time_x_k.png">
</p>

Na razão de compressão por K, a resposta gráfica é

Assim como o resultado obtido para o arquivo de texto, o gráfico índices
por _K_ se comporta da mesma forma.

## Considerações finais
