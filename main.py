# -*- coding: utf-8 -*-

import time


from models import *
import os


if __name__=="__main__":
    # Mode 0: LogSondagem
    # Mode 1: Locação de Pontos
    mode = -1

    if not (mode in [0,1]):
        mode = int(input("Digite:\n0: para Log de Sondagem\n1: Locação de Pontos\n2: para Log de CPTu"))

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
                modelSaida = Locacao(planilha,caminhoPlanilhaEntrada)
            elif mode==2: # Log de CPTu
                modelSaida = LogCPTu(planilha,caminhoPlanilhaEntrada)
            modelSaida.criarElementos()
            modelSaida.finalizar(pastaSaidas,CLOSE=True)
        

    pass
end_time = time.time()

print(f"Programa finalizado em {end_time-start_time:.5f} segs.\n")