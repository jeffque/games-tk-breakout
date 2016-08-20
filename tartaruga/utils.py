import turtle

def draw_colisao(bola, retangulo, canvas):
    print('colisao de bola %s com retangulo %s' % (bola, retangulo))

    canvas.delete('all')
    tortuguita = turtle.RawTurtle(canvas)
    # desenhar o retângulo..
    tortuguita.forward(retangulo.width)
    tortuguita.left(90)
    tortuguita.forward(retangulo.height)
    tortuguita.left(90)
    tortuguita.forward(retangulo.width)
    tortuguita.left(90)
    tortuguita.forward(retangulo.height)
    tortuguita.left(90)

    # posicionar a tartaruga para o desenho
    inferior_esquerdo_retangulo = (retangulo.position_center[0] - retangulo.width / 2, retangulo.position_center[1] + retangulo.height / 2)
    centro_relativo_bola = (bola.position_center[0] - inferior_esquerdo_retangulo[0], bola.position_center[1] - inferior_esquerdo_retangulo[1])

    tortuguita.penup()
    tortuguita.forward(centro_relativo_bola[0])
    tortuguita.right(90)
    # pondo a tartaruga no ponto mais inferior da bola
    tortuguita.forward(centro_relativo_bola[1] + bola.radius)
    tortuguita.left(90)
    tortuguita.pendown()

    tortuguita.circle(bola.radius)
