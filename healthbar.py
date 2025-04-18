import pygame

pygame.init()
pygame.display.set_caption('Health Bar')

class HealthBar():
    def __init__(self, x, y, w, h, max_hp):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.hp = max_hp
        self.max_hp = max_hp

    def draw(self, surface):
        # Tính tỷ lệ máu còn lại
        ratio = self.hp / self.max_hp
        # Vẽ nền đỏ cho thanh máu
        pygame.draw.rect(surface, "red", (self.x, self.y, self.w, self.h))
        # Vẽ thanh màu xanh lá đại diện cho máu còn lại
        pygame.draw.rect(surface, "green", (self.x, self.y, self.w * ratio, self.h))

    def update(self, amount):
        # Giảm máu và đảm bảo máu không xuống dưới 0
        self.hp = max(0, self.hp - amount)
