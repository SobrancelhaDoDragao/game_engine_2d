"""
Classes para criação de mapas do pinball
"""
from base import AbstractMap


class MainMap(AbstractMap):
    """
    Mapa principal do jogo pinball
    """

    def __init__(self, win_size, space):
        # Extedendo a classe pai
        super().__init__(win_size, space)
        # Vou usar o conceito de GRID para posicionar os elementos na tela.
        self.col, self.row = 5, 5
        # Dividindo a largura da tela pela quantidade de colunas
        self.col_width = self.screen_width // self.col
        # Dividindo a altura da tela pela quantidade de linhas
        self.row_height = self.screen_height // self.row

        self.margin_bottom = 60

    def create_segments(self):
        self.draw_funnel()
        self.draw_borders()
        # self.draw_ball_path()

    def create_polys(self):
        """
        Metodo que deve criar todos os poligonos e adicionar na self.polys
        """
        self.create_buppers()
        self.create_bumper_lauch()

    def create_balls(self):
        """
        Metodo que deve criar todas as bolas e adicionar no self.balls
        """
        self.draw_balls()

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
        self.segments.append(lateral_left)
        self.segments.append(lateral_right)
        self.segments.append(funil_left)
        self.segments.append(funil_right)

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

        self.segments.append(top_border)
        self.segments.append(left_border)
        self.segments.append(right_border)
        self.segments.append(bottom_border)
        self.segments.append(lateral_double_left)
        self.segments.append(funil_double_left)
        self.segments.append(lateral_double_right)
        self.segments.append(funil_double_right)

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

        # bumper right
        bumper_right = (vertices_right_bumper, position_right_bumper)
        # left bumper
        bumper_left = (vertices_left_bumper, position_left_bumper)

        self.polys.append(bumper_right)
        self.polys.append(bumper_left)

    def create_bumper_lauch(self):
        """
        Criando um bumper para desviar a bola
        """
        # bumper width e bumper height
        width, height = 80, 80

        vertices_bumper = [(0, 0), (width, width), (width, height), (height, 0)]

        # right bumper
        bumper_x = self.screen_width - width
        bumper_y = 0

        position_bumper = (bumper_x, bumper_y)

        bumper = (vertices_bumper, position_bumper)

        self.polys.append(bumper)

    def draw_balls(self):
        """
        Funcao para desenhar os elementos em formato de bola
        """
        radius = 60
        ball_x = self.col_width * (self.col / 2)
        ball_y = self.row_height * 1
        pos = (ball_x, ball_y)

        ball = (radius, pos)

        self.balls.append(ball)

    def draw_ball_path(self):
        """
        Caminha da bola para o centro
        """
        redirect = (self.col_width * 4, 0), (self.screen_width, self.row_height * 1)
        redirect_line2 = (self.col_width * 3.5, self.row_height * 0.5), (
            self.col_width * 4.7,
            self.row_height * 1.5,
        )
        self.segments.append(redirect)
        self.segments.append(redirect_line2)

    @property
    def flippers_position(self):
        # Definindo a posicao dos flippers
        self.flippers = (
            self.col_width * 2,
            self.row_height * 5 - self.margin_bottom,
        ), (
            self.col_width * 3,
            self.row_height * 5 - self.margin_bottom,
        )
        return self.flippers

    @property
    def ball_creation_position(self):
        return (
            self.screen_width - self.col_width * 0.15,
            self.row_height * 4,
        )
