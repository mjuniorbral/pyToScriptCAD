import inspect
import os
from functions import *

quebra_linha = "\n"

class Layer ():
    def __init__(self,
                 nameLayer:str="0",
                 Color:str="white",
                 Linetype:str="Continuous",
                 Lineweight:str="Default") -> None:
        
        self.nameLayer = nameLayer.replace(" ","_")
        self.Color = Color
        self.Linetype = Linetype
        self.Lineweight = Lineweight
        pass
    
    def __repr__(self) -> str:
        return f"{self.__class__}: {self.nameLayer=},{self.Color=},{self.Linetype=},{self.Lineweight=}"
    
    def create_Layer (self)->str:
        return f"-LAYER\nNew\n{self.nameLayer}\nColor\n{self.Color}\n{self.nameLayer}\nLtype\n{self.Linetype}\n{self.nameLayer}\nLweight\n{self.Lineweight}\n"\
            f"{self.nameLayer}\n\n"
    def modify_Layer (self) -> str:
        return f"-LAYER\nColor\n{self.Color}\n{self.nameLayer}\nLtype\n{self.Linetype}\n{self.nameLayer}\nLweight\n{self.Lineweight}\n{self.nameLayer}\n\n"
    def set_Layer (self) -> str:
        return f"-LAYER\nSet\n{self.nameLayer}\n\n"
LAYER_0 = Layer()

class StyleText ():
    def __init__(self,
                 nameStyle:str = "Standard",
                 fontName:str = "txt",
                 textHeight:float = 0.00,
                 widthFactor:float = 1.00,
                 obliqAngle:float = 0.00,
                 textBackwards:bool = False,
                 textUpsidedown:bool = False,
                 vertical:bool = False) -> None:
        
        self.nameStyle = nameStyle.replace(" ","_")
        self.fontName = fontName
        self.textHeight = textHeight
        self.widthFactor = widthFactor
        self.obliqAngle = obliqAngle
        self.textBackwards = textBackwards
        self.textUpsidedown = textUpsidedown
        self.vertical = vertical
        pass
    
    def create_Style(self)->str:
        script = f"-STYLE\n{self.nameStyle}\n\"{self.fontName}\"\n{self.textHeight}\n{self.widthFactor}\n{self.obliqAngle}\n{'YES' if self.textBackwards else 'NO'}\n"\
            f"{'YES' if self.textUpsidedown else 'NO'}\n"
        
        """
        Fontes que precisam da escolha do vertical:
        - Simplex
        - [Adicionar novas e mudar a opção da condição abaixo]
        """
        
        if "simplex" in self.nameStyle.lower():
            script += f"{'YES' if self.vertical else 'NO'}\n"
        return script
            

    def modify_Style(self)->str:
        script = f"-STYLE\n{self.nameStyle}\n\"{self.fontName}\"\n{self.textHeight}\n{self.widthFactor}\n{self.obliqAngle}\n{'YES' if self.textBackwards else 'NO'}\n"\
            f"{'YES' if self.textUpsidedown else 'NO'}\n"
        return script

    def set_Style(self)->str:
        return f"STYLE\n{self.nameStyle}\n"
    
    pass
STYLE_TEXT_STANDARD = StyleText()

####################################### Object #######################################
class Object ():
    def __init__(self,layer:Layer=LAYER_0,ID="ID-inexistente") -> None:
        self.ID = ID
        self.Layer = layer
        self.comments = []
        pass
    def set(self) -> None:
        print(f"Função {self.__class__.__name__}.{inspect.currentframe().f_code.co_name} não definida na classe {self.__class__.__name__}.")
        pass
    def load_settings(self) -> None:
        print(f"Função {self.__class__.__name__}.{str(inspect.currentframe().f_code.co_name)} não definida na classe {self.__class__.__name__}.")
        pass
    def set_comments(self) -> str:
        if len(self.comments)==0:
            return ""
        return f";{str.join(quebra_linha+';',self.comments)}\n"
    def __repr__(self) -> str:        
        return self.ID
    __str__=__repr__
    pass

