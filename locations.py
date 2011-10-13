# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
from sprites import Doodle, Platform, Header, Button, TextSprite
from random import randint
import sys

# Base class for location
class Location(object):
    parent = None
    def __init__(self, parent):
        self.window = pygame.display.get_surface()
        self.parent = parent
        self.background = pygame.image.load('img/background.png')
    def event(self,event):
        pass
    def draw(self):
        pass


# first menu location
class Start_location(Location):
    
    def __init__(self, parent):
        Location.__init__(self, parent)
        pygame.mouse.set_visible(1)
        self.startbtn = Button(240, 200, "Start")
        self.exitbtn = Button(240, 270, "Exit")
        self.buttons = pygame.sprite.Group()
        self.buttons_captions = pygame.sprite.Group()
        self.buttons_captions.add(self.startbtn.textSprite)
        self.buttons_captions.add(self.exitbtn.textSprite)
        self.buttons.add(self.startbtn)
        self.buttons.add(self.exitbtn)
        
    def draw(self):
        self.window.blit(self.background, (0, 0))        
        self.buttons.draw(self.window)
        self.buttons_captions.draw(self.window)
    def event(self,event):
        if event.type == MOUSEMOTION:
            for btn in self.buttons:
                if btn.rect.collidepoint(pygame.mouse.get_pos()):
                #pass
                    btn.changeState(1)
                else:
                #pass
                    btn.changeState(0)
        elif event.type == MOUSEBUTTONUP:
            if self.startbtn.rect.collidepoint(pygame.mouse.get_pos()):
                self.parent.location = Game_location(self.parent,"Vasya")
            elif self.exitbtn.rect.collidepoint(pygame.mouse.get_pos()):
                sys.exit()





# gameplay location
class Game_location(Location):
    
    gravitation = 0.2
    
    def __init__(self, parent, name):
        Location.__init__(self, parent)
        pygame.mouse.set_visible(0)
        self.doodle = Doodle()
        self.doodle.name = name
        self.allsprites = pygame.sprite.Group()
        self.allsprites.add(self.doodle)
        for i in range(0, 14):
            self.allsprites.add(Platform(randint(-100, 450), randint(0, 640), randint(0, 2)))
        
        self.header = Header()
    
    def draw(self):
        self.window.blit(self.background, (0, 0))
        
        if self.doodle.alive == 1: 
            # doodler animation
            mousePos = pygame.mouse.get_pos()
            self.doodle.ySpeed = self.doodle.ySpeed - self.gravitation
            self.doodle.incY(-self.doodle.ySpeed)
            self.doodle.setX(mousePos[0])
            self.doodle._move()
            
            if self.doodle.ySpeed > 3 and self.doodle.y < 300:
                for spr in self.allsprites:  # moving world
                    spr._moveY(self.doodle.ySpeed)
                                 
            for spr in self.allsprites:
                if type(spr).__name__ == "Platform":
                    if spr.pType == 1 or (spr.pType == 2 and spr.crashed == 2): # move blue and crashed platforms
                        spr._move()
                    # if platform under legs
                    if self.doodle.getLegsRect().colliderect(spr.getSurfaceRect()) and self.doodle.ySpeed < 0: # legs on platform
                        if spr.pType == 0 or spr.pType == 1:
                            self.doodle.ySpeed = 10
                             
                        elif spr.pType == 2:
                            if spr.crashed == 0:
                                spr.crashed = 1
                                spr._move()
                    
                    if spr.y > 620:         # renew platforms
                        spr.x = randint(10, 470)
                        spr.y = randint(-50, -30) + randint(0, 30)
                        spr.changepType(randint(0, 2))
                        spr._move()
                
            self.allsprites.draw(self.window)
            self.window.blit(self.header, (0,0))
        else:
            #if dead - load exit location
            self.parent.location = Game_location(self.parent,self.doodle.name)

    def event(self,event):
        if event.type == KEYDOWN:
            print event.key


# game stats and exit location
class Exit_location(Location):
    def __init__(self, parent, name, score):
        Location.__init__(self, parent)
        self.background = pygame.image.load('img/background.png')
        print "Exiting"
