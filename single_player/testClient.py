import pygame
import single_player.round_copy as myConns
from time import sleep
import socket
from single_player.network import Network

class TractorClient():

    def initGraphics(self):
        pass

    def __init__(self):

        pygame.init()
        width, height = 900,600

        # initialize the screen
        self.screen = pygame.display.set_mode((width, height))

        # initialize pygame clock
        self.clock=pygame.time.Clock()
        self.initGraphics()
        pygame.display.set_caption("Client -1")
        self.data = None
        self.card_indices = []
        self.rects = []
        self.test_rect = pygame.Surface((200, 200))
        self.test_rect.fill((255, 255, 255, 255))

    def draw_test(self):
        pass
        self.screen.blit(self.test_rect, [450 + 22 * (0), 445 - 0],area=self.test_rect.get_rect(), special_flags=0)
        # self.rects.append(pygame.draw.rect(self.screen, (255, 255, 255, 255), pygame.Rect(0,0,200,200)))
        # self.rects.append(pygame.draw.rect(self.screen, (255, 0, 0, 255), pygame.Rect(100,100,200,200)))

    def update(self):
        # make the game 60 fps
        self.clock.tick(60)

        # clear the screen
        self.screen.fill(0)

        # draws board over cleared screen
        self.draw_test()

        # take input
        click = None
        for event in pygame.event.get():
            # quit if the quit button was pressed
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                click = event.pos
                print(self.test_rect.get_rect().move(200, 200).collidepoint(click))
                print(self.test_rect.get_rect().collidepoint(click))
                # print(self.rects[0].collidepoint(click))
                # print(self.rects[1].collidepoint(click))
                print(click)

        # update the screen
        pygame.display.flip()

while 1:
    myClient = TractorClient()
    myClient.update()