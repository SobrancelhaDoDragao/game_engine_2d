"""
Classes para criação de mapas do pinball
"""
import pymunk
import pygame as pg
from abc import ABC, abstractmethod

class AbstractMap(ABC):
    """
    Classe abstrada para criação de mapas
    """
    thickness = 5
    segment_color = pg.Color('black')
    segment_friction = 1.0
    segment_elasticity = 0.5

    def __init__(self,WIN_SIZE,space):
        self.space = space
        self.WIDHT = WIN_SIZE[0]
        self.HEIGHT = WIN_SIZE[1]

        self.platforms = []
        self.segments_points()

        
    def draw_map(self):
        for plataform in self.platforms:
            self.create_segment(*plataform)
    
    def create_segment(self,from_,to_):
        """
        Função para criar um segmento
        Parâmentros: posição do começo, mais posição do final
        """
        # posição
        segment_shape = pymunk.Segment(self.space.static_body,from_,to_,self.thickness)
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
        COL, ROW = 5,5
        # Dividindo a largura da tela pela quantidade de colunas
        COL_WIDTH = self.WIDHT// COL
        # Dividindo a altura da tela pela quantidade de linhas
        ROW_HEIGHT = self.HEIGHT// ROW
        
        MARGIN_BOTTOM = 40

        self.draw_funnel(COL_WIDTH,ROW_HEIGHT,MARGIN_BOTTOM)
        self.draw_borders(COL_WIDTH,ROW_HEIGHT,MARGIN_BOTTOM)
        
    def draw_funnel(self,COL_WIDTH,ROW_HEIGHT,MARGIN_BOTTOM):
        """
        Funcao para desenhar funil que leva ate os flippers
        """
        # Inclinação do segemento que leva a bolinha até o meio
        INCLI = 40

        # Agora para colocar o elementos na coluna basta multiplicar COL_WIDTH * Numero da coluna
        # Mesma coisa com a linha

        # Segmento pocisionando na primeira coluna até a penultima linha
        lateral_left = (COL_WIDTH*0.8 - INCLI,ROW_HEIGHT*2),(COL_WIDTH*1,ROW_HEIGHT*4)
        # Segmento pocisionado na ultima coluna ate a penultina linha
        lateral_right =(COL_WIDTH*4.2 + INCLI,ROW_HEIGHT*2),(COL_WIDTH*4,ROW_HEIGHT*4)

        funil_left = (COL_WIDTH*1,ROW_HEIGHT*4),(COL_WIDTH*2,ROW_HEIGHT*5 - MARGIN_BOTTOM)
        
        funil_right = (COL_WIDTH*4,ROW_HEIGHT*4),(COL_WIDTH*3,ROW_HEIGHT*5 - MARGIN_BOTTOM)

        # Adicionando a lista de para desenhar
        self.platforms.append(lateral_left)
        self.platforms.append(lateral_right)
        self.platforms.append(funil_left)
        self.platforms.append(funil_right)
        
        # Definindo a posicao dos flippers
        self.flippers = (COL_WIDTH*2,ROW_HEIGHT*5 - MARGIN_BOTTOM),(COL_WIDTH*3,ROW_HEIGHT*5 - MARGIN_BOTTOM)

    def draw_borders(self,COL_WIDTH,ROW_HEIGHT,MARGIN_BOTTOM):
        """
        Desenha bordas entorno da tela
        """
        top_border = (0,0),(self.WIDHT,0)
        left_border = (self.WIDHT,0),(self.WIDHT,self.HEIGHT)
        right_border = (0,0),(0,self.HEIGHT)

        self.platforms.append(top_border)
        self.platforms.append(left_border)
        self.platforms.append(right_border)

    @property
    def flippers_position(self):
        return self.flippers





    