# -*- coding: utf-8 -*-

import time

from pyToCAD import model_to_doc_dxf
from models import *
import os

_NOVO = True
_BLOCKALL = True
_CLOSE = False

if __name__=="__main__":
    # Mode -1: Perguntar modo
    # Mode 0: LogSondagem
    # Mode 1: Locação de Pontos
    # Mode 2: Projeção de Verticais
    mode = 0

    if not (mode in [0,1,2]):
        mode = int(input("Digite:\n0: para Log de Sondagem\n1: Locação de Pontos\n2: Projeção de Verticais (em desenvolvimento)\n"))

    start_time = time.time()
    print("\n"*5)
    print("===== Programa iniciado...")
    print("\n"*20)
    
    pastaEntradas = 'in\\'
    pastaSaidas = 'out\\'

    if not os.path.exists(pastaEntradas):
        os.mkdir(pastaEntradas)
        print("Criou-se a pasta 'in'")
    if not os.path.exists(pastaSaidas):
        os.mkdir(pastaSaidas)
        print("Criou-se a pasta 'out'")

    for caminhoPlanilhaEntrada in get_all_files_in_directory(pastaEntradas):
        for planilha in listarPlanilhas(caminhoPlanilhaEntrada):
            print(f"_____________Iniciando processamento do \"{caminhoPlanilhaEntrada}\", planilha \"{planilha}\"")
            if mode==0: # LogSondagem
                modelSaida = LogSondagem(planilha,caminhoPlanilhaEntrada)
            elif mode==1: # Locação de Pontos
                # _NOVO = False
                # _BLOCKALL = False
                modelSaida = Locacao(planilha,caminhoPlanilhaEntrada)
            elif mode==2:
                modelSaida = ProjSecao(planilha,caminhoPlanilhaEntrada)
            modelSaida.criarElementos()
            modelSaida.finalizar(pastaSaidas,CLOSE=_CLOSE,NOVO=_NOVO,BLOCKALL=_BLOCKALL)
            model_to_doc_dxf(modelSaida)

    pass
end_time = time.time()

print(f"Programa finalizado em {end_time-start_time:.5f} segs.\n")