######################################## Line ########################################
class Line (Object):
    def __init__(self,
                 p0:tuple,
                 pi:tuple,
                 layer:Layer=LAYER_0,
                 Color="BYLAYER",
                 Linetype="BYLAYER",
                 Lineweight="BYLAYER") -> None:
        super().__init__(layer,f"Object.{self.__class__.__name__}.ID=[{p0},{pi}]")
        self.p0 = p0
        self.pi = pi
        self.Color = Color
        self.Linetype = Linetype
        self.Lineweight = Lineweight
        pass
    def load_settings(self) -> str:
        return f"{setColor(self.Color)}{setLineType(self.Linetype)}{setLineWeight(self.Lineweight)}{self.Layer.set_Layer()}"
    def set(self) -> str:
        return f"LINE {setCoord(self.p0)} {setCoord(self.pi)} \n"
    pass

####################################### Circle #######################################
class Circle (Object):
    def __init__(self,
                 p0:tuple,
                 r:float,
                 layer:Layer=LAYER_0,
                 Color="BYLAYER",
                 Linetype="BYLAYER",
                 Lineweight="BYLAYER") -> None:
        super().__init__(layer,f"Object.{self.__class__.__name__}.ID=[{p0},{r}]")
        self.p0 = p0
        self.r = r
        self.Color = Color
        self.Linetype = Linetype
        self.Lineweight = Lineweight
        pass
    def load_settings(self) -> str:
        return f"{setColor(self.Color)}{setLineType(self.Linetype)}{setLineWeight(self.Lineweight)}{self.Layer.set_Layer()}"
    def set(self) -> str:
        return f"CIRCLE {setCoord(self.p0)} {self.r}\n"
    pass

######################################## Text ########################################
class Text (Object):
    def __init__(self,
                 p0:tuple,
                 content:str,
                 style:StyleText=STYLE_TEXT_STANDARD,
                 layer:Layer=LAYER_0,
                 Color="BYLAYER",
                 justify:str="L",
                 height:float=1.00,
                 rotation:float=0.00,
                 applyHeight:bool=True) -> None:
        super().__init__(layer,f"Object.{self.__class__.__name__}.ID=[{p0},{content}]")

        # Tratamento de encoding (ScriptCAD)
        self.aplicarSinalEncoding = False
        nAcentosCedilhas = len(encontrar_acentos_e_cedilha(content))
        if nAcentosCedilhas>0:
            self.content = remover_acentos(content)
            self.comments.append(f"! ! ! ! AVISOS - {self.__class__.__name__}.{str(inspect.currentframe().f_code.co_name)}: Seu objeto {self.__class__.__name__} foi alterado devido a limitação de formatação e todos os acentos e cedilhas foram retirados (número de remoções totais: {nAcentosCedilhas}). Para informação, o texto original antes da alteração está entre chaves: \n;[{content}].")
            print(self.comments[-1])
            self.aplicarSinalEncoding = True
        else:
            self.content = content
        
        # Atribuição dos atributos
        self.p0 = p0
        self.style = style
        self.applyHeight = applyHeight
        if self.style.textHeight!=0.00 and self.applyHeight:
            self.comments.append(f"! ! ! ! AVISOS - {self.__class__.__name__}.{str(inspect.currentframe().f_code.co_name)}: O obeto {self.__class__.__name__} escolhido não permite personalizar o tamanho dos objetos Text individualmente.Aconselha-se revisar a definição da altura do objeto Style {self.style.nameStyle}.")
            print(self.comments[-1])
        self.Color = Color
        self.justify = justify
        self.height = height
        self.rotation = rotation
        pass

    def load_settings(self) -> str:
        return f"{setColor(self.Color)}{self.Layer.set_Layer()}"
    def set(self) -> str:
        preScript = ""
        if self.style.textHeight!=0.00 and self.applyHeight:
            return preScript+f"TEXT\n{self.style.set_Style()}JUSTIFY\n{self.justify}\n{setCoord(self.p0)}\n{self.rotation}\n{self.content}\n"
        return preScript+f"TEXT\n{self.style.set_Style()}JUSTIFY\n{self.justify}\n{setCoord(self.p0)}\n{self.height}\n{self.rotation}\n{self.content}\n"
    pass

