import pygame
from sys import exit
from math import sqrt

SIZE = W, H = (800, 600)
GREY = (59, 59, 59)
GREEN = (80, 200, 120)
BLUE = (12, 34, 250)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
dx = 0.2
enemy_offset = 60
enemy_quan = 10

class Bullet:
    def __init__(self, x, y):
        self.r = 5
        self.offset = 20 
        self.x = x + self.offset
        self.y = y
        self.dy = 0.1
        self.exist = True

    def hit(self, enemies):
        for e in enemies:
            dist = sqrt((self.x - e.x)*(self.x - e.x)\
                    + (self.y - e.y)*(self.y - e.y))
            if dist <= e.r + self.r:
                e.alive = False
                self.exist = False
                return

    def move(self):
        self.y = self.y - self.dy
        if self.y < 0: self.exist = False

    def draw(self, screen):
        pygame.draw.circle(screen, BLACK,\
                    (round(self.x), round(self.y)), self.r)

class Enemy:
    def __init__(self, x, y):
        self.r = 20
        self.x = x
        self.y = y
        self.dx = 0.03
        self.py = -1
        self.mode = True #True - horizontal, False - vert
        self.alive = True

    def draw(self, screen):
        pygame.draw.circle(screen, BLUE,\
                    (round(self.x), round(self.y)), self.r)

    def move(self):
        if self.mode:
            self.x = self.x + self.dx
        else:
            if self.y - self.py < 50:
                self.y = self.y + abs(self.dx)
            else:
                self.mode = True
                return
            
        if (self.x < 0 + self.r or self.x > W - self.r)\
           and self.mode:
            self.mode = False
            self.dx = self.dx * (-1)
            self.py = self.y
            
        if self.y > H - 150:
            self.y = 30
            self.x = 30
            self.mode = True

class Player:
    def __init__(self):
        self.side = 40
        self.x = W / 2 - self.side / 2
        self.y = H - 20
        self.dir = 0 # 0 - stay, 1 - left, 2 - right

    def setDir(self, direct): self.dir = direct
    
    def move(self):
        if self.dir == 2: self.x = self.x + dx
        elif self.dir == 1: self.x = self.x - dx
        
        if self.x < 0: self.x = W - self.side
        elif self.x >= W - self.side: self.x = 0

    def draw(self, screen):
        pygame.draw.polygon(screen, GREEN,\
            ((self.x, self.y),\
             (self.x + self.side/2, self.y - self.side/2),
             (self.x + self.side, self.y)))


def run():
    pygame.init()
    pygame.display.set_caption("SPACE INVADERS")
    screen = pygame.display.set_mode(SIZE)
    clock = pygame.time.Clock()

    player = Player()
    bullets = []
    enemies = []

    while 1:
        #clock.tick()
        if len(enemies) == 0:
            for i in range(enemy_quan):
                enemies.append(Enemy(30 + i * enemy_offset, 30))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.setDir(1)
                if event.key == pygame.K_RIGHT:
                    player.setDir(2)
                if event.key == pygame.K_SPACE:
                    bullets.append(Bullet(player.x, player.y))
            elif event.type == pygame.KEYUP and\
                 event.key != pygame.K_SPACE:
                if event.key == pygame.K_RIGHT:
                    player.setDir(0)
                if event.key == pygame.K_LEFT:
                    player.setDir(0)


        player.move()
        for enemy in enemies: enemy.move()        
        for bullet in bullets:
            bullet.move()
            bullet.hit(enemies)
        
        screen.fill(GREY)
        player.draw(screen)
        for enemy in enemies: enemy.draw(screen)
        for bullet in bullets: bullet.draw(screen)

        for bullet in bullets:
            if not bullet.exist:
                bullets.remove(bullet)
        for enemy in enemies:
            if not enemy.alive:
                enemies.remove(enemy)

        pygame.display.update()
        




if __name__ == "__main__":
    run()
