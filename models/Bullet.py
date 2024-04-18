import pygame
from models.Constant import Direction

class Bullet:
    def __init__(self, bullet_type="player", speed_bullet=10) -> None:
        self.image = pygame.image.load(f'./images/bullet/{bullet_type}.png')
        self.rect = self.image.get_rect()
        self.direction = Direction.left
        self.speed = speed_bullet
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)
    
    def move(self):
        if self.direction == Direction.left:
            self.rect.x -= self.speed
        elif self.direction == Direction.right:
            self.rect.x += self.speed
