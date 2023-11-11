import pygame
import numpy as np
import math

pygame.init()

screenWidth = 1432
screenHeight = 1040
music = pygame.mixer.music.load('Sprites/b2/minecraft.mp3')
hitSound = pygame.mixer.Sound('Sprites/b2/hitSound.wav')
breakSound = pygame.mixer.Sound('Sprites/b2/breakSound.wav')
deathSound = pygame.mixer.Sound('Sprites/b2/deathSound.wav')
bg = pygame.image.load('Sprites/b2/bg.png')
introbg = pygame.image.load('Sprites/b2/introbg.png')
rankingbg = pygame.image.load('Sprites/b2/rankingbg.png')
fasesbg = pygame.image.load('Sprites/b2/fasesbg.png')
pausebg = pygame.image.load('Sprites/b2/pausebg.png')
gameoverbg = pygame.image.load('Sprites/b2/gameoverbg.png')
pygame.display.set_icon(pygame.image.load('Sprites/b2/icon.png'))
myFont = pygame.font.Font('Sprites/cyberdyne.ttf', 28)
tinyFont = pygame.font.Font('Sprites/cyberdyne.ttf', 14)
gameOverFont = pygame.font.Font('Sprites/cyberdyne.ttf', 70)
nameFont = pygame.font.Font('Sprites/Mangotea.ttf', 94)
heart = pygame.image.load('Sprites/heartFull.png')
hurt = pygame.image.load('Sprites/heartEmpty.png')
win = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Buggatron Breaker 2")
imgBlock1 = pygame.Surface.convert(pygame.image.load('Sprites/block1.png'))
imgBlock2a = pygame.Surface.convert(pygame.image.load('Sprites/block2a.png'))
imgBlock2b = pygame.Surface.convert(pygame.image.load('Sprites/block2b.png'))
imgBlock3a = pygame.Surface.convert(pygame.image.load('Sprites/block3a.png'))
imgBlock3b = pygame.Surface.convert(pygame.image.load('Sprites/block3b.png'))
imgBlock3c = pygame.Surface.convert(pygame.image.load('Sprites/block3c.png'))
clock = pygame.time.Clock()
Blocks = []
xSep = 54
ySep = 24


