import pygame
from pygame.math import Vector2 as vector
from os import walk
import os.path

class Entity(pygame.sprite.Sprite):
    def __init__(self, pos, groups, path, collision_sprites):
        super().__init__(groups)

        self.import_assets(path)
        self.frame_index = 0
        self.status = 'down'

        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center = pos)
        # -- movement attributes--
        self.pos = vector(self.rect.center)
        self.direction = vector()
        self.speed = 200
        # -- collision(การชน) ---
        self.hitbox = self.rect.inflate(-self.rect.width * 0.5, -self.rect.height/2)
        self.collision_sprites = collision_sprites
        self.attacking = False

    def import_assets(self, path):
        self.animations = {}
        # os.walk
        for index, folder in enumerate(walk(path)):
            if index == 0:
                for name in folder[1]:
                    self.animations[name] = []
            else:
                for file_name in sorted(folder[2], key=lambda string: int(string.split('.')[0])):
                    path = folder[0].replace('\\', '/') + '/' + file_name
                    # --โหลดรูปภาพ ---
                    surf = pygame.image.load(path).convert_alpha()
                    # --- หาชื่อ Key จากชื่อโฟลเดอร์ ----
                    #key = folder[0].split('/')[3]
                    key = os.path.basename(folder[0])
                    #print(key)
                    # --- เก็บใส่ Dictionary ---
                    self.animations[key].append(surf)
                    print(f"path: {path}, key: {key}")

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