from classes import (
    StyleText,
    Layer,
    Line,
    Circle,
    Text,
    MText,
    Polyline,
    Rectangle,
    Hatch,
    Block,
    Script
    )
import ezdxf
from ezdxf.lldxf.const import VALID_DXF_LINEWEIGHTS
from functions import nearest_value
from models import Model
from ezdxf import zoom
"""
ezdxf_factory.py - Factory para criar entidades DXF a partir das classes do usuário
"""

from typing import Tuple, List, Optional
import inspect

from ezdxf.enums import TextEntityAlignment as alignment
justify_map = {
    "C": alignment.CENTER,
    "L": alignment.LEFT,
    "R": alignment.RIGHT,
    "M": alignment.MIDDLE,
    "A": alignment.ALIGNED,
    "F": alignment.FIT,
    "BC": alignment.BOTTOM_CENTER,
    "BL": alignment.BOTTOM_LEFT,
    "BR": alignment.BOTTOM_RIGHT,
    "TC": alignment.TOP_CENTER,
    "TL": alignment.TOP_LEFT,
    "TR": alignment.TOP_RIGHT,
    "MC": alignment.MIDDLE_CENTER,
    "ML": alignment.MIDDLE_LEFT,
    "MR": alignment.MIDDLE_RIGHT,
}

attachment_point_map = {
    "TL": 1,
    "TC": 2,
    "TR": 3,
    "ML": 4,
    "MC": 5,
    "MR": 6,
    "BL": 7,
    "BC": 8,
    "BR": 9,
}

named_color_map = {
    "red":1,
    "yellow":2,
    "green":3,
    "cyan":4,
    "blue":5,
    "magenta":6,
    "white":7
}

# Mocks para constantes (ajuste conforme seu código)
LAYER_0 = type('Layer', (), {'name': '0'})()
STYLE_TEXT_STANDARD = type('StyleText', (), {'nameStyle': 'Standard', 'textHeight': 0.0})()

def map_color(color):
    """Mapeia cores BYLAYER para DXF"""
    if str(color).upper().strip() == "BYLAYER":
        return 256
    try:
        return int(color)
    except:
        if str(color).lower().strip() in named_color_map:
            return named_color_map[str(color).lower().strip()]
        else:
            raise Exception(f"Cor inválida: {color}")

def map_lineweight(lw):
    """Mapeia lineweight para DXF units"""
    if lw == "BYLAYER" or lw == "Default":
        return -1
    try:
        # return int(float(lw) * 10)  # mm -> 1/100 mm
        return nearest_value(lw,VALID_DXF_LINEWEIGHTS)
    except:
        return -1

def map_font (font_name):
    """Mapeia fontname para os formatados suportados no DXF"""
    if not font_name.endswith('.shx') and not font_name.endswith('.ttf'):
        return font_name + '.ttf'
    return font_name

def criar_estilo_texto(doc: ezdxf.document.Drawing, style_obj: StyleText):
    """
    Cria estilo de texto no DXF baseado na classe StyleText
    """
    # Mapeia atributos da classe para dxfattribs do ezdxf
    dxfattribs = {
        'font': map_font(style_obj.fontName),
        'height': style_obj.textHeight,
        'width_factor': style_obj.widthFactor,
        'oblique_angle': style_obj.obliqAngle
    }
    
    # Adiciona flags de texto (se suportado pelo estilo DXF)
    if style_obj.textBackwards:
        dxfattribs['text_flags'] = getattr(dxfattribs.get('text_flags', 0), 'value', 0) | 2
    if style_obj.textUpsidedown:
        dxfattribs['text_flags'] = getattr(dxfattribs.get('text_flags', 0), 'value', 0) | 4
    if style_obj.vertical:
        dxfattribs['text_flags'] = getattr(dxfattribs.get('text_flags', 0), 'value', 0) | 1
    
    # Remove atributos vazios ou zero
    dxfattribs = {k: v for k, v in dxfattribs.items() 
                  if v != 0.00 and v is not None and v != ''}
    
    # Cria o estilo
    doc.styles.add(style_obj.nameStyle, dxfattribs=dxfattribs)
    return style_obj.nameStyle

