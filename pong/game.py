import json
from pygame.math import Vector2

import pong
import pong.entities
import pong.common


class Player(pong.entities.Paddle):
    def __init__(self, playerNum):
        super().__init__(None)
        self.score = 0
        self.number = playerNum
        self.reset_location()

    def reset_location(self):
        if self.world is None:
            return
        new_y = (self.world.HEIGHT - self.HEIGHT) / 2
        new_x = -1
        if self.number in (pong.constants.PLAYER1, pong.constants.PLAYER_LEFT):
            new_x = pong.constants.PLAYER_MARGIN    # Left side
        elif self.number in (pong.constants.PLAYER2, pong.constants.PLAYER_RIGHT):
            new_x = self.world.WIDTH - pong.constants.PLAYER_MARGIN - self.WIDTH    # Right side
        self.location = Vector2(new_x, new_y)

    def __repr__(self):
        return 'Player{this.number} :: score={this.score}; location={this.location}'.format(this=self)


class Pong(pong.entities.World):

    def __init__(self):
        super().__init__()

        self.player1 = Player(pong.constants.PLAYER1)
        self.player2 = Player(pong.constants.PLAYER2)
        self.ball = pong.entities.Ball()

        self.player1.world = self
        self.player2.world = self
        self.ball.world = self

        self.player1.reset_location()
        self.player2.reset_location()
        self.ball.reset()

        self.add(self.player1, self.player2, self.ball)

        self.ball.heading = Vector2(1, 1).normalize()

    def ball_out(self):
        ball_center = Vector2(self.ball.get_rect().center)
        if ball_center.x < self.WIDTH / 2:
            return self.player1
        else:
            return self.player2

    def handle_scores(self):
        if not self.ball.alive():
            if self.ball_out() is self.player1:
                self.player2.score += 1
            else:
                self.player1.score += 1
            self.ball.reset()

    def update(self, passSecond):
        super().update(passSecond)
        self.handle_scores()

    def locations_json(self):
        return json.dumps(self, default=pong.common.toJson, separators=(',', ':'))

    def update_with_json(self, jsonPong):

        p = json.loads(jsonPong, object_hook=pong.common.fromJson)
        assert isinstance(p, Pong)
        self.player1.location = p.player1.location
        self.player1.score = p.player1.score
        self.player1.WIDTH = p.player1.WIDTH
        self.player1.HEIGHT = p.player1.HEIGHT

        self.player2.location = p.player2.location
        self.player2.score = p.player2.score
        self.player2.WIDTH = p.player2.WIDTH
        self.player2.HEIGHT = p.player2.HEIGHT

        self.ball.location = p.ball.location

