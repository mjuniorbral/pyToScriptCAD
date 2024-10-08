# pyToScriptCAD

Um módulo para elaboração de scripts para automação da elaboração de arquivo dwg

## Descrição do Autor

Programa escrito por Marcelo Cabral dos Santos Junior

Analista Técnico de Engenharia Civil na GEOCOBA - Projetos de Engenharia (https://www.geocoba.com/)

Contato: mjuniorbral@gmail.com (pessoal)

## Descrição das dependências

Versão utilizada do Python: 3.10.11

Módulos utilizados nativos do Python (não precisa de instalação):

- unicodedata
- os
- inspect
- time

Módulos externos utilizados (instalados através do pip install obtido no Microsoft Store junto com o Python 3.10.11):

- pandas (1.5.3): utilizado pra abrir e importar a planilha de entradas da sondagem // Instale usando o comando ´pip install pandas´

Versão utilizada do Autocad: S.51.0.0 Autodesk AutoCAD LT 2022 (Product Version visto no Menu Help > About)

*Não tem opções que envolvam o eixo Z (para autocad 3D, não irá funcionar - a menos que tenha uma alteração dos script com adição das coordenadas Z=0)*

## Estrutura de arquivos e pastas necessária
- /.
- /main.py
- /functions.py
-  /classes.py
- /models.py
- /Modelo de Entrada Log Sondagem.xlsx      (modelo da planilha de entrada)
- /in/
- /in/planilhaEntrada.xlsx     (planilha de entrada preenchida precisa ser posta aqui antes de inicializar o programa)
- /out/

## Notas das atualizações
Data/Hora de início do desenvolvimento: 07/06/2024 10h00
- Versão 0.0.1 - 07/06/2024 - Implementação das classes básicas de funcionamento do programa.
- Versão 0.0.2 - 20/06/2024 - Definição da arquitetura de software e finalização de algumas implementações.
- Versão 0.0.3 - 29/07/2024 - Correções de bugs: - traço não estava sendo computado nas colunas de classificação de rochas
- Versão 0.1.0 - 14/08/2024 - Nova versão do progrma com atualização do modelo de sondagem
  - Novo modelo requisitado pela CCR,
  - Módulo models totalmente reformulado (modelo anteriores de log de sondagem foi totalmente descontinuado nessa versão),
  - correção de bugs,
  - implementação do BLOCKALL no método Script.compileScript (transformar tudo em um bloco com (0,0) como origem),
  - atualização do modelo da planilha de entrada,
  - adição de parâmetros na tabela de Configurações na planilha de entradas para deixar a geração do log mais personalizável,
  - Adicionado o tempo de execução,
  - Implementação dos critérios de parada de forma explícita na entrada,
  - Implementação de criação de pastas in e out caso não tenham,
  - Criação de mais estilos de texto simplex com widthFactor diferentes,
  - Estruturação da classe do modelo foi aprimorada deixando comentários para clarear o código,
  - Aprimorado a geração de log (terminal) para acompanhamento da execução do programa.
- Versão 0.1.1 - 16/08/2024 - Implementação das cores baseado no novo CTB da CCR
- Versão 0.1.2 - 28/08/2024 - Correção do posicionamento dos valores de Recuperação e RQD (alteração no arquivo models.py no método LogSondagem.criarElementos)

## Como usar o programa?
1. Garantir que as versões do python, autocad e módulo pandas estão compatíveis com esse projeto (não precisa ser a mesma versão, mas precisa ser compatível - na dúvida, rode o programa, e se não der erro, a princípio é compatível);
2. Preencher a planilha modelo com as informações da sondagem;
3. Nomear a aba/planilha do arquivo excel igual ao nome da sondagem apresentada na própria planilha;
4. Criar quantas abas quiser para quantas sondagens for preciso;
5. Se não tiver criado, criar uma pasta de nome "in" (tudo minúsculo) e uma de nome "out" (tudo minúsculo) na mesma pasta onde está o arquivo "main.py" (conforme estrutura de arquivos e pastas citado anteriormente);
6. Mover a planilha de entrada preenchida para a pasta "in";
7. Em seguida, executar o programa "main.py" no terminal usando o python3;
8. Os scripts irão ser gerados, por padrão, na pasta "out";
9. Existem outras formas de usar esse programa, mas ele está configurado para ser fixo com as sondagens.
10. qualquer dúvida, meu contato está disponível para envio de mensagens.
