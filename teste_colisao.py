from breakout.game import Bola, Tijolo, tempo_after
from breakout.tipo_colisao import TipoColisao
from tartaruga import draw_colisao

import tkinter as tk

class BreakoutGameDummy(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.start = False
        self.master.title("Breaker!!")
        self.grid()
        self.score_value = 0
        self.colisao_text_var = tk.StringVar()
        self.bola_text_var = tk.StringVar()
        self.tijolo_text_var = tk.StringVar()
        self.create_widgets()


    def start_game(self):
        if (self.start):
            print('cara, você já começou o jogo!')
            return
        self.start = True
        print('start game')
        self.game_loop()


    def game_loop(self):
        self.bola.move()
        # bola foi pra baixo demais...
        if (self.bola.position_center[1] - self.bola.radius > self.canvas.winfo_reqheight()):
            self.start = False
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
            colisao_raquete = TipoColisao.NAO_COLIDIU
            if (colisao_raquete != TipoColisao.NAO_COLIDIU):
                self.bola.processar_colicao(colisao_raquete)
            # testar colisão com tijolos
            else:
                for tijolo in self.tijolos:
                    colisao_tijolo = self.bola.colidiu(tijolo)
                    if (colisao_tijolo != TipoColisao.NAO_COLIDIU):
                        self.colisao_coisas(colisao_tijolo, self.bola, tijolo, self.canvas_turtle)
                        break
        if (self.start):
            self.after(tempo_after, self.game_loop)


    def colisao_coisas(self, colisao_tijolo, bola, tijolo, canvas_turtle):
        print('colisão (%s) com o tijolo de id %d' % (colisao_tijolo, tijolo.rectangle))
        print('bola %s tijolo %s' % (bola, tijolo))
        self.colisao_text_var.set(colisao_tijolo)
        draw_colisao(bola, tijolo, canvas_turtle)
        self.bola.processar_colicao(colisao_tijolo)
        self.remove_tijolo(tijolo)


    def remove_tijolo(self, tijolo):
        print('id do tijolo %s' % tijolo.rectangle)
        self.canvas.delete(tijolo.rectangle)
        self.tijolos.remove(tijolo)
        self.start = False


    def create_widgets(self):
        self.score_label = tk.Label(self, textvariable=self.colisao_text_var, height=1, width = 30, bg='#000000', fg ='#ff0000')
        self.score_label.grid(row=0, column=0, sticky=tk.W + tk.N + tk.S + tk.E,
                              padx=(10,0), pady=(5,0))
        self.bola_label = tk.Label(self, textvariable=self.bola_text_var, height=1, width = 30)
        self.bola_label.grid(row=1, column=0, sticky=tk.W + tk.N + tk.S + tk.E,
                              padx=(10,0), pady=(5,0))
        self.tijolo_label = tk.Label(self, textvariable=self.tijolo_text_var, height=1, width=30)
        self.tijolo_label.grid(row=2, column=0, sticky=tk.W + tk.N + tk.S + tk.E,
                             padx=(10, 0), pady=(5, 0))
        self.btn_start = tk.Button(self, text = 'Start', command = self.start_game)
        self.btn_start.grid(row = 0, column = 1)

        self.canvas = tk.Canvas(self, height=480, width=800)
        self.canvas.grid(column=1, row=3)
        self.posicionar_elementos_inicial()
        self.canvas_turtle = tk.Canvas(self, height=480, width=800)
        self.canvas_turtle.grid(column=0, row=3)


    def posicionar_elementos_inicial(self):
        self.bola = Bola(self.canvas, (self.canvas.winfo_reqwidth() / 2, self.canvas.winfo_reqheight() - 2 * 30))
        self.tijolos = []

        for row in range(0, 6):
            for column in range(0, 3):
                pos_x = row * Tijolo.width + 80
                pos_y = column * Tijolo.height + 80
                tijolo = Tijolo(self.canvas, 'GREEN', (pos_x, pos_y))
                self.tijolos.append(tijolo)
        pos_x_bola = 3 * Tijolo.width + 80
        pos_y_bola = 3 * Tijolo.height + 80
        self.bola = Bola(self.canvas, (pos_x_bola, pos_y_bola))

        for row in range(0, 6):
            if row == 3:
                continue
            for column in range(3, 5):
                pos_x = row * Tijolo.width + 80
                pos_y = column * Tijolo.height + 80
                tijolo = Tijolo(self.canvas, 'GREEN', (pos_x, pos_y))
                self.tijolos.append(tijolo)
        for row in range(0, 6):
            for column in range(5, 9):
                pos_x = row * Tijolo.width + 80
                pos_y = column * Tijolo.height + 80
                tijolo = Tijolo(self.canvas, 'GREEN', (pos_x, pos_y))
                self.tijolos.append(tijolo)


def create_dummy_game():
    gameboard = BreakoutGameDummy()
    return gameboard


create_dummy_game().mainloop()
