import pymunk.pygame_util
from pymunk import Vec2d

from map import MainMap


class PysicsEngine2D:
    """
    Classe criada para gerenciar a fisica do jogo
    """

    BALL_MASS = 2
    BALL_RADIUS = 10
    BALL_ELASTICITY = 0.9
    BALL_FRICTION = 1
    GRAVITY = 0, 800
    SEGMENT_THICKNESS = 4

    def __init__(self, game):
        self.screen = game.screen
        pymunk.pygame_util.positive_y_is_up = False
        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)
        self.space = pymunk.Space()
        self.space.gravity = self.GRAVITY
        self.fps = game.FPS
        self.map = MainMap(game.WIN_SIZE, self.space)
        self.map.draw_map()
        self.create_flipper()
        self.create_flipper_left()

    def update(self):
        self.space.step(1 / self.fps)
        self.space.debug_draw(self.draw_options)

    def new_ball(self, pos):
        ball_moment = pymunk.moment_for_circle(self.BALL_MASS, 0, self.BALL_RADIUS)
        ball_body = pymunk.Body(self.BALL_MASS, ball_moment)
        ball_body.position = pos
        ball_shape = pymunk.Circle(ball_body, self.BALL_RADIUS)
        ball_shape.elasticity = self.BALL_ELASTICITY
        ball_shape.friction = self.BALL_FRICTION
        self.space.add(ball_body, ball_shape)

    def create_flipper(self):
        pos = (
            self.map.flippers_position[1][0] - 20,
            self.map.flippers_position[1][1] + 5,
        )

        fp = [(10, -10), (-50, 0), (10, 10)]
        mass = 1000
        moment = pymunk.moment_for_poly(mass, fp)

        # right flipper
        r_flipper_body = pymunk.Body(mass, moment)
        r_flipper_body.position = pos
        r_flipper_body.elasticity = 5
        r_flipper_body.friction = 1
        r_flipper_body.density = 1
        r_flipper_body.group = 1
        r_flipper_shape = pymunk.Poly(r_flipper_body, fp)
        self.space.add(r_flipper_body, r_flipper_shape)

        r_flipper_joint_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        r_flipper_joint_body.position = pos
        j = pymunk.PinJoint(r_flipper_body, r_flipper_joint_body, (0, 0))
        s = pymunk.DampedRotarySpring(
            r_flipper_body, r_flipper_joint_body, 0.10, 20000000, 900000
        )
        self.space.add(j, s)

        self.r_flipper_body = r_flipper_body

    def create_flipper_left(self):
        pos = (
            self.map.flippers_position[0][0] + 20,
            self.map.flippers_position[0][1] + 5,
        )

        fp = [(10, -10), (-50, 0), (10, 10)]

        mass = 1000
        moment = pymunk.moment_for_poly(mass, fp)

        l_flipper_body = pymunk.Body(mass, moment)
        l_flipper_body.position = pos
        l_flipper_body.elasticity = 5
        l_flipper_body.friction = 1
        l_flipper_body.density = 1
        l_flipper_body.group = 1
        l_flipper_shape = pymunk.Poly(l_flipper_body, [(-x, y) for x, y in fp])
        self.space.add(l_flipper_body, l_flipper_shape)

        l_flipper_joint_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        l_flipper_joint_body.position = pos
        j = pymunk.PinJoint(l_flipper_body, l_flipper_joint_body, (0, 0), (0, 0))
        s = pymunk.DampedRotarySpring(
            l_flipper_body, l_flipper_joint_body, -0.10, 20000000, 900000
        )
        self.space.add(j, s)

        self.l_flipper_body = l_flipper_body

    def botao(self):
        self.r_flipper_body.apply_impulse_at_local_point(
            Vec2d.unit() * -50000, (-150, 0)
        )

    def botaoleft(self):
        self.l_flipper_body.apply_impulse_at_local_point(
            Vec2d.unit() * 50000, (-150, 0)
        )
