import ezdxf

# Carregar o arquivo DXF
doc = ezdxf.readfile("modules\ASV.dxf")

# Acessar o modelspace
msp = doc.modelspace()

# Buscar todas as polilinhas (LWPolyline ou POLYLINE)
polylines = msp.query('LWPOLYLINE POLYLINE')

with open("modules\pontos.txt",mode="w") as arquivo:
    for i,polyline in enumerate(polylines):
        print(f"Polilinha: {polyline.dxftype()}, Handle: {polyline.dxf.handle}")
        
        with polyline.points() as pts:
            points = list(pts)
            layer = polyline.dxf.layer
            for j, point in enumerate(points):
                x = float(point[0])
                y = float(point[1])
                print(f"{i+1}\t{j+1}\t{x}\t{y}\t{layer}",file=arquivo)