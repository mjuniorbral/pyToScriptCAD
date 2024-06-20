from classes import *
import pandas as pd

class LogSondagemPai():
    def __init__(self,nomeSondagem:str,caminhoRelativo:str,ltscale:float) -> None:
        self.nomeSondagem = nomeSondagem
        self.caminhoRelativo = caminhoRelativo
        self.script = Script(nomeSondagem,ltscale=ltscale)
        self.entrada = pd.read_excel(self.caminhoRelativo,self.nomeSondagem)
        pass

    def finalizarLog(self,caminho="") -> None:
        self.script.refresh()
        self.script.compileScript(True,True)
        self.script.save(caminho)
        print(f"_____________Finalizando log {self.nomeSondagem}\n")

class LogSondagem(LogSondagemPai):
    
    def __init__(self,nomeSondagem:str,caminhoRelativo:str) -> None:

        ltscale=0.01

        super().__init__(nomeSondagem,caminhoRelativo,ltscale)
        
        self.TXT_GEOCOBA = Layer("TXT_GEOCOBA","green")
        self.AVISOS = Layer("AVISOS","red")
        self.LOGS = Layer("LOGS","yellow")
        self.NIVEL_DAGUA = Layer("NIVEL AGUA","blue")
        
        self.SIMPLEX_GEOCOBA = StyleText("SIMPLEX-GEOCOBA","Simplex",widthFactor=0.8)

        dadosSondagens = self.entrada[self.entrada.columns[0:2]]
        config = self.entrada[self.entrada.columns[3:5]]
        camadas = self.entrada[self.entrada.columns[6:10]]
        manobrasSolo = self.entrada[self.entrada.columns[11:14]]
        manobrasRocha = self.entrada[self.entrada.columns[15:23]]
        
        self.dadosSondagens = dadosSondagens[dadosSondagens.notna().any(axis=1)]
        self.config = config[config.notna().any(axis=1)]
        self.camadas = camadas[camadas.notna().any(axis=1)]
        self.manobrasSolo = manobrasSolo[manobrasSolo.notna().any(axis=1)]
        self.manobrasRocha = manobrasRocha[manobrasRocha.notna().any(axis=1)]
    
    def criarElementosCamadas(self,dx:float=4.7)->None:
        elementos = []
        for n,camada in self.camadas.iterrows():
            inicio = camada["Início"]
            fim = camada["Fim"]
            descricao = camada["Descrição"]
            elementos.append(Line((0,-fim),(dx,-fim),Color="250",Linetype="DASHED2"))
            
            texto = MText((0,-inicio),(dx,-fim),str.upper(descricao),layer=self.TXT_GEOCOBA,textHeight=acharHeightIdeal(descricao,dx,abs(inicio-fim)))
            if texto.aplicarSinalEncoding:
                elementos.append(Circle((dx/2,-(inicio+fim)/2),(fim-inicio)/2,self.AVISOS))
            elementos.append(texto)
        for elemento in elementos:
            self.script.addElements(elemento)

    def criarElementosManobrasRochas(self,x0:float=5.24,dx:float=1.5)->None:
        elementos = []
        for n,manobra in self.manobrasRocha.iterrows():
            inicio = manobra["Início.2"]
            fim = manobra["Fim.2"]
            rec = manobra["% Rec."]
            rqd = manobra["RQD (%)"]
            elementos.append(
                Rectangule(
                    (x0,-inicio),
                    (x0+2*dx,-fim),
                    self.LOGS)
            )
            elementos.append(
                Line(
                    (x0+dx,-inicio),
                    (x0+dx,-fim),
                    self.LOGS
                )
            )
            xREC = dx*(rec/100)
            elementos.append(
                Line(
                    (x0+dx+xREC,-inicio),
                    (x0+dx+xREC,-fim),
                    self.LOGS
                )
            )
            
            ########## aplicação do hatch #######################################################################
            elementos.append(
                Hatch(
                    (x0+dx+0.5*xREC,-(inicio+fim)/2),
                    LAYER_0,
                    Color="red"
                )
            )
            
            elementos.append(
                Text(
                    (x0+dx/2.,-inicio-(fim-inicio)/2.),
                    str(int(rqd)),
                    layer=self.TXT_GEOCOBA,
                    height=0.4,
                    justify="MC"
                    )
            )
            elementos.append(                 
                Text(
                    (x0+dx+dx/2.,-inicio-(fim-inicio)/2.),
                    str(int(rec)),
                    layer=self.TXT_GEOCOBA,
                    height=0.4,
                    justify="MC"
                )
            )
        for elemento in elementos:
            self.script.addElements(elemento)

    def criarElementosManobrasSolos(self,x0:float=5.24,dx:float=1.5)->None:
        elementos = []
        for n,manobra in self.manobrasSolo.iterrows():
            inicio = manobra["Início.1"]
            fim = manobra["Fim.1"]
            if str(fim)=="nan":
                fim = inicio+1.
            if isinstance(manobra["nSPT"],(int,float)):
                nSPT = str(int(manobra["nSPT"]))
            elif isinstance(manobra["nSPT"],str):
                nSPT = manobra["nSPT"]
            elementos.append(
                Rectangule(
                    (x0,-inicio),
                    (x0+dx,-fim),
                    self.LOGS)
            )
            elementos.append(
                Text(
                    (x0+dx/2.,-inicio-(fim-inicio)/2.),
                    nSPT,
                    self.SIMPLEX_GEOCOBA,                
                    self.TXT_GEOCOBA,
                    height=0.675,
                    justify="MC"
                    )
            )
        for elemento in elementos:
            self.script.addElements(elemento)

    def criarElementosGerais(self,dx:float=4.7,dx2:float=0.54,dx3:float=1.5)->None:
        dadosSond = self.dadosSondagens.set_index("Dados Sondagem")
        elementos = []
        profund = dadosSond.at["Prof. total (m)","Unnamed: 1"]
        nomeSondagem = dadosSond.at["Nome da Sondagem","Unnamed: 1"]
        
        # Verificando a equivalência entre o nome da planilha e da sondagem no campo da célula referente
        if self.nomeSondagem!=nomeSondagem:
            self.nomeSondagem = nomeSondagem
            self.script.nome_arquivo= nomeSondagem
            print(f"! ! ! ! AVISOS - {str(inspect.currentframe().f_code.co_name)}: O nome da planilha é diferente do nome na célula referente a sondagem. Nome do modelo foi substituido para {nomeSondagem}")

        cotaSondagem = dadosSond.at["Cota de Boca (m)","Unnamed: 1"]
        cotaNA = dadosSond.at["Profundidade do NA. (m)","Unnamed: 1"]
        elementos.append(Rectangule((0,0),(dx,-profund),self.LOGS))
        elementos.append(Rectangule((dx,0),(dx+dx2,-profund),self.LOGS))
        y = 0.0
        while y<=profund:
            if y%1==0:
                elementos.append(Line((-0.32,-y),(0,-y),self.LOGS))
            else:
                elementos.append(Line((-0.16,-y),(0,-y),self.LOGS))
            
            if y%5==0:
                elementos.append(Text((-0.62,-y),str(int(y)),self.SIMPLEX_GEOCOBA,self.TXT_GEOCOBA,justify="MR",height=0.675))
                
            y+=0.5
            
        H = 5. # Altura do quadro de informações da sondagem
        B = 11.5 # Base do quadro de informações da sondagem
        h1 = 5. # Altura da seta
        h2 = 3. # Altura do subquadro de cota e profundidade
        h3 = 2. # Altura do subquadro do nome da sondagem
        lSeta = 0.7 # Altura da seta
        elementos.append(Rectangule((-B/2.,H+h1),(B/2.,h1),self.LOGS))
        elementos.append(Line((-B/2.,h1+h2),(B/2.,h1+h2),self.LOGS))
        elementos.append(Line((0,h1+h2),(0,h1),self.LOGS))
        elementos.append(Line((0,0),(0,h1),self.LOGS))
        elementos.append(
            Polyline(

                ((0,0),(lSeta,lSeta),(-lSeta,lSeta)),
                self.LOGS,
                True
                ))
        elementos.extend(
            [
                Text((-2.1,0.3),"NA",self.SIMPLEX_GEOCOBA,self.TXT_GEOCOBA,justify="ML",height=0.675,rotation=90),
                Text((dx/2.,0.3),"MATERIAL",self.SIMPLEX_GEOCOBA,self.TXT_GEOCOBA,justify="ML",height=0.675,rotation=90),
                MText((dx+dx2-0.1,0.3),(dx+dx2-0.5+1,0.3+1),"NSPT\nRQD(%)",self.SIMPLEX_GEOCOBA,self.TXT_GEOCOBA,justify="TL",textHeight=0.675,rotation=90,lineSpacing=.8),
                Text((dx+dx2+dx3+0.5,0.3),"REC(%)",self.SIMPLEX_GEOCOBA,self.TXT_GEOCOBA,justify="TL",height=0.675,rotation=90),
                Text((0,h1+h2+h3/2),f"{nomeSondagem}",layer=self.TXT_GEOCOBA,justify="MC",height=0.675),
                MText((-B/2,h1),(0,h1+h2),f"Cota\n{dotToComma(cotaSondagem)}m",layer=self.TXT_GEOCOBA,justify="MC",textHeight=0.675),
                MText((+B/2,h1),(0,h1+h2),f"Profundid.\n{dotToComma(profund)}m",layer=self.TXT_GEOCOBA,justify="MC",textHeight=0.675)
            ]
        )
        dxNA = 3.7
        x0NA = -4.6
        if isinstance(cotaNA,str):
            elementos.extend(
                [
                    Line((x0NA+0.0*dx,-profund-1),(x0NA+dxNA-0.0*dxNA,-profund-1),self.NIVEL_DAGUA),
                    Text((x0NA+0.5*dx,-profund-1+0.25),f"{cotaNA}",self.SIMPLEX_GEOCOBA,self.TXT_GEOCOBA,justify="BC",height=0.675)
                ]
            )
        else:
            elementos.extend(
                [
                    Line((x0NA+0.00*dx,-cotaNA-0*0.25),(x0NA+dxNA-0.00*dxNA,-cotaNA-0*0.25),self.NIVEL_DAGUA),
                    Line((x0NA+0.10*dx,-cotaNA-1*0.25),(x0NA+dxNA-0.10*dxNA,-cotaNA-1*0.25),self.NIVEL_DAGUA),
                    Line((x0NA+0.20*dx,-cotaNA-2*0.25),(x0NA+dxNA-0.20*dxNA,-cotaNA-2*0.25),self.NIVEL_DAGUA),
                    Line((x0NA+0.30*dx,-cotaNA-3*0.25),(x0NA+dxNA-0.30*dxNA,-cotaNA-3*0.25),self.NIVEL_DAGUA),
                    Line((x0NA+0.40*dx,-cotaNA-4*0.25),(x0NA+dxNA-0.40*dxNA,-cotaNA-4*0.25),self.NIVEL_DAGUA),
                    Text((x0NA+0.50*dx,-cotaNA+0.15),f"{cotaNA}m",self.SIMPLEX_GEOCOBA,self.TXT_GEOCOBA,justify="BC",height=0.675)
                ]
            )
        for elemento in elementos:
            self.script.addElements(elemento)

    def criarElementos(self):
        self.criarElementosGerais()
        self.criarElementosCamadas()
        self.criarElementosManobrasSolos()
        self.criarElementosManobrasRochas()
        pass

    pass
