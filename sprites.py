# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *


# doodle sprite
class Doodle(pygame.sprite.Sprite):
    name = "Anonymus"
    score = 0
    alive = 1
    ySpeed = 5
    x = 240
    y = 500
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.img_r = pygame.image.load('img/doodle_r.png').convert()
        self.img_l = pygame.image.load('img/doodle_l.png').convert()
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
		
    def _moveY(self, speed):
        self.y = self.y + speed
        self.rect.center = (self.x,self.y)
        
    def setX(self,x):
        if x < self.x:
            self.image = self.img_l
        elif x > self.x:
            self.image = self.img_r
        self.x = x
        self.image.set_colorkey(self.image.get_at((0,0)), RLEACCEL)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x,self.y)
        
    def incY(self,y):
        if y < 0:
            self.score = self.score + abs(y)
            #print self.score
        self.y = self.y + y



class Platform(pygame.sprite.Sprite):
    """ platfofm:
        0 : green static
        1 : blue moving
        2 : brown crashing
    """
    x = 0
    y = 0

    def __init__(self, x, y, pType):
        self.x = x
        self.y = y
        self.pType = pType
        pygame.sprite.Sprite.__init__(self)
        if pType == 0:
            self.image = pygame.image.load('img/greenplatform.png').convert()
        elif pType == 1:
            self.image = pygame.image.load('img/blueplatform.png').convert()
            self.way = -1 # 1 or -1 platform way
            self.xSpeed = 5
        elif pType == 2:
            self.image = pygame.image.load('img/brownplatform.png').convert()
            self.ySpeed = 10
            self.crashed = 0
            
        self.image.set_colorkey(self.image.get_at((0,0)), RLEACCEL)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x,self.y)
    
    
    def getSurfaceRect(self):
        left = self.rect.left
        top = self.rect.top
        width = self.rect.width
        height = self.rect.height*0.1
        return pygame.Rect(left, top, width, height)
    
    def changepType(self, pType):
        if not pType == self.pType:
            if pType == 0:
                self.image = pygame.image.load('img/greenplatform.png').convert()
            elif pType == 1:
                self.image = pygame.image.load('img/blueplatform.png').convert()
                self.way = -1 # 1 or -1 platform way
                self.xSpeed = 5
            elif pType == 2:
                self.image = pygame.image.load('img/brownplatform.png').convert()
                self.ySpeed = 10
                self.crashed = 0
            
            self.image.set_colorkey(self.image.get_at((0,0)), RLEACCEL)
            self.rect = self.image.get_rect()
            self.rect.center = (self.x,self.y)
            self.pType = pType
    
    def _move(self):
        if self.pType == 0:
            pass
        elif self.pType == 1:
            self.x = self.x + self.xSpeed*self.way
            if self.x < 20 or self.x > 460:
                self.way = - self.way
        elif self.pType == 2:
            if self.crashed == 1:
                self.image = pygame.image.load('img/blueplatformbr.png').convert()
                self.image.set_colorkey(self.image.get_at((0,0)), RLEACCEL)
                self.rect = self.image.get_rect()
                self.rect.center = (self.x,self.y)
                self.crashed = 2
            elif self.crashed == 2:
                self.y = self.y + self.ySpeed
                
        self.rect.center = (self.x,self.y)
        
    def _moveY(self, speed):
        self.y = self.y + speed
        self.rect.center = (self.x,self.y)
        

class Button(pygame.sprite.Sprite):
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
        
class Header(pygame.Surface):
    def __init__(self):
        pygame.Surface.__init__(self,(480,50), pygame.SRCALPHA)
        self.fill((0,191,255,128))
        
        
class TextSprite(pygame.sprite.Sprite):
 
    def __init__(self, x, y, text=''):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.font = pygame.font.Font(None, 25)  # load the default font, size 25
        self.color = (255, 165, 149)         # our font color in rgb
        self.text = text
        self.generateImage() # generate the image
 
    def setText(self, text):
        self.text = text
        self.generateImage()
    def setColor(self, color):
        self.color = color
        self.generateImage()
    
    def generateImage(self):
        self.image = self.font.render(self.text, True, self.color)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)