######################################## MText #######################################
class MText (Object):
    def __init__(self,
                 p0:tuple,
                 pi:tuple,
                 content:str,
                 style:StyleText=STYLE_TEXT_STANDARD,
                 layer:Layer=LAYER_0,
                 Color:str="BYLAYER",
                 justify:str="MC",
                 textHeight:float=0.00,
                 width:float=0.00,
                 rotation:float=0.00,
                 lineSpacing:float=0.00,
                 columns=None) -> None:
        super().__init__(layer,f"Object.{self.__class__.__name__}.ID=[{p0},{content.split(quebra_linha)[0]}]")

        content = content.replace("\n","\\P") # \P é a indicação que significa quebra de linha no SCRIPT CAD
        
        # Tratamento de encoding (ScriptCAD)
        self.aplicarSinalEncoding = False
        nAcentosCedilhas = len(encontrar_acentos_e_cedilha(content))
        if nAcentosCedilhas>0:
            self.content = remover_acentos(content)
            self.comments.append(f"! ! ! ! AVISOS - {self.__class__.__name__}.{str(inspect.currentframe().f_code.co_name)}: Seu objeto {self.__class__.__name__} foi alterado devido a limitação de formatação e todos os acentos e cedilhas foram retirados (número de remoções totais: {nAcentosCedilhas}). Para informação, o texto original antes da alteração está entre chaves (em que \P significa uma quebra de linha): \n;[{content}]")
            print(self.comments[-1])
            self.aplicarSinalEncoding = True
        else:
            self.content = content
        self.p0 = p0
        self.pi = pi
        self.style = style
        self.layer = layer
        self.Color = Color
        self.justify = justify
        self.textHeight = textHeight
        self.width = width
        self.rotation = rotation
        self.lineSpacing = lineSpacing
        self.columns = columns
        pass

    def load_settings(self) -> str:
        return f"{setColor(self.Color)}{self.Layer.set_Layer()}"
    def set(self) -> str:
        finalScript = f"MTEXT\n{setCoord(self.p0)}\n{self.style.set_Style()}"

        if self.textHeight!=0.00:
            finalScript += f"H\n{self.textHeight}\n"
        if self.width!=0.00:
            finalScript += f"W\n{self.width}\n"
        if self.rotation!=0.00:
            finalScript += f"R\n{self.rotation}\n"
        if self.lineSpacing!=0.00:
            finalScript += f"L\nE\n{self.lineSpacing}\n"

        finalScript += f"JUSTIFY\n{self.justify}\n{setCoord(self.pi)}\n{self.content}\n\n"
        return finalScript
    pass

####################################### Polyline #####################################
class Polyline (Object):
    def __init__(self,
                 pSequencial:tuple[tuple],
                 layer:Layer=LAYER_0,
                 closed:bool=False,
                 Color="BYLAYER",
                 Linetype="BYLAYER",
                 Lineweight="BYLAYER") -> None:
        super().__init__(layer,f"Object.{self.__class__.__name__}.ID=[{pSequencial[0:5]}]")
        self.closed = closed
        self.pSequencial = pSequencial
        self.Color = Color
        self.Linetype = Linetype
        self.Lineweight = Lineweight
        pass


    def load_settings(self) -> str:
        return f"{setColor(self.Color)}{setLineType(self.Linetype)}{setLineWeight(self.Lineweight)}{self.Layer.set_Layer()}"
    def set(self) -> str:
        if self.closed:
            return f"PLINE\n{quebra_linha.join([setCoord(self.pSequencial[i]) for i in range(len(self.pSequencial))])}\n{'CLOSE' if self.closed else ''}\n"
        return f"PLINE\n{quebra_linha.join([setCoord(self.pSequencial[i]) for i in range(len(self.pSequencial))])}\n\n"
    pass

###################################### Rectangule ####################################
class Rectangule (Object):
    def __init__(self,
                 p0:tuple,
                 pi:tuple,
                 layer:Layer=LAYER_0,
                 Color="BYLAYER",
                 Linetype="BYLAYER",
                 Lineweight="BYLAYER") -> None:
        super().__init__(layer,f"Object.{self.__class__.__name__}.ID=[{p0},{pi}]")
        
        # Depois implementar as opções que o comando RECTANGLE tem no autoCAD.
             
        self.p0 = p0
        self.pi = pi
        self.Color = Color
        self.Linetype = Linetype
        self.Lineweight = Lineweight
        pass

    def load_settings(self) -> str:
        return f"{setColor(self.Color)}{setLineType(self.Linetype)}{setLineWeight(self.Lineweight)}{self.Layer.set_Layer()}"
    def set(self) -> str:
        return f"RECTANGLE\n{setCoord(self.p0)}\n{setCoord(self.pi)}\n"
    pass

