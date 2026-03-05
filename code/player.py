from unittest import case

import pygame
from pygame.math import Vector2 as vector
from os import walk

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, path, collision_sprites, create_bullet):
        super().__init__(groups)
        # -- image&rect--
        self.image = pygame.Surface((100, 100))
        self.image.fill('red')
        self.rect = self.image.get_rect(center = pos)
        # -- movement attributes--
        self.pos = vector(self.rect.center)
        self.direction = vector()
        self.speed = 200
        # -- collision(การชน) ---
        #self.hitbox = self.rect.inflate(0, -self.rect.height/2)
        self.hitbox = self.rect.inflate(-self.rect.width * 0.5, -self.rect.height / 2)
        self.collision_sprites = collision_sprites
        self.imports_assets(path)
        self.status = 'down'
        self.frame_index = 0
        self.attacking = False
        self.create_bullet = create_bullet

    def imports_assets(self, path):
        self.animations = {}
        # os.walk
        for index, folder in enumerate(walk(path)):
            if index == 0:
                for name in folder[1]:
                    self.animations[name] = []
            else:
                for file_name in sorted(folder[2], key = lambda string: int(string.split('.')[0])):
                    path = folder[0].replace('\\','/') + '/' + file_name
                    # --โหลดรูปภาพ ---
                    surf = pygame.image.load(path).convert_alpha()
                    # --- หาชื่อ Key จากชื่อโฟลเดอร์ ----
                    key = folder[0].split('/')[3]
                    # --- เก็บใส่ Dictionary ---
                    self.animations[key].append(surf)
                    #print(path)

    def animate(self,dt):
        current_animation = self.animations[self.status]
        self.frame_index += 7 * dt
        if self.frame_index >= len(current_animation):
            self.frame_index = 0
            if self.attacking:
                self.attacking = False
        self.image = current_animation[int(self.frame_index)]

        # -- ยิงกระสุนเฟรมที่ 2 ---
        if int(self.frame_index) == 2 and self.attacking and not self.bullet_shot:
            bullet_start_pos = self.rect.center + self.bullet_direction * 80

            self.create_bullet(bullet_start_pos, self.bullet_direction)
            self.bullet_shot = True

    def input(self):
        keys = pygame.key.get_pressed()

        if not self.attacking:
            if keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = 'right'
            elif keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = 'left'
            else :
                self.direction.x = 0

            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0

            if keys[pygame.K_SPACE]:
                self.attacking = True
                self.direction = vector()
                self.frame_index = 0
                self.bullet_shot = False

                # --กำหนดทิศทางกระสุน--
                match self.status.split('_')[0]:
                    case 'left' : self.bullet_direction = vector(-1,0)
                    case 'right' : self.bullet_direction = vector(1,0)
                    case 'up' : self.bullet_direction = vector(0,-1)
                    case 'down' : self.bullet_direction = vector(0,1)


    def get_status(self):
        if self.direction.x == 0 and self.direction.y == 0:
            self.status = self.status.split('_')[0] + '_idle'
        if self.attacking:
            self.status = self.status.split('_')[0] + '_attack'

    def move(self, dt):
        if self.direction.magnitude()!=0:
            self.direction = self.direction.normalize()
        # ---Hori
        self.pos.x += self.direction.x * self.speed * dt
        self.hitbox.centerx = round(self.pos.x)
        self.rect.centerx = self.hitbox.centerx
        self.collision('horizontal')

        self.pos.y += self.direction.y * self.speed * dt
        self.hitbox.centery = round(self.pos.y)
        self.rect.centery = self.hitbox.centery
        self.collision('vertical')

    def collision(self, direction):
        # ---เช็คชน Hitox ---
        for sprite in self.collision_sprites.sprites():
            if hasattr(sprite, 'hitbox') and sprite.hitbox.colliderect(self.hitbox):
                # --horizontal---
                if direction == 'horizontal':
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right
                    self.rect.centerx = self.hitbox.centerx
                    self.pos.x = self.hitbox.centerx
                # ---Vertical---
                else:
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom
                    self.rect.centery = self.hitbox.centery
                    self.pos.y = self.hitbox.centery

    def update(self, dt):
        self.get_status()
        self.input()
        self.move(dt)
        self.animate(dt)