def criar_linha(doc: ezdxf.document.Drawing, line_obj: Line):
    """
    Cria linha no DXF baseada na classe Line
    """
    # Mapeia atributos da classe para dxfattribs do ezdxf
    dxfattribs = {
        'layer': line_obj.Layer.name if hasattr(line_obj.Layer, 'name') else str(line_obj.Layer)
    }
    
    # Mapeia cores BYLAYER → 256 (DXF padrão)
    if line_obj.Color != "BYLAYER":
        try:
            dxfattribs['color'] = int(line_obj.Color)
        except:
            dxfattribs['color'] = line_obj.Color
    
    # Linetype
    if line_obj.Linetype != "BYLAYER":
        dxfattribs['linetype'] = line_obj.Linetype
    
    # Lineweight (em centésimos de mm → DXF units)
    if line_obj.Lineweight != "BYLAYER":
        try:
            lw = float(line_obj.Lineweight)
            dxfattribs['lineweight'] = int(lw * 10)  # Ex: 0.5mm → 50
        except:
            dxfattribs['lineweight'] = line_obj.Lineweight
    
    # Cria a linha
    msp = doc.modelspace()
    linha = msp.add_line(
        start=line_obj.p0, 
        end=line_obj.pi,
        dxfattribs=dxfattribs
    )
    
    return linha

def criar_layer(doc: ezdxf.document.Drawing, layer_obj: Layer) -> str:
    """Cria layer no DXF"""
    try:
        doc.layers.add(
            name        = layer_obj.nameLayer,
            color       = map_color(layer_obj.Color),
            linetype    = layer_obj.Linetype,
            lineweight  = map_lineweight(layer_obj.Lineweight),
            )
    except Exception as m:
        if "already exists" in str(m):
            if layer_obj.nameLayer=="0":
                layer = doc.layers.get("0")
                layer.dxf.color = map_color(layer_obj.Color)
                layer.dxf.linetype = layer_obj.Linetype
                layer.dxf.lineweight = map_lineweight(layer_obj.Lineweight)
            else:
                raise Exception("Avaliar extrutura try/except acima dessa linha.")
        else:
            raise Exception("Avaliar extrutura try/except acima dessa linha.")
    return layer_obj.nameLayer

def criar_linha(doc: ezdxf.document.Drawing, line_obj: Line) -> ezdxf.entities.Line:
    """Cria linha no DXF"""
    dxfattribs = {
        'layer': line_obj.Layer.nameLayer if hasattr(line_obj.Layer, 'nameLayer') else '0',
        'color': map_color(line_obj.Color),
        'linetype': line_obj.Linetype,
        'lineweight': map_lineweight(line_obj.Lineweight)
    }
    return doc.modelspace().add_line(start=line_obj.p0, end=line_obj.pi, dxfattribs=dxfattribs)

def criar_circulo(doc: ezdxf.document.Drawing, circle_obj: Circle) -> ezdxf.entities.Circle:
    """Cria círculo no DXF"""
    dxfattribs = {
        'layer': circle_obj.Layer.nameLayer if hasattr(circle_obj.Layer, 'nameLayer') else '0',
        'color': map_color(circle_obj.Color),
        'linetype': circle_obj.Linetype,
        'lineweight': map_lineweight(circle_obj.Lineweight)
    }
    return doc.modelspace().add_circle(center=circle_obj.p0, radius=circle_obj.r, dxfattribs=dxfattribs)

