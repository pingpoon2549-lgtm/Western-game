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
        self.all_sprites = AllSprites()
        self.setup()

    def setup(self):
        self.player = Player((200, 200), self.all_sprites, PATHS['player'],None)

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
            self.all_sprites.customize_draw(self.player)
            #self.all_sprites.draw(self.display_surface)

            pygame.display.update()

class AllSprites(pygame.sprite.Group) :
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = vector()

        self.bg = pygame.image.load('../graphics/other/bg.png').convert()

    def customize_draw(self, player):
        self.offset.x = player.rect.centerx - WINDOW_WIDTH/2
        self.offset.y = player.rect.centery - WINDOW_HEIGHT/2
        # -- วาดพื้นหลัง --
        self.display_surface.blit(self.bg, -self.offset)
        # -- วาด Sprite ทุกตัว --
        for sprite in self.sprites():
            offset_rect = sprite.image.get_rect(center = sprite.rect.center)
            offset_rect.center -= self.offset
            self.display_surface.blit(sprite.image, offset_rect)


if __name__ == '__main__':
    game = Game()
    game.run()