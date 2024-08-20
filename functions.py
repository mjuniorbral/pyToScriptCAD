import unicodedata
import inspect
import pandas as pd
import numpy as np
import os

def toGrandeza (valor,unidade,casasDecimais=2,separadorDecimal=",",separadorMilhar="")->str:
    if valor=="-" or str(valor)=="nan":
        return valor
    inteiro = int(valor)
    decimal = round(valor-inteiro,casasDecimais)
    if len(unidade)>0:
        unidade = " "+unidade
    cont = 0
    strInteiro = ""
    for c in str(inteiro)[::-1]:
        cont+=1
        strInteiro+=c
        if cont%3==0:
            strInteiro+=separadorMilhar
    strInteiro = strInteiro[::-1]
    if strInteiro[0]==separadorMilhar:
        strInteiro = strInteiro[1:]
    strDecimal = f"{decimal:.{casasDecimais}f}"[2:]
    if casasDecimais==0:
        separadorDecimal = ""
    return f"{strInteiro}{separadorDecimal}{strDecimal}{unidade}"

def celToStr(celula):
    if celula==np.nan:
        return "-"
    return str(celula)

def encontrar_acentos_e_cedilha(texto):
    acentos_e_cedilha = []
    if not isinstance(texto,str):
        print(f"! ! ! ! AVISOS - {str(inspect.currentframe().f_code.co_name)}: O texto '{texto}' não é um str. Ele será convertido.")
        texto = str(texto)
    for caractere in texto:
        # Normaliza o caractere em forma NFD (Nomalization Form Decomposition)
        # para separar o caractere base dos diacríticos
        nome_unicode = unicodedata.name(caractere)
        if 'WITH' in nome_unicode or 'CEDILLA' in nome_unicode:

            acentos_e_cedilha.append(caractere)

    return acentos_e_cedilha

def remover_acentos(texto):
    # Normaliza o texto para a forma NFD (decomposição)
    texto_normalizado = unicodedata.normalize('NFD', texto)
    # Constrói a string sem os caracteres combinantes (diacríticos)
    texto_sem_acentos = ''.join(
        char for char in texto_normalizado
        if unicodedata.category(char) != 'Mn'
    )
    # Substitui 'ç' por 'c'
    texto_sem_acentos = texto_sem_acentos.replace('ç', 'c').replace('Ç', 'C')

    return texto_sem_acentos

def setColor(color:str)->str:
    return f"-COLOR\n{color}\n"

def setLineType(Linetype:str)->str:
    return f"-LINETYPE\nLoad\n{Linetype}\n{Linetype}\nSet\n{Linetype}\n\n"

def setLineWeight(LineWeight:str)->str:
    return f"LWEIGHT\n{LineWeight}\n"

def setCoord(coord:tuple=(0,0),_3d:bool=False)->str:
    if _3d:
        if len(coord)!=3:
            raise ValueError(f"{str(inspect.currentframe().f_code.co_name)}: É preciso de 3 coordenadas para um espaço considerado 3D. Informações dadas {coord}")
        return f"{coord[0]},{coord[1]},{coord[2]}"
    return f"{coord[0]},{coord[1]}"

def dotToComma(num:float)->str:
    return str(num).replace(".",",")

def acharHeightIdeal (texto,dx,dy,taxaEspacoAltura=1.6666,preenchimento=0.7,maxHeight=0.25,minHeight=0.1):
    if not isinstance(texto,str):
        texto = str(texto)
    textHeight = ((preenchimento/taxaEspacoAltura)*(dx*dy/len(texto)))**0.5
    
    if textHeight > maxHeight:
        textHeight = maxHeight
        print(f"! ! ! ! AVISOS - {str(inspect.currentframe().f_code.co_name)}: O textHeight é maior do que o máximo de {maxHeight}, por isso ele foi substituido.")
    if textHeight < minHeight:
        textHeight = minHeight
        print(f"! ! ! ! AVISOS - {str(inspect.currentframe().f_code.co_name)}: O textHeight é menor do que o mínimo de {minHeight}, por isso ele foi substituido.")
    return round(textHeight,2)

def listarPlanilhas(file_path:str)->list:
    # Carregar o arquivo Excel
    excel_file = pd.ExcelFile(file_path)

    # Obter os nomes das planilhas
    sheet_names = excel_file.sheet_names

    # Retornar os nomes das planilhas
    return sheet_names

def get_all_files_in_directory(directory:str)->list:
    """
    Retorna uma lista com o caminho de todos os arquivos dentro de uma pasta.

    :param directory: Caminho da pasta.
    :return: Lista de caminhos de arquivos.
    """
    file_paths = []
    
    # Percorre todos os arquivos e subdiretórios
    for root, _, files in os.walk(directory):
        for file in files:
            # Adiciona o caminho completo do arquivo à lista
            file_paths.append(os.path.join(root, file))
    
    return file_paths