import pymunk.pygame_util
from pymunk import Vec2d

from map import MainMap


class PysicsEngine2D:
    """
    Classe criada para gerenciar a fisica do jogo
    """

    BALL_MASS = 2
    BALL_RADIUS = 10
    BALL_ELASTICITY = 1
    BALL_FRICTION = 0.4
    GRAVITY = 0, 800
    SEGMENT_THICKNESS = 4
    FLIPPER_POLYGON_RIGHT = [(10, -10), (-50, 0), (10, 10)]
    # Invertendo os polygon do flipper right
    FLIPPER_POLYGON_LEFT = [(-x, y) for x, y in FLIPPER_POLYGON_RIGHT]

    def __init__(self, game):
        self.screen = game.screen
        pymunk.pygame_util.positive_y_is_up = False
        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)
        self.space = pymunk.Space()
        self.space.gravity = self.GRAVITY
        self.fps = game.FPS
        self.map = MainMap(game.WIN_SIZE, self.space)
        self.map.draw_map()
        self.draw_flippers()

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

    def create_flipper(self, pos, polygon):
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
        j = pymunk.PinJoint(flipper_body, flipper_joint_body, (0, 0))
        s = pymunk.DampedRotarySpring(
            flipper_body, flipper_joint_body, 0.10, 20000000, 900000
        )
        self.space.add(j, s)

        return flipper_body

    def draw_flippers(self):
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

    def on_press_right_arrow(self):
        self.r_flipper_body.apply_impulse_at_local_point(
            Vec2d.unit() * -50000, (-150, 0)
        )

    def on_press_left_arrow(self):
        self.l_flipper_body.apply_impulse_at_local_point(
            Vec2d.unit() * 50000, (-150, 0)
        )
