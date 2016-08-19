from enum import Enum


class TipoColisao(Enum):
    NAO_COLIDIU = 0
    FROM_ESQUERDA = 1
    FROM_CIMA = 2
    FROM_DIREITA = 3
    FROM_BAIXO = 4