def criar_texto(doc: ezdxf.document.Drawing, text_obj:Text) -> ezdxf.entities.Text:
    """Cria texto no DXF"""
    dxfattribs = {
        'layer': text_obj.Layer.nameLayer if hasattr(text_obj.Layer, 'nameLayer') else '0',
        'style': text_obj.style.nameStyle,
        'color': map_color(text_obj.Color),
        'height': text_obj.height if text_obj.applyHeight else 0
    }
    # Justificativa
    # justify_map = {'L': 'LEFT', 'C': 'MIDDLE_CENTER', 'R': 'RIGHT'}
    if text_obj.justify in justify_map:
        texto = doc.modelspace().add_text(text_obj.content, dxfattribs=dxfattribs)
        texto.set_placement(text_obj.p0,align=justify_map[text_obj.justify])
        texto.dxf.rotation = text_obj.rotation
        return texto

def criar_mtext(doc: ezdxf.document.Drawing, mtext_obj:MText) -> ezdxf.entities.MText:
    """Cria MText no DXF"""
    dxfattribs = {
        'layer': mtext_obj.Layer.nameLayer if hasattr(mtext_obj.Layer, 'nameLayer') else '0',
        'style': mtext_obj.style.nameStyle,
        'color': map_color(mtext_obj.Color)
    }
    
    mtext = doc.modelspace().add_mtext(
        text=mtext_obj.content,
        dxfattribs=dxfattribs,
    )
    mtext.set_location(insert=mtext_obj.p0,rotation=mtext_obj.rotation, attachment_point=attachment_point_map[mtext_obj.justify])
    mtext.set_placement(mtext_obj.p0, mtext_obj.pi, align=mtext_obj.justify)
    mtext.dxf.char_height = mtext_obj.textHeight
    mtext.dxf.width = mtext_obj.width
    mtext.dxf.rotation = mtext_obj.rotation
    mtext.dxf.line_spacing_factor = mtext_obj.lineSpacing
    return mtext

def criar_polyline(doc: ezdxf.document.Drawing, polyline_obj:Polyline) -> ezdxf.entities.LWPolyline:
    """Cria polilinha no DXF"""
    dxfattribs = {
        'layer': polyline_obj.Layer.nameLayer if hasattr(polyline_obj.Layer, 'nameLayer') else '0',
        'color': map_color(polyline_obj.Color),
        'linetype': polyline_obj.Linetype,
        'lineweight': map_lineweight(polyline_obj.Lineweight),
        'closed': polyline_obj.closed
    }
    return doc.modelspace().add_lwpolyline(polyline_obj.pSequencial, dxfattribs=dxfattribs)

def criar_retangulo(doc: ezdxf.document.Drawing, rect_obj: Rectangle) -> ezdxf.entities.LWPolyline:
    """Cria retângulo como POLYLINE fechada no DXF"""
    x0, y0 = rect_obj.p0
    x1, y1 = rect_obj.pi
    
    # 4 vértices do retângulo (no sentido horário)
    vertices = [
        (x0, y0),
        (x1, y0),
        (x1, y1),
        (x0, y1)
    ]
    
    dxfattribs = {
        'layer': rect_obj.Layer.nameLayer if hasattr(rect_obj.Layer, 'nameLayer') else '0',
        'color': map_color(rect_obj.Color),
        'linetype': rect_obj.Linetype,
        'lineweight': map_lineweight(rect_obj.Lineweight),
        'closed': True  # Fecha automaticamente
    }
    
    return doc.modelspace().add_lwpolyline(vertices, dxfattribs=dxfattribs)

def criar_hatch(doc: ezdxf.document.Drawing, hatch_obj: Hatch) -> ezdxf.entities.Hatch:
    """Cria hatch no DXF (simplificado - precisa de boundary)"""
    # Cria círculo auxiliar como boundary para o hatch
    circle = doc.modelspace().add_circle(hatch_obj.p0, radius=10, visible=False)
    
    dxfattribs = {
        'layer': hatch_obj.Layer.nameLayer if hasattr(hatch_obj.Layer, 'nameLayer') else '0',
        'color': map_color(hatch_obj.Color),
        'pattern_name': hatch_obj.pattern,
        'scale': hatch_obj.scale,
        'rotation': hatch_obj.angle,
        'linetype': hatch_obj.Linetype,
        'lineweight': map_lineweight(hatch_obj.Lineweight)
    }
    
    hatch = doc.modelspace().add_hatch(dxfattribs=dxfattribs)
    hatch.paths.add_face_path(circle, True)  # Usa círculo como boundary
    circle.delete()
    return hatch

