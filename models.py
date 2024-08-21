from classes import *
import pandas as pd
import numpy as np
from functions import toGrandeza

class Model():
    def __init__(self,nome:str,caminhoRelativo:str,ltscale:float) -> None:
        self.nome = nome
        self.caminhoRelativo = caminhoRelativo
        self.script = Script(nome,ltscale=ltscale)
        self.entrada = pd.read_excel(self.caminhoRelativo,self.nome)
        pass

    def finalizarLog(self,caminho="",SALVAR=True,BLOCKALL=True,CLOSE=False,NOVO=True) -> None:
        self.script.refresh()
        self.script.compileScript(SALVAR=SALVAR,BLOCKALL=BLOCKALL,CLOSE=CLOSE,NOVO=NOVO)
        self.script.save(caminho)
        print(f"_____________Finalizando log {self.nome}\n")

class LogSondagem(Model):
    
    def __init__(self,nomeSondagem:str,caminhoRelativo:str) -> None:

        ltscale=0.01

        super().__init__(nomeSondagem,caminhoRelativo,ltscale)
        self.nomeSondagem = self.nome
        
        self.LINHA_FINA = Layer("LOGSOND-LINHA_FINA","red")
        self.TXT = Layer("LOGSOND-TXT","8")
        self.LOGS = Layer("LOGSOND-LOGS","yellow")
        self.NIVEL_DAGUA = Layer("LOGSOND-NIVEL_AGUA","green")
        self.NSPT = Layer("LOGSOND-NSPT","green")
        
        self.SIMPLEX_W50 = StyleText("LOGSOND-SIMPLEX-W50","Simplex",widthFactor=0.5)
        self.SIMPLEX_W60 = StyleText("LOGSOND-SIMPLEX-W60","Simplex",widthFactor=0.6)
        self.SIMPLEX_W80 = StyleText("LOGSOND-SIMPLEX-W80","Simplex",widthFactor=0.8)
        
        self.SIMPLEX = StyleText("LOGSOND-SIMPLEX","Simplex",widthFactor=1.0)

        dadosSondagens = self.entrada[self.entrada.columns[0:2]]
        config = self.entrada[self.entrada.columns[3:5]]
        camadas = self.entrada[self.entrada.columns[6:10]]
        manobrasSolo = self.entrada[self.entrada.columns[11:14]]
        manobrasRocha = self.entrada[self.entrada.columns[15:23]]
        criteriosParada = self.entrada[self.entrada.columns[24:26]]
       
        self.dadosSondagens = dadosSondagens[dadosSondagens.notna().any(axis=1)]
        self.config = config[config.notna().any(axis=1)]
        self.camadas = camadas[camadas.notna().any(axis=1)]
        self.manobrasSolo = manobrasSolo[manobrasSolo.notna().any(axis=1)]
        self.manobrasRocha = manobrasRocha[manobrasRocha.notna().any(axis=1)]
        self.criteriosParada = criteriosParada[criteriosParada.notna().any(axis=1)]

    def criarElementos(self)->None:
        
        # Isolamento dos dados ========================================================================================
        dadosSond = self.dadosSondagens.set_index("Dados Sondagem")
        elementos = []
        profund = dadosSond.at["Prof. total (m)","Unnamed: 1"]
        nomeSondagem = dadosSond.at["Nome da Sondagem","Unnamed: 1"]
        cotaSondagem = dadosSond.at["Cota de Boca (m)","Unnamed: 1"]
        profNA = dadosSond.at["Profundidade do NA. (m)","Unnamed: 1"]
        distProj = dadosSond.at["Distância de Projeção (m)","Unnamed: 1"]

        print("Extraindo parâmetros da planilha.")

        try:
            dadosConfig = self.config.set_index("Configurações")
            dimensoesQuadroAltura = dadosConfig.at["dimensoesQuadroAltura","Unnamed: 4"]
            dimensoesQuadroLargura = dadosConfig.at["dimensoesQuadroLargura","Unnamed: 4"]
            espessuraBarra = dadosConfig.at["espessuraBarra","Unnamed: 4"]
            hTriang = dadosConfig.at["hTriang","Unnamed: 4"]
            afastamentoTextoQuadro = dadosConfig.at["afastamentoTextoQuadro","Unnamed: 4"]
            tamanhoFonte = dadosConfig.at["tamanhoFonte","Unnamed: 4"]
            espacamentoFinalSond = dadosConfig.at["espacamentoFinalSond","Unnamed: 4"]
            alturaLegendaRocha = dadosConfig.at["alturaLegendaRocha","Unnamed: 4"]
            razaoFonteLegendaRocha = dadosConfig.at["razaoFonteLegendaRocha","Unnamed: 4"]
            razaoFonteLegendaQuadro = dadosConfig.at["razaoFonteLegendaQuadro","Unnamed: 4"]
            razaoFonteNSPT = dadosConfig.at["razaoFonteNSPT","Unnamed: 4"]
            razaoFonteTxtRocha = dadosConfig.at["razaoFonteTxtRocha","Unnamed: 4"]
            dxLITO = dadosConfig.at["dxLITO","Unnamed: 4"]
            dxALTeFRAT = dadosConfig.at["dxALTeFRAT","Unnamed: 4"]
            dxRQDeREC = dadosConfig.at["dxRQDeREC","Unnamed: 4"]
            afastamentoNA = dadosConfig.at["afastamentoNA","Unnamed: 4"]
            dxNA = dadosConfig.at["dxNA","Unnamed: 4"]
            dimensoesQuadro:tuple[float] = ( dimensoesQuadroLargura, dimensoesQuadroAltura )
            print("Parâmetros extraídos da planilha com sucesso.")
        except Exception as m:
            print(f"\n! ! ! ! AVISOS - {str(inspect.currentframe().f_code.co_name)}: Os parâmetros NÃO foram extraídos da forma correta. Erro: [ {m} ]. Os parâmetros padrões serão usados.\n")
            # Parâmetros padrões
            dimensoesQuadroAltura = 3.50
            dimensoesQuadroLargura = 8.00
            espessuraBarra = 0.20
            hTriang = 0.70
            afastamentoTextoQuadro = 0.30
            tamanhoFonte = 0.40
            espacamentoFinalSond = 0.20
            alturaLegendaRocha = 0.60
            razaoFonteLegendaRocha = 0.60
            razaoFonteLegendaQuadro = 0.90
            razaoFonteNSPT = 0.80
            razaoFonteTxtRocha = 0.80
            dxLITO = 3.00
            dxALTeFRAT = 1.00
            dxRQDeREC = 1.00
            afastamentoNA = 0.50
            dxNA = 3.00
            dimensoesQuadro:tuple[float] = ( dimensoesQuadroLargura, dimensoesQuadroAltura )
        
        # Verificando a equivalência entre o nome da planilha e da sondagem no campo da célula referente ==============
        if self.nomeSondagem!=nomeSondagem:
            self.nomeSondagem = nomeSondagem
            self.script.nome_arquivo= nomeSondagem
            print(f"! ! ! ! AVISOS - {str(inspect.currentframe().f_code.co_name)}: O nome da planilha é diferente do nome na célula referente a sondagem. Nome do modelo foi substituido para {nomeSondagem}")

        # Inserindo os elementos ======================================================================================
        
        # Quadro resumo ===============================================================================================
        elementos.append(Rectangule((-dimensoesQuadro[0]/2.,dimensoesQuadro[1]+hTriang),(dimensoesQuadro[0]/2.,hTriang),self.LOGS))
        elementos.append(Line((-dimensoesQuadro[0]/2.,dimensoesQuadro[1]*(1./3.)+hTriang),(dimensoesQuadro[0]/2.,dimensoesQuadro[1]*(1./3.)+hTriang),self.LOGS))
        elementos.append(Line((-dimensoesQuadro[0]/2.,dimensoesQuadro[1]*(2./3.)+hTriang),(dimensoesQuadro[0]/2.,dimensoesQuadro[1]*(2./3.)+hTriang),self.LOGS))
        elementos.append(Line((0,dimensoesQuadro[1]+hTriang),(0,hTriang),self.LOGS))
        elementos.append(Polyline(((0,0),(-espessuraBarra,hTriang),(espessuraBarra,hTriang)),self.LOGS,True))
        
        # Texto do quadro resumo ======================================================================================
        elementos.append(Text((-afastamentoTextoQuadro,dimensoesQuadro[1]*(5./6.)+hTriang),"Sondagem",self.SIMPLEX,self.TXT,justify="MR",height=tamanhoFonte*razaoFonteLegendaQuadro))
        elementos.append(Text((-afastamentoTextoQuadro,dimensoesQuadro[1]*(3./6.)+hTriang),"Cota",self.SIMPLEX,self.TXT,justify="MR",height=tamanhoFonte*razaoFonteLegendaQuadro))
        elementos.append(Text((-afastamentoTextoQuadro,dimensoesQuadro[1]*(1./6.)+hTriang),"Dist. Proj.",self.SIMPLEX,self.TXT,justify="MR",height=tamanhoFonte*razaoFonteLegendaQuadro))
        
        elementos.append(Text((+afastamentoTextoQuadro,dimensoesQuadro[1]*(5./6.)+hTriang),self.nomeSondagem,self.SIMPLEX,self.TXT,justify="ML",height=tamanhoFonte))
        elementos.append(Text((+afastamentoTextoQuadro,dimensoesQuadro[1]*(3./6.)+hTriang),toGrandeza(cotaSondagem,"m"),self.SIMPLEX,self.TXT,justify="ML",height=tamanhoFonte))
        elementos.append(Text((+afastamentoTextoQuadro,dimensoesQuadro[1]*(1./6.)+hTriang),toGrandeza(distProj,"m"),self.SIMPLEX,self.TXT,justify="ML",height=tamanhoFonte))
        
        # Barra (ou palito) hachurada da linha de sondagem ============================================================
        elementos.append(Rectangule((-espessuraBarra/2.,0),(espessuraBarra/2.,-profund),self.LOGS))
        y = -1
        while y>-profund:
            elementos.append(Line((-espessuraBarra/2.,y),(espessuraBarra/2.,y),self.LOGS))
            y-=1
        y = 0
        while y>-profund:
            if y%2==0:
                elementos.append(Hatch((0,y-0.05),self.LOGS))
            y-=1

        # Inserindo legenda das rochas
        if len(self.manobrasRocha)==0:
            alturaLegendaRocha=0
        else:
            elementos.append(Text((-dxLITO/2.-2*dxALTeFRAT-espessuraBarra/2.,-profund-alturaLegendaRocha/2.),"LITO",self.SIMPLEX,self.TXT,height=razaoFonteLegendaRocha*tamanhoFonte,justify="MC"))
            elementos.append(Text((-1.5*dxALTeFRAT-espessuraBarra/2.,-profund-alturaLegendaRocha/2.),"ALT",self.SIMPLEX,self.TXT,height=razaoFonteLegendaRocha*tamanhoFonte,justify="MC"))
            elementos.append(Text((-0.5*dxALTeFRAT-espessuraBarra/2.,-profund-alturaLegendaRocha/2.),"FRAT",self.SIMPLEX,self.TXT,height=razaoFonteLegendaRocha*tamanhoFonte,justify="MC"))
            elementos.append(Text((+1.5*dxRQDeREC+espessuraBarra/2.,-profund-alturaLegendaRocha/2.),"RQD(%)",self.SIMPLEX_W60,self.TXT,height=razaoFonteLegendaRocha*tamanhoFonte,justify="MC"))
            elementos.append(Text((+0.5*dxRQDeREC+espessuraBarra/2.,-profund-alturaLegendaRocha/2.),"REC(%)",self.SIMPLEX_W60,self.TXT,height=razaoFonteLegendaRocha*tamanhoFonte,justify="MC"))
            
        # Inserindo o final da sondagem ================================================================================
        elementos.append(Text((-afastamentoTextoQuadro,-profund-alturaLegendaRocha-espacamentoFinalSond),f"Final da sondagem: {toGrandeza(profund,'m')}",self.SIMPLEX_W60,self.TXT,justify="TR",height=tamanhoFonte))
        
        # Adicionando a posição do Nível da Água =======================================================================
        if str(profNA).upper() == "SECO" or isinstance(profNA,str):
            elementos.append(Text((+afastamentoTextoQuadro,-profund-alturaLegendaRocha),f"NA: {profNA}",self.SIMPLEX,self.NIVEL_DAGUA,justify="TL",height=tamanhoFonte))
            pass
        else:
            elementos.append(Line((-espessuraBarra/2.,-profNA),(+espessuraBarra/2.+2*dxRQDeREC+dxNA+afastamentoNA,-profNA),self.NIVEL_DAGUA))

            elementos.append(Line((+espessuraBarra/2.+2*dxRQDeREC+dxNA*1/7+afastamentoNA,-profNA-dxNA*1/10),(+espessuraBarra/2.+2*dxRQDeREC+dxNA*6/7+afastamentoNA,-profNA-dxNA*1/10),self.NIVEL_DAGUA))
            elementos.append(Line((+espessuraBarra/2.+2*dxRQDeREC+dxNA*2/7+afastamentoNA,-profNA-dxNA*2/10),(+espessuraBarra/2.+2*dxRQDeREC+dxNA*5/7+afastamentoNA,-profNA-dxNA*2/10),self.NIVEL_DAGUA))
            elementos.append(Line((+espessuraBarra/2.+2*dxRQDeREC+dxNA*3/7+afastamentoNA,-profNA-dxNA*3/10),(+espessuraBarra/2.+2*dxRQDeREC+dxNA*4/7+afastamentoNA,-profNA-dxNA*3/10),self.NIVEL_DAGUA))
            
            elementos.append(Text((+espessuraBarra/2.+2*dxRQDeREC+dxNA/2.+afastamentoNA,-profNA),f"NA: {toGrandeza(profNA,'m')}",self.SIMPLEX_W80,self.NIVEL_DAGUA,height=tamanhoFonte,justify="BC"))
        
        # Adicionar nSPT
        for n,manobra in self.manobrasSolo.iterrows():
            inicio = manobra["Início.1"]
            fim = manobra["Fim.1"]
            if str(fim)=="nan":
                fim = inicio+1.
            if isinstance(manobra["nSPT"],(int,float)):
                nSPT = str(int(manobra["nSPT"]))
            elif isinstance(manobra["nSPT"],str):
                nSPT = manobra["nSPT"]

            if abs(inicio-fim)<=0.5:
                elementos.append(Text((-espessuraBarra,-inicio),nSPT,self.SIMPLEX,self.NSPT,height=tamanhoFonte*razaoFonteNSPT,justify="TR"))
            else:
                elementos.append(Text((-espessuraBarra,-inicio-(fim-inicio)/2.),nSPT,self.SIMPLEX,self.NSPT,height=tamanhoFonte*razaoFonteNSPT,justify="MR"))
        
        # Adicionando camadas de solo
        for n,camada in self.camadas.iterrows():
            inicio = camada["Início"]
            fim = camada["Fim"]
            classificacao = camada["Classificação"]
            elementos.append(Rectangule((-espessuraBarra/2.-2*dxALTeFRAT-dxLITO,-inicio),(-espessuraBarra/2.-2*dxALTeFRAT,-fim),self.LOGS))
            elementos.append(MText((-espessuraBarra/2.-2*dxALTeFRAT-dxLITO,-inicio),(-espessuraBarra/2.-2*dxALTeFRAT,-fim),str.upper(str(classificacao)),self.SIMPLEX,self.TXT,textHeight=acharHeightIdeal(classificacao,dxLITO,abs(inicio-fim))))
            
            elementos.append(Line((-espessuraBarra/2.-2*dxALTeFRAT,-inicio),(-espessuraBarra/2.,-inicio),self.LINHA_FINA,Linetype="DASHED",Lineweight="0.05"))
            
        elementos.append(Line((-espessuraBarra/2.-2*dxALTeFRAT,-fim),(-espessuraBarra/2.,-fim),self.LINHA_FINA,Linetype="DASHED",Lineweight="0.05"))
            
        # Adicionado manobras de rocha
        for n,manobra in self.manobrasRocha.iterrows():
            inicio = manobra["Início.2"]
            fim = manobra["Fim.2"]
            rec = manobra["% Rec."]
            rqd = manobra["RQD (%)"]
            alt = manobra["A"]
            frat = manobra["F"]
            
            if abs(inicio-fim)>tamanhoFonte*razaoFonteTxtRocha:
                razaoFonteTxtRocha = razaoFonteTxtRocha
            elif tamanhoFonte*razaoFonteTxtRocha<0.32:
                razaoFonteTxtRocha = 0.32/tamanhoFonte
                pass

            # Texto Alteração, Fraturamento, Recuperação e RQD
            elementos.append(Text((-0.5*espessuraBarra-1.5*dxALTeFRAT,-0.5*abs(inicio+fim)),alt,self.SIMPLEX_W50,self.TXT,justify="MC",height=tamanhoFonte*razaoFonteTxtRocha))
            elementos.append(Text((-0.5*espessuraBarra-0.5*dxALTeFRAT,-0.5*abs(inicio+fim)),frat,self.SIMPLEX_W50,self.TXT,justify="MC",height=tamanhoFonte*razaoFonteTxtRocha))
            elementos.append(Text((+0.5*espessuraBarra+0.5*dxRQDeREC,-0.5*abs(inicio+fim)),toGrandeza(rqd,"",0),self.SIMPLEX,self.TXT,justify="MC",height=tamanhoFonte*razaoFonteTxtRocha))
            elementos.append(Text((+0.5*espessuraBarra+1.5*dxRQDeREC,-0.5*abs(inicio+fim)),toGrandeza(rec,"",0),self.SIMPLEX,self.TXT,justify="MC",height=tamanhoFonte*razaoFonteTxtRocha))
            
            # Retângulo da Alteração
            elementos.append(Rectangule(
                (-0.5*espessuraBarra-2*dxALTeFRAT,-inicio),
                (-0.5*espessuraBarra-1*dxALTeFRAT,-fim),
                self.LOGS
                ))
            # Retângulo do Fraturamento
            elementos.append(Rectangule(
                (-0.5*espessuraBarra-1*dxALTeFRAT,-inicio),
                (-0.5*espessuraBarra-0*dxALTeFRAT,-fim),
                self.LOGS
                ))
            # Retângulo da Recuperação
            elementos.append(Rectangule(
                (+0.5*espessuraBarra+1*dxRQDeREC,-inicio),
                (+0.5*espessuraBarra+0*dxRQDeREC,-fim),
                self.LOGS
                ))
            # Retângulo do RQD
            elementos.append(Rectangule(
                (+0.5*espessuraBarra+2*dxRQDeREC,-inicio),
                (+0.5*espessuraBarra+1*dxRQDeREC,-fim),
                self.LOGS
                ))
        
        # Adicionando critérios de parada
        for n,criterio in self.criteriosParada.iterrows():
            textoCriterio = criterio["Critérios de Paralisação"]
            profCriterio = criterio["Prof. (m)"]
            elementos.append(Text((+espessuraBarra,-profCriterio),str.upper(str(textoCriterio)),self.SIMPLEX,self.TXT,height=razaoFonteNSPT*tamanhoFonte,justify="BL"))
            
        # Adicionando os elementos ao Script do Modelo =================================================================
        for elemento in elementos:
            self.script.addElements(elemento)
    pass