######################################## HATCH #######################################
class Hatch (Object):
    def __init__(self,
                 p0:tuple,
                 layer:Layer=LAYER_0,
                 pattern:str="SOLID",
                 Color="BYLAYER",
                 scale:float=0.01,
                 angle:float=0.0,
                 Linetype="BYLAYER",
                 Lineweight="BYLAYER") -> None:
        super().__init__(layer,f"Object.{self.__class__.__name__}.ID=[{p0},{pattern},{Color}]")
        self.p0 = p0
        self.pattern = pattern
        self.Color = Color
        self.scale = scale
        self.angle = angle
        self.Linetype = Linetype
        self.Lineweight = Lineweight
        pass
    def load_settings(self) -> str:
        script = "AI_SELALL\nZOOM\nOBJECT\n"
        script += f"{setColor(self.Color)}{setLineType(self.Linetype)}{setLineWeight(self.Lineweight)}{self.Layer.set_Layer()}"
        if self.pattern.upper() == "SOLID":
            script += f"-HATCH\nP\nSOLID\nLA\n{self.Layer.nameLayer}\n\n"
        elif self.pattern.upper() == "USER":
            self.comments.append(f"! ! ! ! AVISOS - {self.__class__.__name__}.{str(inspect.currentframe().f_code.co_name)}: Objeto {self.__class__.__name__} não possui implementação Pattern=USER. Por hora, será colocado SOLID como padrão.")
            print(self.comments[-1])
            script += f"-HATCH\nP\nSOLID\nLA\n{self.Layer.nameLayer}\n\n"
        elif self.pattern.upper() == "GRADIENT":
            self.comments.append(f"! ! ! ! AVISOS - {self.__class__.__name__}.{str(inspect.currentframe().f_code.co_name)}: Objeto {self.__class__.__name__} não possui implementação Pattern=GRADIENT. Por hora, será colocado SOLID como padrão.")
            print(self.comments[-1])
            script += f"-HATCH\nP\nSOLID\nLA\n{self.Layer.nameLayer}\n\n"
        else:
            script += f"-HATCH\nP\n{self.pattern}\n{self.scale}\n{self.angle}\nLA\n{self.Layer.nameLayer}\n\n"
        return script
    def set(self) -> str:
        return f"-HATCH\n{setCoord(self.p0)}\n\n"
    pass

################################### NÃO IMPLEMENTADO #################################
class Dimension (Object):
    # Copiar de algum outro Object e mudar variáveis e comandos
    pass

