"""
Classes para criação de mapas do pinball
"""
import pymunk
import pygame as pg

class MainMap:

    COL, ROW = 5,5
    MARGIN = 60
    MARGIN_BOTTOM = 150
    thickness = 5

    def __init__(self,WIN_SIZE,space):
        self.space = space
        self.WIDHT = WIN_SIZE[0]
        self.HEIGHT = WIN_SIZE[1]

        self.platforms = []
        
    def draw_map(self):
        self.segments_points()
        for plataform in self.platforms:
            self.create_segment(*plataform)
    
    def segments_points(self):
        """
        Função para calcular as coordenadas dos segmentos

        Pontonicial: x,y, ponto final: x,y
        """
        self.floor = (0,self.WIDHT),(self.WIDHT,self.HEIGHT)
        self.lateral_left = (self.MARGIN,self.HEIGHT//4),(self.MARGIN,self.HEIGHT - self.MARGIN_BOTTOM)
        
        self.lateral_right =(self.WIDHT - self.MARGIN,self.HEIGHT//4),(self.WIDHT - self.MARGIN,self.HEIGHT - self.MARGIN_BOTTOM)
       
       
        self.funil_left = (self.MARGIN,self.HEIGHT - self.MARGIN_BOTTOM),(self.WIDHT//4,self.HEIGHT - self.MARGIN)
        self.funil_right = (self.WIDHT - self.MARGIN,self.HEIGHT - self.MARGIN_BOTTOM),(self.WIDHT - self.WIDHT//4,self.HEIGHT - self.MARGIN)
        self.platforms.append(self.floor)
        self.platforms.append(self.lateral_left)
        self.platforms.append(self.lateral_right)
        self.platforms.append(self.funil_left)
        self.platforms.append(self.funil_right)

    def create_segment(self,from_,to_):
        """
        Função para criar um segmento
        Parâmentros: posição do começo, mais posição do final
        """
        # posição
        segment_shape = pymunk.Segment(self.space.static_body,from_,to_,self.thickness)
        # Propriedades do segmento
        segment_shape.color = pg.Color('black')
        segment_shape.friction = 0.2
        segment_shape.elasticity = 0.4
        self.space.add(segment_shape)