from pygame.math import Vector2
import json
import copy
import pygame.math
import pong

BUFFER_SIZE = 4096

class ClientCommand:
    def __init__(self, fromDict=None):
        self.move_up = False
        self.move_down = False
        self.action = False

        if fromDict is not None and isinstance(fromDict, dict):
            self.update_fromDict(fromDict)
            return

    def clone(self):
        return copy.copy(self)

    def update_fromDict(self, d):
        if not isinstance(d, dict):
            raise
        for k, v in d.items():
            if k in self.__dict__.keys():
                self.__dict__[k] = v

    def json(self):
        return json.dumps(self, default=pong.common.toJson)

    def heading(self):
        dy = 0
        if self.move_up:
            dy = -1
        elif self.move_down:
            dy = +1
        return Vector2(0, dy)

def toJson(obj):

    objClass = type(obj).__name__

    if isinstance(obj, pong.common.ClientCommand):
        return {'__class__': objClass,
                '__value__': obj.__dict__}

    if isinstance(obj, (pygame.math.Vector2, pygame.Rect)):
        return {'__class__': objClass,
                '__value__': [*obj,]}   

    if isinstance(obj, pong.game.Player):
        return {'__class__': objClass,
                'number': obj.number,
                'score': obj.score,
                'rect': obj.get_rect()}

    if isinstance(obj, pong.entities.GameEntity):
        return {'__class__': objClass,
                '__value__': obj.get_rect()}

    if isinstance(obj, pong.game.Pong):
        return {'__class__': objClass,
                'player1': obj.player1,
                'player2': obj.player2,
                'ball': obj.ball,
                'state': None}

    raise 


def fromJson(jsonObj):

    if '__class__' in jsonObj:
        _class = jsonObj['__class__']

        if _class == 'ClientCommand':
            return pong.common.ClientCommand(fromDict=jsonObj['__value__'])

        if _class == 'Vector2':
            return pygame.math.Vector2(jsonObj['__value__'])  

        if _class == 'Rect':
            return pygame.Rect(jsonObj['__value__'])

        if _class == 'Ball':
            x, y, w, h = (*jsonObj['__value__'],)
            ball = pong.entities.Ball((x, y))
            ball.WIDTH, ball.HEIGHT = w, h
            return ball

        if _class == 'Player':
            x, y, w, h = (*jsonObj['rect'],)
            player = pong.game.Player(jsonObj['number'])
            player.location = pygame.math.Vector2(x, y)
            player.WIDTH = w
            player.HEIGHT = h
            player.score = jsonObj['score']
            return player

        if _class == 'Pong':
            pongWorld = pong.game.Pong()
            pongWorld.player1 = jsonObj['player1']
            pongWorld.player2 = jsonObj['player2']
            pongWorld.ball = jsonObj['ball']
            pongWorld.state = jsonObj['state']  
            return pongWorld
    return jsonObj
