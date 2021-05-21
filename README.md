# iti-project-1

> Primeiro projeto da disciplina de Introdução à Teoria da Informação,
> cujo o objetivo é implementar um compressor e descompressor utilizando o algoritmo LZW.

## Equipe

[Lucas Moreira](https://github.com/lucasmsa), [Marismar Costa](https://github.com/marismarcosta), [Gustavo Eraldo](https://github.com/EraldoCi)

## Introdução

## Metodologia

Para realizar tanto a compressão como compressão dos dados é necessário
se atentar à: modo de leitura dos arquivos, incialização do dicionário e tamanho do dicionário.
Tendo isso em vista, para o primeiro caso foi estabelicido que todos arquivos
devem ser lidos no modo binário, assim, facilita a leitura de qualquer tipo de
arquivo.
O dicionário é inicializado, em ambos os modos de operação, com
os 256 símbolos da tabela [ASCII](https://www.rapidtables.com/code/text/ascii-table.html).

Já o tamanho mínimo do dicionário será $$ 2^{9} = 512 $$ bits. O _K_ é um
parâmetro de entrada, pois deseja-se observar o comportamento da **razão de compressão**
ao variar o tamanho do dicionário e dada uma mesma entrada. _K_ pode estar no
intervalo $$ 9 <= K <= 16 $$.

## Resultados

## Considerações finais
