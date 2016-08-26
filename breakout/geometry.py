from .tipo_colisao import TipoColisao

def pitagoras_quad(coordenada):
    return coordenada[0] ** 2 + coordenada[1] ** 2

def pitagoras(coordenada):
    return pitagoras_quad(coordenada)**0.5


def coords_delta(coord_a, coord_b):
    delta = []
    delta.append(coord_a[0] - coord_b[0])
    delta.append(coord_a[1] - coord_b[1])
    return delta


def distances(referencia, outros):
    return [coords_delta(referencia, outro) for outro in outros]


def closest(referencia, outros):
    mais_proximos = []
    dist_base = pitagoras_quad(coords_delta(referencia, outros[0]))
    for outro in outros:
        dist_comp = pitagoras_quad(coords_delta(referencia, outro))
        if dist_comp < dist_base:
            mais_proximos = [outro]
        elif dist_comp == dist_base:
            mais_proximos.append(outro)
    return mais_proximos


class Geometrico:
    def __init__(self, position_center):
        self.position_center = []
        self.position_center.append(position_center[0])
        self.position_center.append(position_center[1])

    def __sub__(self, other):
        return coords_delta(self.position_center, other.position_center)


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


    def four_points(self):
        mid_width = self.width/2
        mid_height = self.height/2
        return ((self.position_center[0] - mid_width, self.position_center[1] - mid_height),
                (self.position_center[0] - mid_width, self.position_center[1] + mid_height),
                (self.position_center[0] + mid_width, self.position_center[1] + mid_height),
                (self.position_center[0] + mid_width, self.position_center[1] - mid_height))
