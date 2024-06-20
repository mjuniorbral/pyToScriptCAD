# -*- coding: utf-8 -*-

# Programa escrito por Marcelo Cabral dos Santos Junior
# Analista Técnico de Engenharia Civil na GEOCOBA - Projetos de Engenharia (https://www.geocoba.com/)
# Contato: msj@geocoba.com (profissional), mjuniorbral@gmail.com (pessoal)

# Versão utilizada do Python: 3.10.11

# Módulos utilizados nativos do Python (não precisa de instalação):
# - unicodedata
# - os
# - inspect

# Módulos externos utilizados (instalados através do pip install obtido no Microsoft Store junto com o Python 3.10.11):
# - pandas (1.5.3): utilizado pra abrir e importar a planilha de entradas da sondagem

# Versão utilizada do Autocad: S.51.0.0 Autodesk AutoCAD LT 2022 (Product Version visto no Menu Help > About)
# Não tem opções que envolvam o eixo Z (para autocad 3D, não irá funcionar - a menos que tenha uma alteração dos script com adição das coordenadas Z=0)

# Estrutura de arquivos e pastas necessária
# --/.
# --/main.py
# --/functions.py
# --/classes.py
# --/models.py
# --/Modelo de Entrada Log Sondagem.xlsx      (modelo da planilha de entrada)
# --/in/
# --/in/planilhaEntrada.xlsx     (planilha de entrada preenchida precisa ser posta aqui antes de inicializar o programa)
# --/out/

# Data/Hora de início do desenvolvimento: 07/06/2024 10h00
# Versão 0.0.1 - 07/06/2024 - Implementação das classes básicas de funcionamento do programa.
# Versão 0.0.2 - 20/06/2024 - Definição da arquitetura de software e finalização de algumas implementações.

from classes import *
from models import *
from functions import *

pastaEntradas = 'in\\'
pastaSaidas = 'out\\'

if __name__=="__main__":
    # nomeSondagem = "SM-481.19" # O nome da planilha deve ser o mesmo do nome da sondagem apresentada na planilha
    # nomeArquivo = "Entrada Log Sondagem.xlsx"
    for caminhoPlanilhaEntrada in get_all_files_in_directory(pastaEntradas):
        for planilha in listarPlanilhas(caminhoPlanilhaEntrada):
            if 1==1: #arquivo==pastaEntradas+nomeArquivo:
                if 1==1: #planilha==nomeArquivo:
                    print(f"_____________Iniciando processamento do \"{caminhoPlanilhaEntrada}\", planilha \"{planilha}\"")
                    logSaida = LogSondagem(planilha,caminhoPlanilhaEntrada)
                    logSaida.criarElementos()
                    logSaida.finalizarLog(pastaSaidas)
    pass