class Player(object):
    def __init__(self):
        self.runs = 0
        self.radius = 32
        self.x = (screenWidth // 2) - self.radius
        self.y = 850
        self.vel = 10
        self.diam = self.radius * 2
        self.xCentre = (self.x + self.radius)
        self.yCentre = (self.y + self.radius)
        self.lives = 3
        self.score = 0
        self.img = pygame.Surface.convert_alpha(pygame.image.load('Sprites/R01.png'))

    def update_name(self):
        if self.runs == 0:
            self.name = 'Faustão Pentelho'
        elif self.runs == 1:
            self.name = 'Guilherme Boulos'
        elif self.runs == 2:
            self.name = 'Carlinhos'
        elif self.runs == 3:
            self.name = 'Nierlatotépy'
        elif self.runs == 4:
            self.name = 'Sheila'
        elif self.runs == 5:
            self.name = 'Moriá'
        elif self.runs == 6:
            self.name = 'Morte ao Capitalismo'
        elif self.runs == 7:
            self.name = 'Venoninho Extreme'
        elif self.runs == 8:
            self.name = 'Bololo Haha'
        elif self.runs == 9:
            self.name = 'Professor me dá 10'
        elif self.runs == 10:
            self.name = 'Help me'

    def lose_life(self):
        global gameOn
        global gameOverOn

        if self.lives > 1:
            self.lives -= 1
        else:
            gameOverText = gameOverFont.render('GAME OVER', 1, (0, 0, 0))
            win.blit(gameOverText, ((screenWidth / 2 - gameOverText.get_width() // 2), (screenHeight / 2 - gameOverText.get_height() // 2)))
            pygame.display.update()
            i = 0
            while i < 250:
                pygame.time.delay(10)
                i += 1
                if event.type == pygame.QUIT:
                    i = 251
                    pygame.quit()
                    quit()
            gameOn = False
            gameOverOn = True

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))


class Ball(object):
    BallRoll = [pygame.Surface.convert_alpha(pygame.image.load('Sprites/B01.png')), pygame.Surface.convert_alpha(pygame.image.load('Sprites/B02.png')),
                pygame.Surface.convert_alpha(pygame.image.load('Sprites/B03.png')), pygame.Surface.convert_alpha(pygame.image.load('Sprites/B04.png')),
                pygame.Surface.convert_alpha(pygame.image.load('Sprites/B05.png')), pygame.Surface.convert_alpha(pygame.image.load('Sprites/B06.png')),
                pygame.Surface.convert_alpha(pygame.image.load('Sprites/B07.png')), pygame.Surface.convert_alpha(pygame.image.load('Sprites/B08.png')),
                pygame.Surface.convert_alpha(pygame.image.load('Sprites/B09.png')), pygame.Surface.convert_alpha(pygame.image.load('Sprites/B10.png'))]

    ReflectY = np.matrix([[1, 0],
                          [0, -1]])
    ReflectX = np.matrix([[-1, 0],
                          [0, 1]])

    def __init__(self, joj):
        self.radius = 10
        self.diam = self.radius * 2
        self.x = joj.xCentre - self.radius
        self.y = joj.y - self.diam
        self.vel = 7
        self.Vel = np.matrix([[-7],
                              [-7]])
        self.isMoving = False
        self.walkCount = 0
        self.xCentre = (self.x + self.radius)
        self.yCentre = (self.y + self.radius)
        self.posMatrix = np.matrix([[self.x], [self.y]])
        self.xOrigin = 0
        self.yOrigin = 0
        self.multiplier = 1
        self.accCount = 0
        self.angle = 1
        self.rect = pygame.Rect((self.x, self.y), (20,20))

    def draw(self, win):
        if self.walkCount + 1 > 30:
            self.walkCount = 0
        if self.isMoving:
            win.blit(self.BallRoll[self.walkCount // 3], (self.x, self.y))
            self.walkCount += 1
        else:
            win.blit(self.BallRoll[self.walkCount // 3], (self.x, self.y))

    def accelerate(self):
        self.multiplier += 1
        self.vel += 1
        if self.Vel.item((0, 0)) > 0:
            self.Vel[0, 0] += 1
        else:
            self.Vel[0, 0] -= 1
        if self.Vel.item((1, 0)) > 0:
            self.Vel[1, 0] += 1
        else:
            self.Vel[1, 0] -= 1

    def check_hit(self, phase):
        global gameOn
        global gameOverOn
        global Sound
        global Blocks
        distance = math.hypot((joj.x + joj.radius) - (self.x + self.radius),
                              (joj.y + joj.radius) - (self.y + self.radius))
        xAxis = np.matrix([[1],
                           [0]])
        yAxis = np.matrix([[0],
                           [1]])
        if np.transpose(self.posMatrix) @ yAxis >= screenHeight - self.diam:  # morre
            restart_pos()
            joj.lose_life()
            if Sound:
                deathSound.play()

        elif np.transpose(self.posMatrix) @ xAxis < self.vel or np.transpose(
                self.posMatrix) @ xAxis > screenWidth - self.vel - self.diam:  # bate nas paredes laterais
            self.angle = math.atan2(ball.y - ball.yOrigin, ball.x - ball.xOrigin)
            self.Vel = self.ReflectX @ self.Vel
            self.xOrigin = self.x
            self.yOrigin = self.y
            if Sound:
                hitSound.play()

        elif np.transpose(self.posMatrix) @ yAxis < 225 + self.vel:  # bate em cima
            self.angle = math.atan2(ball.y - ball.yOrigin, ball.x - ball.xOrigin)
            self.Vel = self.ReflectY @ self.Vel
            self.xOrigin = self.x
            self.yOrigin = self.y
            self.y = 226
            if Sound:
                hitSound.play()

        elif distance <= self.radius + joj.radius:  # bate no jogador
            if joj.x + joj.radius - 5 <= self.xCentre <= ball.x + joj.radius + 5:
                self.Vel = self.ReflectY @ self.Vel
            else:
                if self.angle < 0:
                    if self.xCentre > joj.x + joj.radius:
                        self.Vel = self.ReflectY @ self.ReflectX @ self.Vel
                    else:
                        self.Vel = self.ReflectY @ self.Vel
                else:
                    if self.xCentre < joj.x + joj.radius:
                        self.Vel = self.ReflectY @ self.ReflectX @ self.Vel
                    else:
                        self.Vel = self.ReflectY @ self.Vel
            if Sound:
                hitSound.play()

        else:
            for k in Blocks:
                if self.rect.colliderect(k.rect):
                    self.angle = math.atan2(ball.y - ball.yOrigin, ball.x - ball.xOrigin)
                    self.xOrigin = self.x
                    self.yOrigin = self.y
                    if Sound:
                        hitSound.play()
                        if k.life == 1:
                            breakSound.play()
                    if k.hitbox[0] <= self.xCentre <= k.hitbox[2]:
                        if self.y <= k.hitbox[3] or self.y + self.diam >= k.hitbox[1]:  # bate verticalmente nos blocos
                            self.Vel = self.ReflectY @ self.Vel
                    elif k.hitbox[1] <= self.yCentre <= k.hitbox[3]:
                        if self.x <= k.hitbox[2] or self.x + self.diam >= k.hitbox[0]:  # bate horizontalmente nos blocos
                            self.Vel = self.ReflectX @ self.Vel
                    k.life -= 1
                    if k.life == 0:
                        phase.brokenBlocks += 1
                        self.accCount += 1
                        joj.score += k.value * self.multiplier
                        Blocks.pop(Blocks.index(k))

                if phase.brokenBlocks == phase.totalBlocks:
                    winText = gameOverFont.render('TOP', 1, (0, 0, 0))
                    win.blit(winText,((screenWidth / 2 - winText.get_width() // 2), (screenHeight / 2 - winText.get_height() // 2)))
                    pygame.display.update()
                    i = 0
                    while i < 250:
                        pygame.time.delay(10)
                        i += 1
                        if event.type == pygame.QUIT:
                            i = 251
                            pygame.quit()
                            quit()
                    joj.score += joj.lives * 1000
                    gameOn = False
                    gameOverOn = True


class Block(object):

    def __init__(self, durab, x, y, e):
        self.durab = durab
        self.life = self.durab
        self.width = 50
        self.height = 20
        self.x1 = x
        self.y1 = y
        self.hitbox = (self.x1, self.y1, (self.x1 + self.width), (self.y1 + self.height))
        self.index = e
        self.value = self.durab * 100
        self.rect = ((x,y), (50,20))

    def draw(self, win):
        if self.durab == 1:
            if self.life == 1:
                win.blit(imgBlock1, (self.x1, self.y1))
        if self.durab == 2:
            if self.life == 2:
                win.blit(imgBlock2a, (self.x1, self.y1))
            elif self.life == 1:
                win.blit(imgBlock2b, (self.x1, self.y1))
        if self.durab == 3:
            if self.life == 3:
                win.blit(imgBlock3a, (self.x1, self.y1))
            elif self.life == 2:
                win.blit(imgBlock3b, (self.x1, self.y1))
            elif self.life == 1:
                win.blit(imgBlock3c, (self.x1, self.y1))


class Phase(object):

    def __init__(self, phaseCount):
        self.phaseCount = phaseCount
        self.brokenBlocks = 0
        self.y1 = 340
        if phaseCount == 0:
            self.totalBlocks = 120
            self.matrix = np.matrix([[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                                     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                                     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                                     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                                     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                                     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]])
            self.iMax = 20
            self.jMax = 6

        elif phaseCount == 1:
            self.totalBlocks = 160
            self.matrix = np.matrix([[2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
                                     [2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2],
                                     [2, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 2],
                                     [2, 2, 1, 1, 1, 1, 2, 2, 2, 1, 1, 2, 2, 2, 1, 1, 1, 1, 2, 2],
                                     [2, 2, 1, 1, 1, 1, 2, 2, 2, 1, 1, 2, 2, 2, 1, 1, 1, 1, 2, 2],
                                     [2, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 2],
                                     [2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2],
                                     [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]])
            self.iMax = 20
            self.jMax = 8

        elif phaseCount == 2:
            self.totalBlocks = 198
            self.matrix = np.matrix([[2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2],
                                     [2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2],
                                     [2, 2, 1, 1, 1, 1, 1, 2, 2, 2, 2, 1, 1, 1, 1, 1, 2, 2],
                                     [2, 2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2, 2],
                                     [2, 1, 1, 1, 2, 1, 1, 1, 2, 2, 1, 1, 1, 2, 1, 1, 1, 2],
                                     [2, 1, 1, 1, 2, 1, 1, 2, 2, 2, 2, 1, 1, 2, 1, 1, 1, 2],
                                     [2, 1, 1, 1, 2, 1, 1, 1, 2, 2, 1, 1, 1, 2, 1, 1, 1, 2],
                                     [2, 2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2, 2],
                                     [2, 2, 1, 1, 1, 1, 1, 2, 2, 2, 2, 1, 1, 1, 1, 1, 2, 2],
                                     [2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2],
                                     [2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2]])
            self.iMax = 18
            self.jMax = 11

        elif phaseCount == 3:
            self.totalBlocks = 198
            self.matrix = np.matrix([[1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2],
                                     [2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1],
                                     [1, 2, 3, 3, 1, 3, 3, 2, 3, 3, 1, 3, 3, 2, 3, 3, 1, 2],
                                     [2, 1, 3, 3, 1, 3, 3, 2, 3, 3, 1, 3, 3, 2, 3, 3, 2, 1],
                                     [1, 2, 3, 3, 1, 3, 3, 2, 3, 3, 1, 3, 3, 2, 3, 3, 1, 2],
                                     [2, 1, 3, 3, 1, 3, 3, 2, 3, 3, 1, 3, 3, 2, 3, 3, 2, 1],
                                     [1, 2, 3, 3, 1, 3, 3, 2, 3, 3, 1, 3, 3, 2, 3, 3, 1, 2],
                                     [2, 1, 3, 3, 1, 3, 3, 2, 3, 3, 1, 3, 3, 2, 3, 3, 2, 1],
                                     [1, 2, 3, 3, 1, 3, 3, 2, 3, 3, 1, 3, 3, 2, 3, 3, 1, 2],
                                     [2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1],
                                     [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2]])
            self.iMax = 18
            self.jMax = 11

        elif phaseCount == 4:
            self.totalBlocks = 153
            self.matrix = np.matrix([[3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3],
                                     [3, 3, 2, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 2, 3, 3],
                                     [3, 3, 2, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 2, 3, 3],
                                     [3, 3, 2, 2, 1, 1, 1, 3, 3, 3, 1, 1, 1, 2, 2, 3, 3],
                                     [3, 3, 2, 2, 2, 2, 2, 3, 3, 3, 2, 2, 2, 2, 2, 3, 3],
                                     [3, 3, 2, 2, 1, 1, 1, 3, 3, 3, 1, 1, 1, 2, 2, 3, 3],
                                     [3, 3, 2, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 2, 3, 3],
                                     [3, 3, 2, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 2, 3, 3],
                                     [3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3]])
            self.iMax = 17
            self.jMax = 9
        elif phaseCount == 5:
            self.totalBlocks = 127
            self.matrix = np.matrix([[3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
                                     [3, 2, 3, 3, 1, 0, 1, 1, 0, 1, 1, 0, 1, 3, 3, 2, 3],
                                     [3, 3, 2, 3, 0, 1, 1, 0, 3, 0, 1, 1, 0, 3, 2, 3, 3],
                                     [3, 2, 3, 0, 1, 1, 0, 3, 2, 3, 0, 1, 1, 0, 3, 2, 3],
                                     [3, 3, 2, 0, 1, 0, 3, 2, 2, 2, 3, 0, 1, 0, 2, 3, 3],
                                     [3, 2, 3, 0, 1, 1, 0, 3, 2, 3, 0, 1, 1, 0, 3, 2, 3],
                                     [3, 3, 2, 3, 0, 1, 1, 0, 3, 0, 1, 1, 0, 3, 2, 3, 3],
                                     [3, 2, 3, 3, 1, 0, 1, 1, 0, 1, 1, 0, 1, 3, 3, 2, 3],
                                     [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]])
            self.iMax = 17
            self.jMax = 9
        elif phaseCount == 6:
            self.totalBlocks = 153
            self.matrix = np.matrix([[2, 3, 3, 3, 3, 1, 1, 1, 3, 1, 1, 1, 3, 3, 3, 3, 2],
                                     [2, 3, 3, 3, 1, 3, 1, 1, 3, 1, 1, 3, 1, 3, 3, 3, 2],
                                     [2, 3, 3, 3, 1, 1, 3, 1, 3, 1, 3, 1, 1, 3, 3, 3, 2],
                                     [2, 3, 3, 3, 1, 1, 1, 3, 2, 3, 1, 1, 1, 3, 3, 3, 2],
                                     [2, 3, 3, 3, 3, 3, 3, 2, 2, 2, 3, 3, 3, 3, 3, 3, 2],
                                     [2, 3, 3, 3, 1, 1, 1, 3, 2, 3, 1, 1, 1, 3, 3, 3, 2],
                                     [2, 3, 3, 3, 1, 1, 3, 1, 3, 1, 3, 1, 1, 3, 3, 3, 2],
                                     [2, 3, 3, 3, 1, 3, 1, 1, 3, 1, 1, 3, 1, 3, 3, 3, 2],
                                     [2, 3, 3, 3, 3, 1, 1, 1, 3, 1, 1, 1, 3, 3, 3, 3, 2]])
            self.iMax = 17
            self.jMax = 9
        elif phaseCount == 7:
            self.totalBlocks = 153
            self.matrix = np.matrix([[2, 3, 3, 2, 2, 3, 3, 3, 2, 3, 3, 3, 2, 2, 3, 3, 2],
                                     [2, 3, 3, 2, 2, 3, 3, 3, 2, 3, 3, 3, 2, 2, 3, 3, 2],
                                     [2, 3, 3, 2, 2, 1, 1, 1, 2, 1, 1, 1, 2, 2, 3, 3, 2],
                                     [2, 3, 3, 2, 2, 1, 1, 1, 2, 1, 1, 1, 2, 2, 3, 3, 2],
                                     [2, 3, 3, 2, 2, 3, 3, 3, 2, 3, 3, 3, 2, 2, 3, 3, 2],
                                     [2, 3, 3, 2, 2, 1, 1, 1, 2, 1, 1, 1, 2, 2, 3, 3, 2],
                                     [2, 3, 3, 2, 2, 1, 1, 1, 2, 1, 1, 1, 2, 2, 3, 3, 2],
                                     [2, 3, 3, 2, 2, 3, 3, 3, 2, 3, 3, 3, 2, 2, 3, 3, 2],
                                     [2, 3, 3, 2, 2, 3, 3, 3, 2, 3, 3, 3, 2, 2, 3, 3, 2]])
            self.iMax = 17
            self.jMax = 9
        elif phaseCount == 8:
            self.totalBlocks = 153
            self.matrix = np.matrix([[3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
                                     [3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3],
                                     [3, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 3],
                                     [3, 1, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 1, 3],
                                     [3, 1, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 1, 3],
                                     [3, 1, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 1, 3],
                                     [3, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 3],
                                     [3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3],
                                     [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]])
            self.iMax = 17
            self.jMax = 9
        elif phaseCount == 9:
            self.totalBlocks = 153
            self.matrix = np.matrix([[2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2],
                                     [2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2],
                                     [2, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3, 2],
                                     [3, 3, 3, 1, 1, 1, 3, 3, 2, 3, 3, 1, 1, 1, 3, 3, 3],
                                     [3, 3, 1, 1, 3, 3, 3, 2, 2, 2, 3, 3, 3, 1, 1, 3, 3],
                                     [3, 3, 3, 1, 1, 1, 3, 3, 2, 3, 3, 1, 1, 1, 3, 3, 3],
                                     [2, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3, 2],
                                     [2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2],
                                     [2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2]])
            self.iMax = 17
            self.jMax = 9
        self.matrix = self.matrix.getT()
        self.x1 = (screenWidth - (self.iMax * xSep)) / 2

    def init_phase(self):
        global Blocks
        x1 = self.x1
        y1 = self.y1
        e = 0
        for i in range(0, self.iMax):
            for j in range(0, self.jMax):
                blockType = self.matrix.item((i, j))
                if blockType > 0:
                    Blocks.append(Block(blockType, (x1 + (i * xSep)), (y1 + (j * ySep)), e))
                e += 1


class Button:
    global mousePos

    def __init__(self, x, y, width, height, img, imgOver):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.img = pygame.Surface.convert_alpha(pygame.image.load(img))
        self.imgOver = pygame.Surface.convert_alpha(pygame.image.load(imgOver))
        self.rect = pygame.Rect((x,y), (width,height))

    def draw(self, win):
        if not self.is_over(mousePos):
            win.blit(self.img, (self.x, self.y))
        else:
            win.blit(self.imgOver, (self.x, self.y))

    def is_over(self, pos):
        if self.rect.collidepoint(pos):
            return True
        return False


def restart_pos():
    ball.isMoving = False
    joj.x = (screenWidth // 2) - ball.radius
    ball.x = joj.x + joj.radius - ball.radius
    ball.y = joj.y - ball.diam
    ball.accCount = 0
    ball.Vel[0, 0] = -7
    ball.Vel[1, 0] = -7
    ball.vel = 7
    ball.multiplier = 1


def restart():
    Blocks.clear()
    joj.score = 0
    joj.lives = 3
    joj.runs += 1
    restart_pos()


def window_manager():
    global introOn
    global fasesOn
    global scoreOn
    global pauseOn
    global gameOverOn
    if introOn:
        intro()
    elif scoreOn:
        ranking()
    elif fasesOn:
        fases()
    elif pauseOn:
        pause()
    elif gameOverOn:
        game_over()


def redraw_intro_window():
    global Music
    global Sound
    win.blit(introbg, (0, 0))
    btnStart.draw(win)
    btnScore.draw(win)
    if Music:
        btnMusicOn.draw(win)
    else:
        btnMusicOff.draw(win)
    if Sound:
        btnSoundOn.draw(win)
    else:
        btnSoundOff.draw(win)
    pygame.display.update()


def intro():
    global Music
    global Sound
    global fasesOn
    global introOn
    global scoreOn
    global mousePos
    global handled

    pygame.mouse.set_visible(True)

    if pygame.mouse.get_pressed()[0] and not handled:
        if btnStart.is_over(mousePos):
            introOn = False
            fasesOn = True
        elif btnScore.is_over(mousePos):
            scoreOn = True
            introOn = False
        elif Music:
            if btnMusicOn.is_over(mousePos):
                pygame.mixer.music.pause()
                Music = False
        else:
            if btnMusicOff.is_over(mousePos):
                pygame.mixer.music.unpause()
                Music = True
        if Sound:
            if btnSoundOn.is_over(mousePos):
                Sound = False
        else:
            if btnSoundOff.is_over(mousePos):
                Sound = True

    redraw_intro_window()


def ranking():
    global scoreOn
    global introOn
    global handled

    pygame.mouse.set_visible(True)
    if pygame.mouse.get_pressed()[0] and not handled:
        if btnBack.is_over(mousePos):
            scoreOn = False
            introOn = True
    redraw_ranking_window()


def redraw_ranking_window():
    win.blit(rankingbg, (0, 0))
    btnBack.draw(win)
    SortedRank = sorted(Rank, key=sort_second, reverse=True)
    x1 = 400
    x2 = 970
    e = 0

    for k in SortedRank:
        if e < 5:
            nome = nameFont.render(str(k[0]), 1, (255, 255, 255))
            pontuacao = myFont.render(str(k[1]), 1, (255, 255, 255))
            if e == 0:
                win.blit(nome, (x1, 190))
                if k[1] >= 10000:
                    win.blit(pontuacao, (x2 - 30, 220))
                else:
                    win.blit(pontuacao, (x2, 220))
            elif e == 1:
                win.blit(nome, (x1, 340))
                if k[1] >= 10000:
                    win.blit(pontuacao, (x2 - 30, 370))
                else:
                    win.blit(pontuacao, (x2, 370))
            elif e == 2:
                win.blit(nome, (x1, 500))
                if k[1] >= 10000:
                    win.blit(pontuacao, (x2 - 30, 530))
                else:
                    win.blit(pontuacao, (x2, 530))
            elif e == 3:
                win.blit(nome, (x1, 660))
                if k[1] >= 10000:
                    win.blit(pontuacao, (x2 - 30, 690))
                else:
                    win.blit(pontuacao, (x2, 690))
            elif e == 4:
                win.blit(nome, (x1, 825))
                if k[1] >= 10000:
                    win.blit(pontuacao, (x2 - 30, 840))
                else:
                    win.blit(pontuacao, (x2, 840))
            e += 1
        else:
            break

    pygame.display.update()


def sort_second(elem):
    return elem[1]


def fases():
    global gameOn
    global fasesOn
    global phase
    global introOn
    global handled

    pygame.mouse.set_visible(True)
    if pygame.mouse.get_pressed()[0] and not handled:
        if btnBack.is_over(mousePos):
            fasesOn = False
            introOn = True
        elif btnFase1.is_over(mousePos):
            phase = Phase(0)
            phase.init_phase()
            gameOn = True
            fasesOn = False
            joj.update_name()
        elif btnFase2.is_over(mousePos):
            phase = Phase(1)
            phase.init_phase()
            gameOn = True
            fasesOn = False
            joj.update_name()
        elif btnFase3.is_over(mousePos):
            phase = Phase(2)
            phase.init_phase()
            gameOn = True
            fasesOn = False
            joj.update_name()
        elif btnFase4.is_over(mousePos):
            phase = Phase(3)
            phase.init_phase()
            gameOn = True
            fasesOn = False
            joj.update_name()
        elif btnFase5.is_over(mousePos):
            phase = Phase(4)
            phase.init_phase()
            gameOn = True
            fasesOn = False
            joj.update_name()
        elif btnFase6.is_over(mousePos):
            phase = Phase(5)
            phase.init_phase()
            gameOn = True
            fasesOn = False
            joj.update_name()
        elif btnFase7.is_over(mousePos):
            phase = Phase(6)
            phase.init_phase()
            gameOn = True
            fasesOn = False
            joj.update_name()
        elif btnFase8.is_over(mousePos):
            phase = Phase(7)
            phase.init_phase()
            gameOn = True
            fasesOn = False
            joj.update_name()
        elif btnFase9.is_over(mousePos):
            phase = Phase(8)
            phase.init_phase()
            gameOn = True
            fasesOn = False
            joj.update_name()
        elif btnFase10.is_over(mousePos):
            phase = Phase(9)
            phase.init_phase()
            gameOn = True
            fasesOn = False
            joj.update_name()

    redraw_fases_window()


def redraw_fases_window():
    win.blit(fasesbg, (0, 0))
    btnBack.draw(win)
    btnFase1.draw(win)
    btnFase2.draw(win)
    btnFase3.draw(win)
    btnFase4.draw(win)
    btnFase5.draw(win)
    btnFase6.draw(win)
    btnFase7.draw(win)
    btnFase8.draw(win)
    btnFase9.draw(win)
    btnFase10.draw(win)
    pygame.display.update()


def pause():
    global pauseOn
    global gameOn
    global introOn
    global phase
    global Music
    global Sound
    global handled
    pygame.mouse.set_visible(True)
    if pygame.mouse.get_pressed()[0] and not handled:
        if btnResume.is_over(mousePos):
            pauseOn = False
            gameOn = True
        elif btnMenu1.is_over(mousePos):
            restart()
            pauseOn = False
            introOn = True
        elif btnRestart.is_over(mousePos):
            restart()
            phase = Phase(phase.phaseCount)
            phase.init_phase()
            pauseOn = False
            gameOn = True
        elif Music:
            if btnMusicOn.is_over(mousePos):
                pygame.mixer.music.pause()
                Music = False
        else:
            if btnMusicOff.is_over(mousePos):
                pygame.mixer.music.unpause()
                Music = True
        if Sound:
            if btnSoundOn.is_over(mousePos):
                Sound = False
        else:
            if btnSoundOff.is_over(mousePos):
                Sound = True

    redraw_pause_window()


def redraw_pause_window():
    win.blit(pausebg, (0, 0))
    btnResume.draw(win)
    btnMenu1.draw(win)
    btnRestart.draw(win)
    if Music:
        btnMusicOn.draw(win)
    else:
        btnMusicOff.draw(win)
    if Sound:
        btnSoundOn.draw(win)
    else:
        btnSoundOff.draw(win)

    pygame.display.update()


def game_over():
    global gameOn
    global introOn
    global gameOverOn
    global handled
    pygame.mouse.set_visible(True)

    if pygame.mouse.get_pressed()[0] and not handled:
        if btnMenu.is_over(mousePos):
            Rank.append((joj.name, joj.score))
            gameOverOn = False
            introOn = True
            restart()
    redraw_game_over_window()


def redraw_game_over_window():
    win.blit(gameoverbg, (0, 0))
    pontuacao = gameOverFont.render(str(joj.score), 1, (255, 255, 255))
    win.blit(pontuacao, (screenWidth / 2 - pontuacao.get_width() / 2, 740))
    nome = nameFont.render(joj.name, 1, (255, 255, 255))
    win.blit(nome, (screenWidth / 2 - nome.get_width() / 2, 390))
    btnMenu.draw(win)
    pygame.display.update()


def phase_design():
    global myFont

    level = phase.phaseCount + 1
    textLevel = gameOverFont.render(str(level), 1, (0, 0, 0))
    if phase.phaseCount == 0:
        win.blit(textLevel, (1014, 80))
    if phase.phaseCount == 1:
        win.blit(textLevel, (997, 80))
    if phase.phaseCount == 2:
        win.blit(textLevel, (997, 80))
    if phase.phaseCount == 3:
        win.blit(textLevel, (997, 80))
    if phase.phaseCount == 4:
        win.blit(textLevel, (996, 80))
    if phase.phaseCount == 5:
        win.blit(textLevel, (995, 80))
    if phase.phaseCount == 6:
        win.blit(textLevel, (997, 80))
    if phase.phaseCount == 7:
        win.blit(textLevel, (995, 80))
    if phase.phaseCount == 8:
        win.blit(textLevel, (995, 80))
    if phase.phaseCount == 9:
        win.blit(textLevel, (982, 80))
    for k in Blocks:
        k.draw(win)


def redraw_game_window():
    win.blit(bg, (0, 0))
    scoreText = myFont.render(str(joj.score), 1, (0, 0, 0))
    win.blit(scoreText, (40, 80))
    total = myFont.render('/' + str(phase.totalBlocks), 1, (0, 0, 0))
    objective = myFont.render(str(phase.brokenBlocks), 1, (0, 0, 0))
    if phase.brokenBlocks < 10:
        win.blit(objective, (1225, 100))
        win.blit(total, (1250, 100))
    elif 10 <= phase.brokenBlocks < 20:
        win.blit(objective, (1215, 100))
        win.blit(total, (1250, 100))
    elif 20 <= phase.brokenBlocks < 100:
        win.blit(objective, (1210, 100))
        win.blit(total, (1260, 100))
    elif phase.brokenBlocks >= 100:
        win.blit(objective, (1210, 100))
        win.blit(total, (1270, 100))

    if joj.lives == 3:
        win.blit(heart, (30, 180))
        win.blit(heart, (52, 180))
        win.blit(heart, (74, 180))
    elif joj.lives == 2:
        win.blit(heart, (30, 180))
        win.blit(heart, (52, 180))
        win.blit(hurt, (74, 180))
    elif joj.lives == 1:
        win.blit(heart, (30, 180))
        win.blit(hurt, (52, 180))
        win.blit(hurt, (74, 180))

    joj.draw(win)
    ball.draw(win)
    phase_design()
    pygame.display.update()


# mainloop
introOn = True
gameOn = False
fasesOn = False
scoreOn = False
pauseOn = False
gameOverOn = False
btnStart = Button(516, 410, 400, 200, 'Sprites/b2/btnStart.png', 'Sprites/b2/btnStartOver.png')
btnScore = Button(516, 620, 400, 200, 'Sprites/b2/btnScore.png', 'Sprites/b2/btnScoreOver.png')
btnMusicOn = Button(516, 830, 80, 80, 'Sprites/b2/btnMusicOn.png', 'Sprites/b2/btnMusicOnOver.png')
btnMusicOff = Button(516, 830, 80, 80, 'Sprites/b2/btnMusicOff.png', 'Sprites/b2/btnMusicOffOver.png')
btnSoundOn = Button(836, 830, 80, 80, 'Sprites/b2/btnSoundOn.png', 'Sprites/b2/btnSoundOnOver.png')
btnSoundOff = Button(836, 830, 80, 80, 'Sprites/b2/btnSoundOff.png', 'Sprites/b2/btnSoundOffOver.png')
btnFase1 = Button(300, 200, 200, 120, 'Sprites/b2/btnFase1.png', 'Sprites/b2/btnFase1Over.png')
btnFase2 = Button(600, 200, 200, 120, 'Sprites/b2/btnFase2.png', 'Sprites/b2/btnFase2Over.png')
btnFase3 = Button(900, 200, 200, 120, 'Sprites/b2/btnFase3.png', 'Sprites/b2/btnFase3Over.png')
btnFase4 = Button(300, 400, 200, 120, 'Sprites/b2/btnFase4.png', 'Sprites/b2/btnFase4Over.png')
btnFase5 = Button(600, 400, 200, 120, 'Sprites/b2/btnFase5.png', 'Sprites/b2/btnFase5Over.png')
btnFase6 = Button(900, 400, 200, 120, 'Sprites/b2/btnFase6.png', 'Sprites/b2/btnFase6Over.png')
btnFase7 = Button(300, 600, 200, 120, 'Sprites/b2/btnFase7.png', 'Sprites/b2/btnFase7Over.png')
btnFase8 = Button(600, 600, 200, 120, 'Sprites/b2/btnFase8.png', 'Sprites/b2/btnFase8Over.png')
btnFase9 = Button(900, 600, 200, 120, 'Sprites/b2/btnFase9.png', 'Sprites/b2/btnFase9Over.png')
btnFase10 = Button(600, 800, 200, 120, 'Sprites/b2/btnFase10.png', 'Sprites/b2/btnFase10Over.png')
btnResume = Button(516, 300, 400, 120, 'Sprites/b2/btnResume.png', 'Sprites/b2/btnResumeOver.png')
btnRestart = Button(516, 470, 400, 120, 'Sprites/b2/btnRestart.png', 'Sprites/b2/btnRestartOver.png')
btnMenu = Button(516, 900, 400, 120, 'Sprites/b2/btnMenu.png', 'Sprites/b2/btnMenuOver.png')
btnMenu1 = Button(516, 640, 400, 120, 'Sprites/b2/btnMenu.png', 'Sprites/b2/btnMenuOver.png')
btnBack = Button(50, 40, 80, 80, 'Sprites/b2/btnBack.png', 'Sprites/b2/btnBackOver.png')
Music = True
Sound = True
pygame.mixer.music.play(-1)
hitSound.set_volume(0.01)
breakSound.set_volume(0.01)
Rank = []
joj = Player()
ball = Ball(joj)
run = True
while run:
    clock.tick(30)
    Keys = pygame.key.get_pressed()
    handled = pygame.mouse.get_pressed()[0]
    mousePos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            quit()

    window_manager()

    if gameOn:
        pygame.mouse.set_visible(False)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                gameOn = False
                pauseOn = True
        if not ball.isMoving:
            if Keys[pygame.K_SPACE]:
                ball.isMoving = True
        else:
            if 0 < mousePos[0] < screenWidth - joj.diam:
                joj.x = mousePos[0]
            if ball.isMoving:
                ball.x += ball.Vel.item((0, 0))
                ball.y += ball.Vel.item((1, 0))
                ball.xCentre = ball.x + ball.radius
                ball.yCentre = ball.y + ball.radius
                ball.posMatrix = ([[ball.x],
                                   [ball.y]])
                ball.rect = pygame.Rect((ball.x, ball.y), (20, 20))
                ball.check_hit(phase)
        if ball.accCount//10 > 0:
            ball.accCount = 0
            ball.accelerate()
        redraw_game_window()

pygame.quit()
