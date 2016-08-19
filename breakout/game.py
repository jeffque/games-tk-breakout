import tkinter as tk
from enum import Enum

class TipoColisao(Enum):
    NAO_COLIDIU = 0
    FROM_ESQUERDA = 1
    FROM_CIMA = 2
    FROM_DIREITA = 3
    FROM_BAIXO = 4

class Bola:
    radius = 10

    def __init__(self, canvas, position_center = (0,0), velocity = (-10, +10)):
        self.canvas = canvas
        self.bola = canvas.create_oval(
            position_center[0] - Bola.radius / 2, position_center[1] - Bola.radius / 2,
            position_center[0] + Bola.radius / 2, position_center[1] + Bola.radius / 2,
            fill='BLUE')
        self.position_center = []
        self.position_center.append(position_center[0])
        self.position_center.append(position_center[1])
        self.velocity = velocity


    def move(self):
        self.position_center[0] = self.position_center[0] + self.velocity[0]
        self.position_center[1] = self.position_center[1] + self.velocity[1]
        self.canvas.move(self.bola, self.velocity[0], self.velocity[1])


class Raquete:
    width = 100
    height = 20
    '''
    canvas é o canvas onde ainda vou desenhar o retângulo da raquete

    position_center é o centro da raquete, no mundo x, y
    '''
    def __init__(self, canvas, position_center = (0,0)):
        self.canvas = canvas
        self.rectangle = canvas.create_rectangle(
            position_center[0] - Raquete.width/2, position_center[1] - Raquete.height/2,
            position_center[0] + Raquete.width/2, position_center[1] + Raquete.height/2,
            fill = 'RED')
        self.position_center = []
        self.position_center.append(position_center[0])
        self.position_center.append(position_center[1])
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
        self.start = True
        self.game_loop()
        print('start game')


    def game_loop(self):
        self.bola.move()
        self.after(100, self.game_loop)

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
        self.bola = Bola(self.canvas, (self.canvas.winfo_reqwidth()/2, self.canvas.winfo_reqheight() - 2*30))
