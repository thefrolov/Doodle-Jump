" Module Sprites "
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
from random import randint

from config import *
# Base class for sprites
class Sprite(pygame.sprite.Sprite):
    " Base class for Sprite "
    def __init__(self, x = 0, y = 0):
        "Initialisation"
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        
    def move_x(self, x):
        self.x = self.x + x
        self._move()
    
    def move_y(self, y):
        self.y = self.y + y
        self._move()
        
    def set_x(self, x):
        self.x = x
        self._move()
    
    def set_y(self, y):
        self.y = y
        self._move()
        
    def _move(self):
        self.rect.center = (self.x,self.y)


    # Sprite image initialization
    def init_image(self, imgPath):
        self.image = pygame.image.load(imgPath).convert()
        self.image.set_colorkey(self.image.get_at((0,0)), RLEACCEL)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x,self.y)
        


class Monster(Sprite):
    def __init__(self, x,y):
        Sprite.__init__(self,x,y)
        self.init_image('img/monster.png')
            
    def move(self):
        self.move_x(randint(-5, 5))
        self.move_y(randint(-5, 5))


class Doodle(Sprite):
    " ласс, описывающий дудлера"
    name = "Anonymus"
    "»м€"
    score = 0
    " оличество очков"
    alive = 1
    ySpeed = 5
    x = doodle_start_position[0]
    y = doodle_start_position[1]
    def __init__(self, name):
        "»нициализаци€"
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.img_r = pygame.image.load('img/doodle.png').convert()
        self.img_l = pygame.transform.flip(self.img_r, True, False) 
        self.image = self.img_r
        self.image.set_colorkey(self.image.get_at((0,0)), RLEACCEL)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x,self.y)

    def _move(self):
        "метод, меремещающий дудлера"
        self.rect.center = (self.x,self.y)
        if self.y >= screen_height:
            self.alive = 0     
    
    def get_legs_rect(self):
        "метод, получающий пр€моугольник под ногами дудлера" 
        left = self.rect.left + self.rect.width*0.1
        top = self.rect.top + self.rect.height*0.9
        width = self.rect.width*0.6
        height = self.rect.height*0.1
        return pygame.Rect(left, top, width, height)
		
    
    def set_x(self, x):
        "метод, устанавливающий положение дудлера по оси X"
        if x < self.x:
            self.image = self.img_l
        elif x > self.x:
            self.image = self.img_r
        self.x = x
        self.image.set_colorkey(self.image.get_at((0,0)), RLEACCEL)
        self.rect = self.image.get_rect()
        self._move()
    
    def inc_y_speed(self, speed):
        "метод, увеличивающий скорость дудлера"
        self.ySpeed = self.ySpeed + speed
    
    def inc_score(self, score):
        self.score = self.score + score
        


class Platform(Sprite):

    def get_surface_rect(self):
        left = self.rect.left
        top = self.rect.top
        width = self.rect.width
        height = self.rect.height*0.1
        return pygame.Rect(left, top, width, height)
        
    def __init__(self, x, y):
        Sprite.__init__(self, x, y)
        if type(self).__name__ == "Platform":
            self.init_image('img/greenplatform.png')
            rnd = randint(-100, 100)
            if rnd >= 0:
                self.spring = Spring(self.x+randint(-int(platform_width/2 - 10), int(platform_width/2) - 10), self.y-20)
            else:
                self.spring = None
        

class MovingPlatform(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.init_image('img/blueplatform.png')    
        self.way = -1 # 1 or -1 platform way
        self.xSpeed = randint(2, 6)
        self.spring = None

    def move(self):
        self.move_x(self.xSpeed*self.way)
        if  10 < self.x < 19 or 460 < self.x < 469:
            self.way = - self.way
    
class CrashingPlatform(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.init_image('img/brownplatform.png')
        self.ySpeed = 10
        self.crashed = 0
        self.spring = None
    
    def crash(self):
        self.init_image('img/brownplatformbr.png')
        self.crashed = 1
    
    def move(self):
        if self.crashed == 0:
            pass
        
        elif self.crashed == 1:
            self.move_y(self.ySpeed)
    def renew(self):
        Platform.renew(self)
        self.init_image('img/brownplatform.png')
        self.crashed = 0
        
class Spring(Sprite):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        compressed = 0
        pygame.sprite.Sprite.__init__(self)

        self.init_image('img/spring.png')

    def compress(self):
        self.init_image('img/spring_comp.png')
        self.compressed = 1
    
    def get_top_surface(self):
        left = self.rect.left
        top = self.rect.top
        width = self.rect.width
        height = self.rect.height*0.1
        return pygame.Rect(left, top, width, height)
            

class Button(Sprite):
    x = 0
    y = 0
    def __init__(self,x,y,text):
        self.x = x
        self.y = y
        
        pygame.sprite.Sprite.__init__(self)
        self.img_sel = pygame.image.load('img/menu_selected.png').convert()
        self.img_unsel = pygame.image.load('img/menu_unselected.png').convert()
        self.textSprite = TextSprite(self.x,self.y, text)
        self.changeState(0)
        
    def changeState(self,state):
        if state == 0:
            self.image = self.img_unsel
            self.textSprite.setColor((255, 165, 149))
        elif state == 1:
            self.image = self.img_sel
            self.textSprite.setColor((243, 227, 200))
        self.image.set_colorkey(self.image.get_at((0,0)), RLEACCEL)
        
        self.rect = self.image.get_rect()
        self.rect.center = (self.x,self.y)
        
class Rectangle(pygame.Surface):
    def __init__(self, width, heigth,color):
        pygame.Surface.__init__(self,(width, heigth), pygame.SRCALPHA)
        self.fill(color)
        
        
class TextSprite(Sprite):
    def __init__(self, x, y, text='', size=35, color=(255, 255, 255)):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.font = pygame.font.Font(None, size)  # load the default font, size 25
        self.color = color         # our font color in rgb
        self.text = text
        self.generateImage() # generate the image
 
    def setText(self, text):
        self.text = text
        self.generateImage()
    def setColor(self, color):
        self.color = color
        self.generateImage()
    def setSize(self, size):
        self.font = pygame.font.Font(None, size)
        self.generateImage()
    
    def generateImage(self):
        self.image = self.font.render(self.text, True, self.color)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        
        
