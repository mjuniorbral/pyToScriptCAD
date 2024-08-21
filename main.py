# -*- coding: utf-8 -*-

import time

start_time = time.time()
print("\n"*5)
print("===== Programa iniciado...")
print("\n"*20)

from models import *
import os

if __name__=="__main__":
    
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
            logSaida = LogSondagem(planilha,caminhoPlanilhaEntrada)
            logSaida.criarElementos()
            logSaida.finalizarLog(pastaSaidas,CLOSE=True)
    pass
end_time = time.time()

print(f"Programa finalizado em {end_time-start_time:.5f} segs.\n")