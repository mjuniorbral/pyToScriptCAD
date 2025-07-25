class Projetora():
    def __init__(self):
        self.tem_reta = False
        self.tem_perpendicular = False
        self.tem_projecao = False
        pass
    def definir_reta_por_dois_pts(self,xA,yA,xB,yB):
        self.m = (yB-yA)/(xB-xA)
        self.n = yA - self.m*xA
        self.x0 = xA
        self.y0 = yA
        self.tem_reta = True
    def definir_reta_perpendicular_a_reta_passando_pelo_pt(self,xP,yP):
        if not self.tem_reta:
            raise Exception()
        self.ms = 1/self.m
        self.ns = yP - self.ms*xP
        self.tem_perpendicular = True
    def definir_ponto_de_projecao_orto_sobre_a_reta(self):
        if not self.tem_perpendicular:
            raise Exception()
        self.xProj = (self.ns-self.n)/(self.m-self.ms)
        self.yProj = self.m*self.xProj + self.n
        if self.yProj != self.ms*self.xProj + self.ns: # Prova real
            raise Exception()
        self.tem_projecao = True
    def definir_posicao_horizontal_na_secao_do_p0(self):
        if not self.tem_projecao:
            raise Exception()
        self.dist_Proj_to_0 = ((self.xProj-self.x0)**2+(self.yProj-self.y0)**2)**0.5
    def run_Projetora(self,xA,yA,xB,yB,xP,yP):
        self.definir_reta_por_dois_pts(xA,yA,xB,yB)
        self.definir_reta_perpendicular_a_reta_passando_pelo_pt(xP,yP)
        self.definir_ponto_de_projecao_orto_sobre_a_reta()
        self.definir_posicao_horizontal_na_secao_do_p0()