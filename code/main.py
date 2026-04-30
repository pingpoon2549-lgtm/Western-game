import pygame, sys

from settings import *
from player import *
from pytmx.util_pygame import load_pygame
from sprite import *
from monster import Coffin, Cactus

# ----start class---
class Game :
    def __init__(self):
        pygame.init()
        # create window
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Western Shoter')

        self.clock = pygame.time.Clock()

        self.all_sprites = AllSprites()
        self.obstacles = pygame.sprite.Group()
        self.monsters = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.startpos = vector(0,0)

        self.bullet_surf = pygame.image.load('../graphics/other/particle.png')
        self.gameover = pygame.image.load('../graphics/GAME OVER.png').convert_alpha()

        self.setup()

    def create_bullet(self, pos, direction):
        print("create_bullet")
        Bullet(pos, direction, self.bullet_surf, [self.all_sprites, self.bullets])

    def setup(self):
        tmx_map = load_pygame('../data/map1.tmx')
        for x,y, surf in tmx_map.get_layer_by_name('Fence').tiles():
            Sprite((x * 64, y * 64), surf, [self.all_sprites, self.obstacles])
        for obj in tmx_map.get_layer_by_name('Object'):
            Sprite((obj.x, obj.y), obj.image, [self.all_sprites, self.obstacles])
        for obj in tmx_map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                #global startpos
                self.startpos = vector(obj.x, obj.y)
                self.player = Player((obj.x, obj.y), self.all_sprites, PATHS['player'], self.obstacles, create_bullet = self.create_bullet)
                self.player.health = 999
            if obj.name == 'Coffin':
                Coffin((obj.x, obj.y), [self.all_sprites, self.monsters], PATHS['coffin'],self.obstacles, self.player)
            if obj.name == 'Cactus':
                 Cactus((obj.x, obj.y), [self.all_sprites, self.monsters], PATHS['cactus'], self.obstacles, self.player, create_bullet = self.create_bullet)

    def bullet_collision(self):
        # print('bullet_collision')
        # ลบกระสุนทิ้ง
        for obstacle in self.obstacles.sprites():
            pygame.sprite.spritecollide(obstacle, self.bullets, True, pygame.sprite.collide_mask)
        # ลบกระสุน+ศัตรูเจ็บ
        for bullet in self.bullets.sprites():
            sprites = pygame.sprite.spritecollide(bullet, self.monsters, False, pygame.sprite.collide_mask)

            if sprites:
                bullet.kill()
                for sprite in sprites:
                    sprite.damage()

        if pygame.sprite.spritecollide(self.player, self.bullets, True, pygame.sprite.collide_mask):
            self.player.damage()

    def reset_game(self):
        self.player.pos = vector(self.startpos.x, self.startpos.y)
        self.player.dead = False
        self.player.health = 999


    def run(self):
        while True:
            # Event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN and self.player.dead:
                    if event.key == pygame.K_y:
                        self.reset_game()
                    elif event.key == pygame.K_n:
                        pygame.quit()
                        sys.exit()

            #Delta time
            dt = self.clock.tick()/1000

            #keys = pygame.key.get_pressed()
            #if self.health <= 0:
                #if keys[pygame.K_SPACE]:
                    #self.health = 3


            # update
            if not self.player.dead:
                self.all_sprites.update(dt)
                self.bullet_collision()

                self.display_surface.fill('black')
                self.all_sprites.customize_draw(self.player)

            #if self.player.dead:
            else :
                gameover_rect = self.gameover.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
                self.display_surface.blit(self.gameover, gameover_rect)
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
        #for sprite in self.sprites():
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_rect = sprite.image.get_rect(center = sprite.rect.center)
            offset_rect.center -= self.offset
            self.display_surface.blit(sprite.image, offset_rect)


if __name__ == '__main__':
    game = Game()
    game.run()