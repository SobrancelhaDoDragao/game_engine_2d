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

    thickness = 5
    segment_color = pg.Color("black")
    segment_friction = 1.0
    segment_elasticity = 0.5

    def __init__(self, win_size, space):
        self.space = space
        self.width = win_size[0]
        self.height = win_size[1]

        self.platforms = []
        self.segments_points()

    def draw_map(self):
        for plataform in self.platforms:
            self.create_segment(*plataform)

    def create_segment(self, from_, to_):
        """
        Função para criar um segmento
        Parâmentros: posição do começo, mais posição do final
        """
        # posição
        segment_shape = pymunk.Segment(
            self.space.static_body, from_, to_, self.thickness
        )
        # Propriedades do segmento
        segment_shape.color = self.segment_color
        segment_shape.friction = self.segment_friction
        segment_shape.elasticity = self.segment_elasticity
        self.space.add(segment_shape)

    @abstractmethod
    def segments_points(self):
        """
        Função para calcular as coordenadas dos segmentos: ponto inicial: x,y, ponto final: x,y
        """
        pass

    @abstractmethod
    def flippers_position(self):
        """
        Função que retorna a posicao que deve ficar os flippers
        """
        pass


class MainMap(AbstractMap):
    """
    Mapa principal do jogo pinball
    """

    def segments_points(self):
        # Vou usar o conceito de GRID para posicionar os elementos na tela.
        col, row = 5, 5
        # Dividindo a largura da tela pela quantidade de colunas
        col_width = self.width // col
        # Dividindo a altura da tela pela quantidade de linhas
        row_height = self.height // row

        margin_bottom = 60

        self.draw_funnel(col_width, row_height, margin_bottom)
        self.draw_borders(col_width, row_height)

    def draw_funnel(self, col_width, row_height, margin_bottom):
        """
        Funcao para desenhar funil que leva ate os flippers
        """
        # Inclinação do segemento que leva a bolinha até o meio
        incli = 40

        # Agora para colocar o elementos na coluna basta multiplicar COL_WIDTH * Numero da coluna
        # Mesma coisa com a linha

        # Segmento pocisionando na primeira coluna até a penultima linha
        lateral_left = (col_width * 0.8 - incli, row_height * 2), (
            col_width * 1,
            row_height * 4,
        )
        # Segmento pocisionado na ultima coluna ate a penultina linha
        lateral_right = (col_width * 4.2 + incli, row_height * 2), (
            col_width * 4,
            row_height * 4,
        )

        funil_left = (col_width * 1, row_height * 4), (
            col_width * 2,
            row_height * 5 - margin_bottom,
        )

        funil_right = (col_width * 4, row_height * 4), (
            col_width * 3,
            row_height * 5 - margin_bottom,
        )

        # Adicionando a lista de para desenhar
        self.platforms.append(lateral_left)
        self.platforms.append(lateral_right)
        self.platforms.append(funil_left)
        self.platforms.append(funil_right)

        # Definindo a posicao dos flippers
        self.flippers = (col_width * 2, row_height * 5 - margin_bottom), (
            col_width * 3,
            row_height * 5 - margin_bottom,
        )

    def draw_borders(self, col_width, row_height):
        """
        Desenha bordas entorno da tela
        """
        top_border = (0, 0), (self.width, 0)
        right_border = (self.width, 0), (self.width, row_height * 2)
        left_border = (0, 0), (0, row_height * 2)

        lateral_double_left = (0, row_height * 2), (col_width * 0.5, row_height * 4)
        funil_double_left = (col_width * 0.5, row_height * 4), (
            col_width * 1.5,
            row_height * 5,
        )

        lateral_double_right = (self.width, row_height * 2), (
            self.width - col_width * 0.5,
            row_height * 4,
        )
        funil_double_right = (self.width - col_width * 0.5, row_height * 4), (
            self.width - col_width * 1.5,
            row_height * 5,
        )

        self.platforms.append(top_border)
        self.platforms.append(left_border)
        self.platforms.append(right_border)
        self.platforms.append(lateral_double_left)
        self.platforms.append(funil_double_left)
        self.platforms.append(lateral_double_right)
        self.platforms.append(funil_double_right)

    @property
    def flippers_position(self):
        return self.flippers
