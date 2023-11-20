from pygame.locals import *
import pygame

import random

import pongserver.server
import pongclient.client
import pong
import pong.entities


"""Pong GUI client"""





address = input('서버주소를 입력해주세요 Server address (host:port) = ')
host, port = address.split(':')
port = int(port)

SERVER_ADDRESS = (host, port)
DISPLAY_SIZE = (pong.entities.World.WIDTH, pong.entities.World.HEIGHT)

FPS = 60


def main():
    pong_world = pong.game.Pong()
    client_command = pong.common.ClientCommand()

    
    local_address = ('localhost', random.randint(10000, 20000))

    svh = client.client.ServerHandler(local_address,
                                          SERVER_ADDRESS,
                                          pong_world,
                                          client_command,)
    svh.start()

    display = pygame.display.set_mode(DISPLAY_SIZE)
    pygame.display.set_caption('Pong GUI Client')
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return

            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    client_command.move_up = True
                elif event.key == K_DOWN:
                    client_command.move_down = True
                elif event.key == K_SPACE:
                    client_command.action = True

            elif event.type == KEYUP:
                if event.key == K_UP:
                    client_command.move_up = False
                elif event.key == K_DOWN:
                    client_command.move_down = False
                elif event.key == K_SPACE:
                    client_command.action = False


     
        display.fill(pygame.Color('black'))
        for entity in pong_world.sprites():
            display.blit(entity.image, entity.location)
           

        pygame.display.update()
        clock.tick(60)

    return


def handle_event(event):
    return


def draw_graphics():
    return


if __name__ == '__main__':
    main()
