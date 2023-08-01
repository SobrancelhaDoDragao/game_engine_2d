from map import MainMap
import pygame as pg
import pymunk.pygame_util

class PysicsEngine2D:
    """
    Classe criada para gerenciar a fisica do jogo
    """
    BALL_MASS = 1
    BALL_RADIUS = 7
    BALL_ELASTICITY = 0.9
    BALL_FRICTION = 0.1
    GRAVITY = 0,2000
    SEGMENT_THICKNESS = 4
    
    def __init__(self,game):
        self.screen = game.screen
        pymunk.pygame_util.positive_y_is_up = False
        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)
        self.space = pymunk.Space()
        self.space.gravity = self.GRAVITY
        self.FPS = game.FPS

        self.map = MainMap(game.WIN_SIZE,self.space)
        self.map.draw_map()

    def update(self):
        self.screen.fill(pg.Color('white'))
        self.space.step(1/self.FPS)
        self.space.debug_draw(self.draw_options)

    def new_ball(self,pos):
        ball_moment = pymunk.moment_for_circle(self.BALL_MASS,0,self.BALL_RADIUS)
        ball_body = pymunk.Body(self.BALL_MASS,ball_moment)
        ball_body.position = pos
        ball_shape = pymunk.Circle(ball_body,self.BALL_RADIUS)
        ball_shape.elasticity = self.BALL_ELASTICITY
        ball_shape.friction = self.BALL_FRICTION
        self.space.add(ball_body,ball_shape)
    