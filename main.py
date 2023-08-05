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
        self.screen = pg.display.set_mode(size=self.WIN_SIZE)
        self.clock = pg.time.Clock()
        self.PysicsEngine = PysicsEngine2D(self)
       
    def update(self):
        self.game_engine.display.set_caption(f'{self.clock.get_fps() :.0f}')
        self.screen.fill(pg.Color('white'))
        self.PysicsEngine.update()
        pg.display.flip()
        self.clock.tick(self.FPS)
    
    def draw(self):
        pass

    def run(self):
        while self.running:
            self.keyboard_events()
            self.update()

    def keyboard_events(self):
        for event in self.game_engine.event.get():
            if event.type == self.game_engine.QUIT:
                self.running = False
            elif event.type == self.game_engine.KEYDOWN and event.key == self.game_engine.K_ESCAPE:
                self.running = False
            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1: # LMB
                self.PysicsEngine.new_ball(event.pos)
            elif event.type == pg.KEYDOWN and event.key == pg.K_RIGHT:
                self.PysicsEngine.botao()
            elif event.type == pg.KEYDOWN and event.key == pg.K_LEFT:
                self.PysicsEngine.botaoleft()

# Caso o arquivo esteja sendo executado diretamente como arquivo principal
if __name__ == "__main__":
    app = Game()
    app.run()
