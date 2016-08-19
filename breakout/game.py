import tkinter as tk

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

class Retangulo(Geometrico):
    def __init__(self, position_center, width, height):
        Geometrico.__init__(self, position_center)
        self.width = width
        self.height = height
        self.diagonal = pitagoras([width/2, height/2])


class Bola(Circulo):
    radius = 5
    def __init__(self, canvas, position_center = (0,0), velocity = (-5, +5)):
        Circulo.__init__(self, position_center, Bola.radius)
        self.canvas = canvas
        self.bola = canvas.create_oval(
            position_center[0] - Bola.radius, position_center[1] - Bola.radius,
            position_center[0] + Bola.radius, position_center[1] + Bola.radius,
            fill='BLUE')
        self.velocity = velocity


    def move(self):
        self.position_center[0] = self.position_center[0] + self.velocity[0]
        self.position_center[1] = self.position_center[1] + self.velocity[1]
        self.canvas.move(self.bola, self.velocity[0], self.velocity[1])

    def processar_colicao(self, tipo_colisao):
        if (tipo_colisao == TipoColisao.FROM_BAIXO):
            self.velocity = (self.velocity[0], -abs(self.velocity[1]))
        elif (tipo_colisao == TipoColisao.FROM_CIMA):
            self.velocity = (self.velocity[0], abs(self.velocity[1]))
        elif (tipo_colisao == TipoColisao.FROM_DIREITA):
            self.velocity = (-abs(self.velocity[0]), self.velocity[1])
        elif (tipo_colisao == TipoColisao.FROM_ESQUERDA):
            self.velocity = (abs(self.velocity[0]), self.velocity[1])

class Raquete(Retangulo):
    width = 100
    height = 20
    '''
    canvas é o canvas onde ainda vou desenhar o retângulo da raquete

    position_center é o centro da raquete, no mundo x, y
    '''
    def __init__(self, canvas, position_center = (0,0)):
        Retangulo.__init__(self, position_center, Raquete.width, Raquete.height)
        self.canvas = canvas
        self.rectangle = canvas.create_rectangle(
            position_center[0] - Raquete.width/2, position_center[1] - Raquete.height/2,
            position_center[0] + Raquete.width/2, position_center[1] + Raquete.height/2,
            fill = 'RED')
        print('posições da raquete (self.position_center): %s' % self.position_center)

    def move_to(self, x):
        print('chamando move_to da raquete para %d' % x)
        delta = x - self.position_center[0]
        print('valores envolvidos: position_cener[0] %d x %d delta %d' % (self.position_center[0], x, delta))
        self.canvas.move(self.rectangle, delta, 0)
        self.position_center[0] = x


class BreakoutGame(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.start = False
        self.master.title("Breaker!!")
        self.grid()
        self.score_value = 0
        self.score_text_var = tk.StringVar()
        self.add_score(0)
        self.create_widgets()
        self.bind_eventos()


    def add_score(self, plus):
        self.score_value += plus
        self.score_text_var.set("Score: %d" % self.score_value)
        print('score? %d' % self.score_value)


    def start_game(self):
        if (self.start):
            print('cara, você já começou o jogo!')
            return
        self.start = True
        self.raquete.move_to(self.canvas.winfo_reqwidth()/2)
        if (self.bola != None):
            self.canvas.delete(self.bola.bola)
        self.bola = Bola(self.canvas, (self.canvas.winfo_reqwidth() / 2, self.canvas.winfo_reqheight() - 2 * 30))
        print('start game')
        self.game_loop()


    def game_loop(self):
        self.bola.move()
        # bola foi pra baixo demais...
        if (self.bola.position_center[1] - self.bola.radius > self.canvas.winfo_reqheight()):
            self.start = False
            self.add_score(-1)
            print('bola vazou, perdeu ponto')
        # bateu de cima...
        elif (self.bola.position_center[1] - self.bola.radius < 0):
            self.bola.processar_colicao(TipoColisao.FROM_CIMA)
        # bateu da esquerda...
        elif (self.bola.position_center[0] - self.bola.radius < 0):
            self.bola.processar_colicao(TipoColisao.FROM_ESQUERDA)
        # bateu da direita...
        elif (self.bola.position_center[0] + self.bola.radius > self.canvas.winfo_reqwidth()):
            self.bola.processar_colicao(TipoColisao.FROM_DIREITA)
        # não bateu de nenhuma borda, verificar colisões com outros objetos
        else:
            colisao_raquete = self.bola.colidiu(self.raquete)
            print('colisao raqute %s' % colisao_raquete)
            if (colisao_raquete != TipoColisao.NAO_COLIDIU):
                self.bola.processar_colicao(colisao_raquete)
        if (self.start):
            self.after(50, self.game_loop)


    def create_widgets(self):
        self.score_label = tk.Label(self, textvariable=self.score_text_var, height=1, width = 30, bg= '#000000', fg = '#ff0000')
        self.score_label.grid(row=0, column=0, sticky=tk.W + tk.N + tk.S + tk.E,
                              padx=(10,0), pady=(5,0))
        self.btn_start = tk.Button(self, text = 'Start', command = self.start_game)
        self.btn_start.grid(row = 0, column = 1)

        self.canvas = tk.Canvas(self, height=480, width=800)
        self.canvas.grid(column=1, row=1)
        self.posicionar_elementos_inicial()


    def move_raquete(self, x):
        if (not self.start):
            return
        self.raquete.move_to(x)


    def bind_eventos(self):
        self.canvas.bind('<Button-1>', lambda event : self.move_raquete(event.x))


    def posicionar_elementos_inicial(self):
        self.raquete = Raquete(self.canvas, (self.canvas.winfo_reqwidth()/2, self.canvas.winfo_reqheight() - 30))
        self.bola = None
