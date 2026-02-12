import pygame, sys
from settings import *
from player import *

# ----start class---
class Game :
    def __init__(self):
        pygame.init()
        # create window
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Western Shoter')
        self.clock = pygame.time.Clock()
        self.all_sprites = pygame.sprite.Group()
        self.setup()

    def setup(self):
        Player((200, 200), self.all_sprites, PATHS['player'],None)

    def run(self):
        while True:
            # Event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            #Delta time
            dt = self.clock.tick()/1000

            # update
            self.all_sprites.update(dt)

            self.display_surface.fill('black')
            self.all_sprites.draw(self.display_surface)

            pygame.display.update()

if __name__ == '__main__':
    game = Game()
    game.run()