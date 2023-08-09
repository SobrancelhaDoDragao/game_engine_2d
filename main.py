"""
Arquivo principal do projeto. Nesse arquivo todos os arquivos sao chamados
"""
import pygame as pg

from engine import PysicsEngine2D


class Game:
    """
    Classe principal criada para gerenciar o jogo
    """

    WIDTH, HEIGHT = 800, 600
    WIN_SIZE = WIDTH, HEIGHT
    FPS = 60

    def __init__(self):
        self.game_engine = pg
        self.game_engine.init()
        self.running = True
        self.screen = self.game_engine.display.set_mode(size=self.WIN_SIZE)
        self.clock = self.game_engine.time.Clock()
        self.pysics_engine = PysicsEngine2D(self)

    def update(self):
        """
        Atualiza a tela do jogo
        """
        self.game_engine.display.set_caption(f"{self.clock.get_fps() :.0f}")
        self.screen.fill(pg.Color("white"))
        self.pysics_engine.update()
        pg.display.flip()
        self.clock.tick(self.FPS)

    def run(self):
        """
        Funcao que executa o jogo
        """
        while self.running:
            self.keyboard_events()
            self.update()

    def keyboard_events(self):
        """
        Funcao para gerenciar inputs do teclado
        """
        for event in self.game_engine.event.get():
            if event.type == self.game_engine.QUIT:
                self.running = False
            elif (
                event.type == self.game_engine.KEYDOWN
                and event.key == self.game_engine.K_ESCAPE
            ):
                self.running = False
            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:  # LMB
                self.pysics_engine.new_ball(event.pos)
            elif event.type == pg.KEYDOWN and event.key == pg.K_RIGHT:
                self.pysics_engine.botao()
            elif event.type == pg.KEYDOWN and event.key == pg.K_LEFT:
                self.pysics_engine.botaoleft()


# Caso o arquivo esteja sendo executado diretamente como arquivo principal
if __name__ == "__main__":
    app = Game()
    app.run()
