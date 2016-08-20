from .tipo_colisao import TipoColisao


def pitagoras(coordenada):
    return (coordenada[0]**2 + coordenada[1]**2)**0.5


class Geometrico:
    def __init__(self, position_center):
        self.position_center = []
        self.position_center.append(position_center[0])
        self.position_center.append(position_center[1])

    def __sub__(self, other):
        delta = []
        delta.append(self.position_center[0] - other.position_center[0])
        delta.append(self.position_center[1] - other.position_center[1])
        return delta

class Circulo(Geometrico):
    def __init__(self, position_center, radius):
        Geometrico.__init__(self, position_center)
        self.radius = radius

    def colidiu(self, rectangle):
        delta = self - rectangle
        distancia = pitagoras(delta)
        if (distancia <= self.radius + rectangle.diagonal):
            # é candidato a colidir se delta_x for menor ou igual a raio + meio comprimento
            if (abs(delta[0]) <= self.radius + rectangle.width/2 and abs(delta[1]) <= self.radius + rectangle.height/2):
                # se delta_x > delta_y em termos absolutos, então é colisão horizontal
                # caso contrário é vertical
                if (abs(delta[0]) - rectangle.width/2 >= abs(delta[1]) - rectangle.height/2):
                    return TipoColisao.FROM_DIREITA if delta[0] < 0 else TipoColisao.FROM_ESQUERDA
                else:
                    return TipoColisao.FROM_BAIXO if delta[0] < 0 else TipoColisao.FROM_CIMA
        return TipoColisao.NAO_COLIDIU

    def __str__(self):
        return "(x=%s,y=%s,r=%s)" % (self.position_center[0], self.position_center[1], self.radius)

class Retangulo(Geometrico):
    def __init__(self, position_center, width, height):
        Geometrico.__init__(self, position_center)
        self.width = width
        self.height = height
        self.diagonal = pitagoras([width/2, height/2])

    def __str__(self):
        return "(x0=%s,y0=%s,x1=%s,y1=%s)" % (self.position_center[0] - self.width/2, self.position_center[1] - self.height/2,
                                              self.position_center[0] + self.width/2, self.position_center[1] + self.height/2)