######################################## Script ######################################
class Script ():
    def __init__(self,
                 nome_arquivo:str,
                 osnap:bool = False,
                 grid:bool = False,
                 orto:bool = False,
                 lwdisplay:bool = False,
                 ltscale:float = 1.00,
                 ) -> None:
        self.nome_arquivo: str = nome_arquivo
        self.comandos: str = ""
        self.Layers = [LAYER_0]
        self.Styles = [STYLE_TEXT_STANDARD]
        self.elementos:list[Object] = []
        self.osnap:bool = osnap
        self.grid:bool = grid
        self.orto:bool = orto
        self.lwdisplay:bool = lwdisplay
        self.ltscale = ltscale
        codePath = os.path.abspath(inspect.getfile(inspect.currentframe())).replace('\\','/')
        self.filePath:str = codePath.replace(str.split(codePath,"/")[-1],"")
        pass

    def add_Layer(self,layer:Layer=LAYER_0) -> None:
        for i in self.Layers:
            if i is layer:
                print(str(inspect.currentframe().f_code.co_name)+": "+"Já existe esse Layer no objeto Script.")
                return
            else:
                if i.nameLayer == layer.nameLayer:
                    raise ValueError(str(inspect.currentframe().f_code.co_name)+": "+"Objetos Layer diferentes com o mesmo parâmetro Layer.nameLayer.")
        self.Layers.append(layer)

    def add_Style(self,style:StyleText=STYLE_TEXT_STANDARD) -> None:
        if not isinstance(style,StyleText):
            raise Exception("O ")
        for i in self.Styles:
            if i is style:
                print(str(inspect.currentframe().f_code.co_name)+": "+"Já existe esse Style no objeto Script.")
                return
            else:
                if i.nameStyle == style:
                    raise ValueError(str(inspect.currentframe().f_code.co_name)+": "+"Objetos Style diferentes com o mesmo parâmetro Style.nameStyle.")
        self.Styles.append(style)

    def addElements (self,newElement) -> None:
        self.elementos.append(newElement)
        pass

    def script(self,comando:str):
        self.comandos += comando
        pass
    
    def refresh (self) -> None:
        for i in self.elementos:
            if "text" in i.ID.lower():
                if i.style in self.Styles:
                    pass
                else:
                    self.add_Style(i.style)
                    
            if i.Layer in self.Layers:
                continue
            else:
                self.add_Layer(i.Layer)
        pass
    
    def compileScript(self,NOVO:bool=True,SALVAR:bool=False,BLOCKALL:bool=False,CLOSE:bool=False,pastaDWG:str="") -> None:

        """      
        Implementar uma função final que compile uma string com as definições abaixo e atribua ao parâmetro Script.comandos.
        - Configurar os objetos Layer do objeto Script usando os métodos Layer.create_Layer.
        - Configurar o modo de SNAP (implementar depois os outros modos como ORTO, GRID, OSNAP, etc)
        - Construir o código com os métodos de criação Object.load_settings e Object.set (set Layer antes para colocar o objeto no Layer certo)
        """

        # Config gerais
        if NOVO:
            self.script("NEW\n\n")
        
        self.script(f"-OSNAP {'ON' if self.osnap else 'OFF'}\n")
        self.script(f"ORTHOMODE {'0' if self.orto else '1'}\n")
        self.script(f"GRIDMODE {'0' if self.grid else '1'}\n")
        self.script(f"LWDISPLAY {'OFF' if self.lwdisplay else 'ON'}\n")
        self.script(f"LTSCALE {self.ltscale}\n")
        
        # Criando os Layers
        for layer in self.Layers:
            if layer is LAYER_0:
                continue
            else:
                self.script(layer.create_Layer())
        
        # Criando os Styles
        for style in self.Styles:
            if style is STYLE_TEXT_STANDARD:
                continue
            else:
                self.script(style.create_Style())
        
        # Criandos os objetos (set Layer do Objeto -> Load Setting do Objeto -> set Objetos)
        for elemento in self.elementos:
            #self.script(elemento.Layer.set_Layer()) # Retirado porque o próprio Object.load_setting ativa o Layer
            self.script(elemento.set_comments())
            self.script(elemento.load_settings())
            self.script(elemento.set())
        
        if BLOCKALL:
            pontoBaseBlock = "0,0"
            self.script(f"BLOCK\n{remover_acentos(self.nome_arquivo.replace(' ',''))}\n{pontoBaseBlock}\nALL\n\nINSERT\n{remover_acentos(self.nome_arquivo.replace(' ',''))}\n{pontoBaseBlock}\n\n\n\n")
        
        self.script("AI_SELALL\nZOOM\nOBJECT\n") # Zoom em foco dos objetos.
        
        if SALVAR:
            # self.script(f"FILEDIA 0\n")
            if pastaDWG=="": # Salvará na pasta out na raiz do classes
                caminho = f"{self.filePath}out/log_{self.nome_arquivo}.dwg"
            else:
                caminho = f"{self.filePath}log_{self.nome_arquivo}.dwg"
            self.script(f"SAVEAS\nLT2018\n\"{caminho}\"\n")
            
            # self.script("Y\n")
            
            if os.path.exists(caminho):
                self.script("Y\n")
            # self.script(f"FILEDIA 1\n")

        if CLOSE:
            self.script(f"CLOSE\n")

    def save (self,caminho:str="") -> None:
        self.pathSCR = f"{caminho}{self.nome_arquivo}.scr"
        # self.pathDWG = f"{caminho}{self.nome_arquivo}.dwg"
        with open(self.pathSCR, "w", encoding="utf-8") as arquivo:
            arquivo.write(self.comandos)
            print(f"Arquivo {self.pathSCR} salvo")
