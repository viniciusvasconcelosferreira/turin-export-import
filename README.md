# Script de Processamento dos Dados de Exportação e Importação do Brasil - 2022

Este script foi desenvolvido como parte da fase 2 do processo seletivo da Turin para a vaga de Analista de Processamento de Dados Júnior. O objetivo deste programa é gerar arquivos CSV separados por estado a partir de dados de exportação e importação. Ele processa os dados fornecidos em arquivos CSV ou por meio de links da web e cria arquivos separados para cada estado, contendo as informações agregadas.

## Requisitos

- Python 3.x
- Pandas (pode ser instalado com `pip install pandas`)

## Uso

1. Clone este repositório ou faça o download do arquivo `main.py`.
2. Certifique-se de que possui uma conexão com a internet para baixar os dados, caso esteja usando links da web.
3. No código, você pode ajustar as seguintes variáveis:

   - `link_exp`: Link para o arquivo CSV de exportação (caso `path_exp` não seja fornecido).
   - `link_imp`: Link para o arquivo CSV de importação (caso `path_imp` não seja fornecido).
   - `path_exp`: Caminho para o arquivo CSV de exportação (se disponível localmente).
   - `path_imp`: Caminho para o arquivo CSV de importação (se disponível localmente).
   - `path_result`: Caminho para o diretório onde os arquivos de saída serão salvos. Se não for fornecido, os arquivos serão salvos no diretório atual.

4. Execute o programa com o comando `python main.py`.

5. Após a execução bem-sucedida, arquivos CSV separados para cada estado serão gerados no diretório especificado em `path_result` ou no diretório atual.

## Observações

- Se tanto `path_exp` quanto `path_imp` forem fornecidos, o programa usará os arquivos locais. Caso contrário, baixará os arquivos usando os links da web fornecidos.
- Certifique-se de que os arquivos de entrada estejam no formato CSV e sigam a estrutura correta (delimitador `;` e cotação `1`).