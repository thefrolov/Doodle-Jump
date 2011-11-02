# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
from random import randint

# Base class for sprites
class Sprite(pygame.sprite.Sprite):
    
    x = 0
    y = 0
    
    def __init__(self, x = 0, y = 0):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        
    def moveX(self, x):
        self.x = self.x + x
        self._move()
    
    def moveY(self, y):
        self.y = self.y + y
        self._move()
        
    def setX(self, x):
        self.x = x
        self._move()
    
    def setY(self, y):
        self.y = y
        self._move()
        
    def _move(self):
        self.rect.center = (self.x,self.y)

# doodle sprite
class Doodle(Sprite):
    name = "Anonymus"
    score = 0
    alive = 1
    ySpeed = 5
    x = 240
    y = 350
    def __init__(self, name):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.img_r = pygame.image.load('img/doodle.png').convert()
        self.img_l = pygame.transform.flip(self.img_r, True, False) 
        self.image = self.img_r
        self.image.set_colorkey(self.image.get_at((0,0)), RLEACCEL)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x,self.y)

    def _move(self):
        self.rect.center = (self.x,self.y)
        if self.y >=640:
            self.alive = 0     
    
    def getLegsRect(self):
        left = self.rect.left + self.rect.width*0.1
        top = self.rect.top + self.rect.height*0.9
        width = self.rect.width*0.6
        height = self.rect.height*0.1
        return pygame.Rect(left, top, width, height)
		
    
    def setX(self, x):
        if x < self.x:
            self.image = self.img_l
        elif x > self.x:
            self.image = self.img_r
        self.x = x
        self.image.set_colorkey(self.image.get_at((0,0)), RLEACCEL)
        self.rect = self.image.get_rect()
        self._move()
    
    def incYSpeed(self, speed):
        self.ySpeed = self.ySpeed + speed
    
    def incScore(self, score):
        self.score = self.score + score
        

# base class for Platform
class Platform(Sprite):
    
    # Sprite image initialization
    def initImg(self, imgPath):
        self.image = pygame.image.load(imgPath).convert()
        self.image.set_colorkey(self.image.get_at((0,0)), RLEACCEL)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x,self.y)
        
    def getSurfaceRect(self):
        left = self.rect.left
        top = self.rect.top
        width = self.rect.width
        height = self.rect.height*0.1
        return pygame.Rect(left, top, width, height)
        
    def __init__(self, x, y):
        Sprite.__init__(self, x, y)
        if type(self).__name__ == "Platform":
            self.initImg('img/greenplatform.png')
    
    def renew(self):
        self.setX(randint(10, 470))
        self.setY(randint(-50, -30) + randint(0, 40))
        self =  MovingPlatform(self.x, self.y)
        

class MovingPlatform(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.initImg('img/blueplatform.png')    
        self.way = -1 # 1 or -1 platform way
        self.xSpeed = randint(2, 6)

    def move(self):
        self.moveX(self.xSpeed*self.way)
        if  10 < self.x < 19 or 460 < self.x < 469:
            self.way = - self.way
    
class CrashingPlatform(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.initImg('img/brownplatform.png')
        self.ySpeed = 10
        self.crashed = 0
    
    def crash(self):
        self.initImg('img/brownplatformbr.png')
        self.crashed = 1
    
    def move(self):
        if self.crashed == 0:
            pass
        
        elif self.crashed == 1:
            self.moveY(self.ySpeed)
    def renew(self):
        Platform.renew(self)
        #self.setX(randint(10, 470))
        #self.setY(randint(-50, -30) + randint(0, 30))
        self.initImg('img/brownplatform.png')
        self.crashed = 0
        

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
        
        