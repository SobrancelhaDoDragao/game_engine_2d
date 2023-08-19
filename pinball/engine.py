import pymunk.pygame_util
from map import MainMap
from pymunk import Vec2d


class PysicsEngine2D:
    """
    Classe criada para gerenciar a fisica do jogo
    """

    BALL_MASS = 1
    BALL_RADIUS = 15
    BALL_COLOR = (170, 170, 170, 255)
    BALL_ELASTICITY = 1
    BALL_FRICTION = 0.4

    LAUNCHER_REST = 300  # Tamanho da bola quando esta sem peso
    LAUNCHER_STIFFNESS = 1000  # Resistencia da mola
    LAUNCHER_DAMPING = 20  # Nao entendi esse

    FLIPPER_POLYGON_RIGHT = [(10, -10), (-50, 0), (10, 10)]
    # Invertendo os polygon do flipper right
    FLIPPER_POLYGON_LEFT = [(-x, y) for x, y in FLIPPER_POLYGON_RIGHT]
    # Gravidade eixo x,y
    GRAVITY = 0, 800

    def __init__(self, game):
        self.screen = game.screen
        self.screen_width = game.WIDTH
        self.screen_height = game.HEIGHT
        pymunk.pygame_util.positive_y_is_up = False
        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)
        self.space = pymunk.Space()
        self.space.gravity = self.GRAVITY
        self.fps = game.FPS
        self.map = MainMap(game.WIN_SIZE, self.space)
        self.map.draw_map()
        self.draw_flippers()
        self.create_launcher()
        self.ball = None

    def update(self):
        """
        Metodo que atualiza a fisica
        """
        self.space.step(1 / self.fps)
        self.space.debug_draw(self.draw_options)
        if self.is_ball_already_created():
            if self.is_ball_out_of_screen():
                # TODO preciso remover a bola do espaco
                self.ball = None

    def new_ball(self):
        """
        Metodo que cria um nova bola
        """
        if not self.is_ball_already_created():
            ball_moment = pymunk.moment_for_circle(self.BALL_MASS, 0, self.BALL_RADIUS)
            ball_body = pymunk.Body(self.BALL_MASS, ball_moment)
            ball_body.position = (
                self.map.ball_creation_position[0],
                self.map.ball_creation_position[1] - 300,
            )
            ball_shape = pymunk.Circle(ball_body, self.BALL_RADIUS)
            ball_shape.color = self.BALL_COLOR
            ball_shape.elasticity = self.BALL_ELASTICITY
            ball_shape.friction = self.BALL_FRICTION
            self.space.add(ball_body, ball_shape)

            self.ball = ball_body

    def is_ball_already_created(self):
        """
        Verifica se ja existe uma bola
        """
        return self.ball is not None

    def load_ball(self):
        """
        Metodo para lancar a bola
        """
        self.launcher.stiffness = self.launcher.stiffness / 2

    def throw_ball(self):
        """
        Funcao para arremessar a bola
        """
        self.launcher.stiffness = self.LAUNCHER_STIFFNESS

    def create_flipper(self, pos, polygon):
        """
        Metodo que cria um flipper
        """
        mass = 1000
        moment = pymunk.moment_for_poly(mass, polygon)

        flipper_body = pymunk.Body(mass, moment)
        flipper_body.position = pos
        flipper_shape = pymunk.Poly(flipper_body, polygon)
        flipper_shape.elasticity = 0.4
        flipper_shape.friction = 1
        flipper_shape.group = 1

        self.space.add(flipper_body, flipper_shape)

        flipper_joint_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        flipper_joint_body.position = pos

        joint = pymunk.PinJoint(flipper_body, flipper_joint_body, (0, 0))

        rotary_spring = pymunk.DampedRotarySpring(
            flipper_body, flipper_joint_body, 0.10, 20000000, 900000
        )

        self.space.add(joint, rotary_spring)

        return flipper_body

    def draw_flippers(self):
        """
        Metodo que desenha os flipers
        """
        # pos x,y dos flippers
        pos = (
            self.map.flippers_position[1][0] - 20,
            self.map.flippers_position[1][1] + 5,
        )

        pos2 = (
            self.map.flippers_position[0][0] + 20,
            self.map.flippers_position[0][1] + 5,
        )

        self.r_flipper_body = self.create_flipper(pos, self.FLIPPER_POLYGON_RIGHT)
        self.l_flipper_body = self.create_flipper(pos2, self.FLIPPER_POLYGON_LEFT)

    def create_launcher(self):
        """
        Criando lancador da bola
        """
        launcher_position = (
            self.map.ball_creation_position[0],
            self.map.ball_creation_position[1],
        )

        top_platform_mass = 10
        lower_platform_mass = 100

        width, height = 50, 10
        vertices = [
            (-width / 2, -height / 2),
            (width / 2, -height / 2),
            (width / 2, height / 2),
            (-width / 2, height / 2),
        ]

        moment_for_top_platform = pymunk.moment_for_poly(top_platform_mass, vertices)
        moment_for_lower_platform = pymunk.moment_for_poly(
            lower_platform_mass, vertices
        )

        body_top = pymunk.Body(top_platform_mass, moment_for_top_platform)
        body_lower = pymunk.Body(lower_platform_mass, moment_for_lower_platform)

        body_top.position = (launcher_position[0], launcher_position[1] - 250)
        body_lower.position = (launcher_position[0], launcher_position[1] + 100)

        shape_top = pymunk.Poly(body_top, vertices)
        shape_lower = pymunk.Poly(body_lower, vertices)

        shape_top.color = self.BALL_COLOR
        shape_lower.color = self.BALL_COLOR

        self.space.add(body_top, shape_top)
        self.space.add(body_lower, shape_lower)

        joint = pymunk.constraints.DampedSpring(
            body_top,
            body_lower,
            (0, 0),
            (0, 0),
            self.LAUNCHER_REST,
            self.LAUNCHER_STIFFNESS,
            self.LAUNCHER_DAMPING,
        )

        self.launcher = joint
        self.space.add(joint)

    def is_ball_out_of_screen(self):
        """
        Verificando se a bola saiu da tela
        """
        # TODO nao funciona corretamente. Demora para verificar se a bola saiu
        return (
            self.ball.position[0] > self.screen_width
            and self.ball.position[1] > self.screen_height
        )

    def limit_velocity(self):
        """
        Metodo para limitar a velocidade da bola, para evitar dela atravessar objetos
        """
        pass

    def on_press_right_arrow(self):
        """
        Controlando o flipper direito
        """
        self.r_flipper_body.apply_impulse_at_local_point(
            Vec2d.unit() * -50000, (-150, 0)
        )

    def on_press_left_arrow(self):
        """
        Controlando o fliper esquerdo
        """
        self.l_flipper_body.apply_impulse_at_local_point(
            Vec2d.unit() * 50000, (-150, 0)
        )
