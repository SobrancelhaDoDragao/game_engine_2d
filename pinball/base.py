"""
Classes bases para serem implementadas
"""
from abc import ABC, abstractmethod

import pymunk


class AbstractMap(ABC):
    """
    Classe abstrada para criação de mapas
    """

    SEGMENT_THICKNESS = 5
    SEGMENT_COLOR = (4, 41, 64, 255)
    SEGMENT_FRICTION = 0.4
    SEGMENT_ELASTICITY = 0.5

    STATIC_POLY_ELASTICY = 1
    STATIC_POLY_FRICTION = 0.2
    STATIC_POLY_COLOR = (214, 213, 142, 255)

    STATIC_BALL_ELASTICY = 1
    STATIC_BALL_FRICTION = 0.2
    STATIC_BALL_COLOR = (214, 213, 142, 255)

    FLIPPER_COLOR = (219, 242, 39, 255)
    LAUNCHER_COLOR = (214, 213, 142, 255)
    BALL_COLOR = (0, 92, 83, 255)

    def __init__(self, win_size, space):
        self.space = space
        self.screen_width = win_size[0]
        self.screen_height = win_size[1]

        self.segments = []
        self.polys = []
        self.balls = []

    def draw_map(self):
        """
        Funcao que desenha o mapa do jogo
        """
        self.create_segments()
        self.create_polys()
        self.create_balls()

        for segment in self.segments:
            self.create_static_segment(*segment)

        for poly in self.polys:
            self.create_static_poly(*poly)

        for ball in self.balls:
            self.create_static_ball(*ball)

    def create_static_segment(self, from_, to_):
        """
        Função para criar um segmento
        Parâmentros: posição do começo, mais posição do final
        """
        # posição
        segment_shape = pymunk.Segment(
            self.space.static_body, from_, to_, self.SEGMENT_THICKNESS
        )
        # Propriedades do segmento
        segment_shape.color = self.SEGMENT_COLOR
        segment_shape.friction = self.SEGMENT_FRICTION
        segment_shape.elasticity = self.SEGMENT_ELASTICITY
        self.space.add(segment_shape)

    def create_static_poly(self, polygon, pos):
        """
        Funcao que cria um poligono statico
        """
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = pos
        shape = pymunk.Poly(body, polygon)
        shape.elasticity = self.STATIC_POLY_ELASTICY
        shape.friction = self.STATIC_POLY_FRICTION
        shape.color = self.STATIC_POLY_COLOR
        self.space.add(body, shape)

    def create_static_ball(self, radius, pos):
        """
        Funcao para criar uma bola static no mapa
        """
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = pos
        shape = pymunk.Circle(body, radius)
        shape.elasticity = self.STATIC_BALL_ELASTICY
        shape.friction = self.STATIC_BALL_FRICTION
        shape.color = self.STATIC_BALL_COLOR
        self.space.add(body, shape)

    @property
    def flippers_color(self):
        """
        Metodo que retorna a cor do flipper
        """
        return self.FLIPPER_COLOR

    @property
    def launcher_color(self):
        """
        Metodo que retona a cor do laucher
        """
        return self.LAUNCHER_COLOR

    @property
    def ball_color(self):
        """
        Metodo que retona a cor do laucher
        """
        return self.BALL_COLOR

    @abstractmethod
    def create_segments(self):
        """
        Metodo que deve criar todos os segmentos e adicionar na self.segments
        """
        pass

    @abstractmethod
    def create_polys(self):
        """
        Metodo que deve criar todos os poligonos e adicionar na self.polys
        """
        pass

    @abstractmethod
    def create_balls(self):
        """
        Metodo que deve criar todas as bolas e adicionar no self.balls
        """
        pass

    @abstractmethod
    def flippers_position(self):
        """
        Metodo que retorna a posicao que deve ficar os flippers
        """
        pass

    @abstractmethod
    def ball_creation_position(self):
        """
        Metodo que retorna a posicao que deve ser criada
        """
        pass
