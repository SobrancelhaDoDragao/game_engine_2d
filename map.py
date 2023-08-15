"""
Classes para criação de mapas do pinball
"""
from abc import ABC, abstractmethod

import pygame as pg
import pymunk


class AbstractMap(ABC):
    """
    Classe abstrada para criação de mapas
    """

    SEGMENT_THICKNESS = 5
    SEGMENT_COLOR = pg.Color("black")
    SEGMENT_FRICTION = 0.4
    SEGMENT_ELASTICITY = 0.5

    STATIC_POLY_ELASTICY = 1
    STATIC_POLY_FRICTION = 0.2
    STATIC_POLY_COLOR = pg.Color("green")

    STATIC_BALL_ELASTICY = 1
    STATIC_BALL_FRICTION = 0.2
    STATIC_BALL_COLOR = pg.Color("green")

    def __init__(self, win_size, space):
        self.space = space
        self.screen_width = win_size[0]
        self.screen_height = win_size[1]

        self.platforms = []

    def draw_map(self):
        """
        Funcao que desenha o mapa do jogo
        """
        self.create_elements()

        for plataform in self.platforms:
            self.create_segment(*plataform)

    def create_segment(self, from_, to_):
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

    def create_a_static_ball(self, pos, radius):
        """
        Funcao para criar um bola static no mapa
        """
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = pos
        shape = pymunk.Circle(body, radius)
        shape.elasticity = self.STATIC_BALL_ELASTICY
        shape.friction = self.STATIC_BALL_FRICTION
        shape.color = self.STATIC_BALL_COLOR
        self.space.add(body, shape)

    @abstractmethod
    def create_elements(self):
        """
        Funcao que desenha todos os elementos do mapa,  que e chamada no comeco do jogo
        """
        pass

    @abstractmethod
    def flippers_position(self):
        """
        Função que retorna a posicao que deve ficar os flippers
        """
        pass

    @abstractmethod
    def ball_creation_position(self):
        """
        Posicao que a bola sera criada no jogo
        """
        pass


class MainMap(AbstractMap):
    """
    Mapa principal do jogo pinball
    """

    def create_elements(self):
        # Vou usar o conceito de GRID para posicionar os elementos na tela.
        self.col, self.row = 5, 5
        # Dividindo a largura da tela pela quantidade de colunas
        self.col_width = self.screen_width // self.col
        # Dividindo a altura da tela pela quantidade de linhas
        self.row_height = self.screen_height // self.row

        self.margin_bottom = 60

        self.draw_funnel()
        self.draw_borders()
        self.draw_ball_path()
        self.draw_polys()
        self.draw_balls()
        
    def draw_polys(self):
        """
        Funcao que desenha os buppers
        """
        self.create_buppers()

    def draw_balls(self):
        """
        Funcao para desenhar os elementos em formato de bola
        """
        radius = 60
        ball_x = self.col_width * (self.col / 2)
        ball_y = self.row_height * 1
        pos = (ball_x, ball_y)
        self.create_a_static_ball(pos, radius)

    def draw_launcher(self):
        """
        Desenhar o lanchador
        """
        pass

    def create_buppers(self):
        """
        Criar os dois bampers, right e left
        """
        # bumper width e bumper height
        width, height = 80, 80
        offset = width // 2

        vertices_left_bumper = [(0, width), (width, 0), (width, height), (0, height)]
        vertices_right_bumper = [(0, 0), (width, width), (width, height), (0, height)]

        # right bumper
        right_bumper_x = self.col_width * 1 + offset
        right_bumper_y = self.row_height * 4 - (height + offset)

        position_right_bumper = (right_bumper_x, right_bumper_y)

        # left bumper
        left_bumper_x = self.col_width * 4 - (width + offset)
        left_bumper_y = right_bumper_y  # os dois tem a mesma altura

        position_left_bumper = (left_bumper_x, left_bumper_y)

        # right bumper
        self.create_static_poly(vertices_right_bumper, position_right_bumper)
        # left bumper
        self.create_static_poly(vertices_left_bumper, position_left_bumper)

    def draw_funnel(self):
        """
        Funcao para desenhar funil que leva ate os flippers
        """
        # Inclinação do segemento que leva a bolinha até o meio
        incli = 40

        # Agora para colocar o elementos na coluna basta multiplicar col_witdh * Numero da coluna
        # Mesma coisa com a linha

        # Segmento pocisionando na primeira coluna até a penultima linha
        lateral_left = (self.col_width * 0.8 - incli, self.row_height * 2), (
            self.col_width * 1,
            self.row_height * 4,
        )
        # Segmento pocisionado na ultima coluna ate a penultina linha
        lateral_right = (self.col_width * 4.2 + incli, self.row_height * 2), (
            self.col_width * 4,
            self.row_height * 4,
        )

        funil_left = (self.col_width * 1, self.row_height * 4), (
            self.col_width * 2,
            self.row_height * 5 - self.margin_bottom,
        )

        funil_right = (self.col_width * 4, self.row_height * 4), (
            self.col_width * 3,
            self.row_height * 5 - self.margin_bottom,
        )

        # Adicionando a lista de para desenhar
        self.platforms.append(lateral_left)
        self.platforms.append(lateral_right)
        self.platforms.append(funil_left)
        self.platforms.append(funil_right)

        # Definindo a posicao dos flippers
        self.flippers = (
            self.col_width * 2,
            self.row_height * 5 - self.margin_bottom,
        ), (
            self.col_width * 3,
            self.row_height * 5 - self.margin_bottom,
        )

    def draw_borders(self):
        """
        Desenha bordas entorno da tela
        """
        margin_right = self.col_width * 0.3

        top_border = (0, 0), (self.screen_width, 0)
        right_border = (self.screen_width, 0), (self.screen_width, self.screen_height)
        left_border = (0, 0), (0, self.row_height * 2)
        bottom_border = (
            self.screen_width - margin_right,
            self.screen_height,
        ), (self.screen_width, self.screen_height)

        lateral_double_left = (0, self.row_height * 2), (
            self.col_width * 0.5,
            self.row_height * 4,
        )

        funil_double_left = (self.col_width * 0.5, self.row_height * 4), (
            self.col_width * 1.5,
            self.row_height * 5,
        )

        lateral_double_right = (
            self.screen_width - margin_right,
            self.row_height * 1.5,
        ), (self.screen_width - margin_right, self.screen_height)

        funil_double_right = (
            self.screen_width - margin_right,
            self.row_height * 4,
        ), (
            self.screen_width - self.col_width * 1.5,
            self.row_height * 5,
        )

        self.platforms.append(top_border)
        self.platforms.append(left_border)
        self.platforms.append(right_border)
        self.platforms.append(bottom_border)
        self.platforms.append(lateral_double_left)
        self.platforms.append(funil_double_left)
        self.platforms.append(lateral_double_right)
        self.platforms.append(funil_double_right)

    def draw_ball_path(self):
        """
        Caminha da bola para o centro
        """
        redirect = (self.col_width * 4,0),(self.screen_width, self.row_height * 1)

        self.platforms.append(redirect)

    @property
    def flippers_position(self):
        return self.flippers

    @property
    def ball_creation_position(self):
        return (
            self.screen_width - self.col_width * 0.15,
            self.row_height * 4,
        )
