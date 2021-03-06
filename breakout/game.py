import tkinter as tk

from .tipo_colisao import TipoColisao
from .geometry import Circulo,Retangulo

deslocamento_base = 0.1
tempo_after = 10
velocidade_bola = tempo_after*deslocamento_base

class Bola(Circulo):
    radius = 5
    def __init__(self, canvas, position_center = (0,0), velocity = (-velocidade_bola, +velocidade_bola)):
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


class Tijolo(Retangulo):
    width = 120
    height = 40
    def __init__(self, canvas, color, position_center = (0,0)):
        Retangulo.__init__(self, position_center, Tijolo.width, Tijolo.height)
        self.canvas = canvas
        self.rectangle = canvas.create_rectangle(
            position_center[0] - Tijolo.width/2, position_center[1] - Tijolo.height/2,
            position_center[0] + Tijolo.width/2, position_center[1] + Tijolo.height/2,
            fill = color)


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


    def move_to(self, x):
        print('chamando move_to da raquete para %d' % x)
        delta = x - self.position_center[0]
        if delta != 0:
            self.canvas.move(self.rectangle, delta, 0)
            self.position_center[0] = x
            self.redef_four_points()


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
            if (colisao_raquete != TipoColisao.NAO_COLIDIU):
                self.bola.processar_colicao(colisao_raquete)
            # testar colisão com tijolos
            else:
                for tijolo in self.tijolos:
                    colisao_tijolo = self.bola.colidiu(tijolo)
                    if (colisao_tijolo != TipoColisao.NAO_COLIDIU):
                        self.bola.processar_colicao(colisao_tijolo)
                        self.remove_tijolo(tijolo)
                        break
        if (self.start):
            self.after(tempo_after, self.game_loop)


    def remove_tijolo(self, tijolo):
        self.canvas.delete(tijolo.rectangle)
        self.tijolos.remove(tijolo)
        self.add_score(1)


    def create_widgets(self):
        self.score_label = tk.Label(self, textvariable=self.score_text_var, height=1, width = 30, bg= '#000000', fg = '#ff0000')
        self.score_label.grid(row=0, column=0, sticky=tk.W + tk.N + tk.S + tk.E,
                              padx=(10,0), pady=(5,0))
        self.btn_start = tk.Button(self, text = 'Start', command = self.start_game)
        self.btn_start.grid(row = 0, column = 1)

        self.canvas = tk.Canvas(self, height=480, width=800, background = 'WHITE')
        self.canvas.grid(column=1, row=1)
        self.posicionar_elementos_inicial()


    def move_raquete(self, x):
        if (not self.start):
            return
        self.raquete.move_to(x)
        print(self.raquete.four_points)


    def bind_eventos(self):
        self.canvas.bind('<Button-1>', lambda event : self.move_raquete(event.x))


    def posicionar_elementos_inicial(self):
        self.raquete = Raquete(self.canvas, (self.canvas.winfo_reqwidth()/2, self.canvas.winfo_reqheight() - 30))
        print(self.raquete)
        print(self.raquete.four_points)
        self.bola = None
        self.tijolos = []

        for row in range(0, 6):
            for column in range(0, 3):
                pos_x = row * Tijolo.width + 80
                pos_y = column * Tijolo.height + 80
                tijolo = Tijolo(self.canvas, 'GREEN', (pos_x, pos_y))
                self.tijolos.append(tijolo)