def criar_blockref(doc: ezdxf.document.Drawing, block_obj: Block) -> ezdxf.entities.Insert:
    """Cria referência de bloco no DXF"""
    # Simplificado - assume bloco já existe ou é padrão
    dxfattribs = {
        'layer': block_obj.Layer.nameLayer if hasattr(block_obj.Layer, 'nameLayer') else '0',
        'color': map_color(block_obj.Color),
        'linetype': block_obj.Linetype,
        'lineweight': map_lineweight(block_obj.Lineweight)
    }
    
    # Cria bloco simples se não existir
    if block_obj.block_path not in doc.blocks.names():
        blk = doc.blocks.new(block_obj.block_path)
        blk.add_circle((0,0), radius=1)  # Placeholder
    
    blockref = doc.modelspace().add_blockref(block_obj.block_path, block_obj.p0, dxfattribs=dxfattribs)
    blockref.dxf.scale = (block_obj.scale_factor, block_obj.scale_factor)
    blockref.dxf.rotation = block_obj.rotation_angle
    return blockref

# Função principal para processar lista de objetos
def desenhar_objetos(doc: ezdxf.document.Drawing, objetos: list):
    """Processa lista de objetos e cria no DXF"""
    # Primeiro cria todos os layers e estilos
    for obj in objetos:
        if isinstance(obj, Layer):
            criar_layer(doc, obj)
        elif hasattr(obj, 'style') and isinstance(obj.style, StyleText):
            doc.styles.add(obj.style.nameStyle, font=obj.style.fontName, dxfattribs={
                'height': obj.style.textHeight,
                "width": obj.style.widthFactor,
                "oblique": obj.style.obliqAngle,
            })
    
    # Depois cria entidades
    entidades = []
    for obj in objetos:
        if isinstance(obj, Layer):
            continue
        elif isinstance(obj, Line):
            entidades.append(criar_linha(doc, obj))
        elif isinstance(obj, Circle):
            entidades.append(criar_circulo(doc, obj))
        elif isinstance(obj, Text):
            entidades.append(criar_texto(doc, obj))
        elif isinstance(obj, MText):
            entidades.append(criar_mtext(doc, obj))
        elif isinstance(obj, Polyline):
            entidades.append(criar_polyline(doc, obj))
        elif isinstance(obj, Rectangle):
            entidades.extend(criar_retangulo(doc, obj))
        elif isinstance(obj, Hatch):
            ...
            # Ignorar por hora os hatchs (eles precisam de áreas definidas por objetos - criar objetos em layers invisíveis para usar como boundary)
            # entidades.append(criar_hatch(doc, obj))
        elif isinstance(obj, Block):
            entidades.append(criar_blockref(doc, obj))
    
    return entidades

# Exemplo de uso:
if __name__ == "__main__":
    doc = ezdxf.new("R2010", setup=True)
    
    # Exemplo com suas classes
    layer1 = Layer("MEU_LAYER", "green", "DASHED", "0.35")
    circulo = Circle((50,50), 5, layer1, Color=2)
    texto = Text((60,60), "Teste", STYLE_TEXT_STANDARD, layer1)
    
    desenhar_objetos(doc, [layer1, circulo, texto])
    doc.saveas("teste_classes.dxf")


def model_to_doc_dxf(model:Model):
    
    doc = ezdxf.new("R2010", setup=True)
    script:Script = model.script
    desenhar_objetos(
        doc = doc,
        objetos = script.Layers + script.Styles + script.elementos
    )
    msp = doc.modelspace()
    zoom.extents(msp)
    doc.saveas(f"{script.nome_arquivo}.dxf")
    return doc