# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
from sprites import Doodle, Platform, MovingPlatform, CrashingPlatform, Header, Button, TextSprite
import sys
from random import randint

# Base class for location
class Location(object):
    parent = None
    def __init__(self, parent):
        self.window = pygame.display.get_surface()
        self.parent = parent
        self.background = pygame.image.load('img/background.png').convert()
    def event(self,event):
        pass
    def draw(self):
        pass


# first menu location
class StartLocation(Location):
    
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
        self.window.blit(self.background, (0, 0))
        
    def draw(self):
        self.buttons.clear(self.window, self.background)
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
                self.parent.location = GameLocation(self.parent,"Vasya")
            elif self.exitbtn.rect.collidepoint(pygame.mouse.get_pos()):
                sys.exit()





# gameplay location
class GameLocation(Location):
    
    gravitation = 0.2
    
    def __init__(self, parent, name):
        Location.__init__(self, parent)
        pygame.mouse.set_visible(0)
        self.doodle = Doodle(name)
        self.doodle.name = name
        self.allsprites = pygame.sprite.Group()
        self.allsprites.add(self.doodle)
        for i in range(0, 8):
            self.allsprites.add(self.randomPlatform(randint(-100, 450), randint(0, 640)))
        self.score_sprite = TextSprite(50,25,self.doodle.name, 45, (0,0,0))
        self.allsprites.add(self.score_sprite)
        self.header = Header()
        self.window.blit(self.background, (0, 0))
    
    
    def randomPlatform(self, x , y):
        dig = randint(0, 100)
        if dig < 35:
            return MovingPlatform(x,y)
        elif dig >= 35 and dig < 50:
            return CrashingPlatform(x,y)
        else:
            return Platform(x,y)
    
    def draw(self):
        if self.doodle.alive == 1:
            self.allsprites.clear(self.window, self.background)
            # doodler jumps
            mousePos = pygame.mouse.get_pos()
            self.doodle.incYSpeed(-self.gravitation)
            self.doodle.setX(mousePos[0])
            self.doodle.moveY(-self.doodle.ySpeed)
            for spr in self.allsprites:
                # if platform under legs
                if isinstance(spr, Platform) and self.doodle.getLegsRect().colliderect(spr.getSurfaceRect()) and self.doodle.ySpeed <= 0:
                    if isinstance(spr,CrashingPlatform):
                        spr.crash()
                        break
                    self.doodle.ySpeed = 10
            
                if isinstance(spr, Platform):
                    # renew platforms
                    if spr.y >= 640:
                        spr.renew()

                
                # move blue and crashed platforms
                if isinstance(spr,MovingPlatform) or (isinstance(spr,CrashingPlatform) and spr.crashed == 1):
                    spr.move()
            
            # moving whole world    
            if self.doodle.y < 300:
                self.doodle.incScore(self.doodle.ySpeed)
                for spr in self.allsprites:
                    if not isinstance(spr, TextSprite):
                        spr.moveY(self.doodle.ySpeed)
            
            
            #draw all on canvas
            self.allsprites.draw(self.window) 
            self.score_sprite.setText("               %s,    %s" % (self.doodle.name, int(self.doodle.score/10)))
            self.window.blit(self.header, (0,0))
        else:
            #if dead - load exit location
            self.parent.location = GameLocation(self.parent,self.doodle.name)

    def event(self,event):
        if event.type == KEYDOWN:
            print event.key
            



# game stats and exit location
class ExitLocation(Location):
    def __init__(self, parent, name, score):
        Location.__init__(self, parent)
        self.background = pygame.image.load('img/background.png')
        print "Exiting"
