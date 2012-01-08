# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
from sprites import Doodle, Platform, MovingPlatform, CrashingPlatform, Rectangle, Button, TextSprite, Spring, Monster
import sys
from random import randint
import inputbox

from config import *

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
        pygame.key.set_repeat(0)
        self.startbtn = Button(240, 200, "Start")
        self.exitbtn = Button(240, 270, "Exit")
        self.controls = pygame.sprite.Group()
        self.surfaces = []
        self.controls_captions = pygame.sprite.Group()
        self.controls_captions.add(self.startbtn.textSprite)
        self.controls_captions.add(self.exitbtn.textSprite)
        self.controls.add(self.startbtn)
        self.controls.add(self.exitbtn)
        self.window.blit(self.background, (0, 0))
        
    def draw(self):
        self.controls.clear(self.window, self.background)
        self.controls.draw(self.window)
        self.controls_captions.draw(self.window)
    
    def event(self,event):
        if event.type == MOUSEMOTION:
            for btn in self.controls:
                if btn.rect.collidepoint(pygame.mouse.get_pos()):
                #pass
                    btn.changeState(1)
                else:
                #pass
                    btn.changeState(0)
        elif event.type == MOUSEBUTTONUP:
            if self.startbtn.rect.collidepoint(pygame.mouse.get_pos()):
                name = inputbox.ask(self.window, "Your name")
                if name:
                    self.parent.location = GameLocation(self.parent, name)
            elif self.exitbtn.rect.collidepoint(pygame.mouse.get_pos()):
                sys.exit()
    
    def showInput(self):
        self.input_surf = Rectangle(300, 100, (0,191,255,200))
        self.surfaces.append(self.input_surf)   




# gameplay location
class GameLocation(Location):
    
    def __init__(self, parent, name):
        Location.__init__(self, parent)
        pygame.key.set_repeat(10)
        pygame.mouse.set_visible(0)
        self.doodle = Doodle(name)
        self.doodle.name = name
        self.allsprites = pygame.sprite.Group()
        self.allsprites.add(self.doodle)
        for i in range(0, platform_count):
            self.allsprites.add(self.randomPlatform(False))
        for platform in self.allsprites:
            if isinstance(platform, Platform) and platform.spring != None:
                self.allsprites.add(platform.spring)

        self.score_sprite = TextSprite(50,25,self.doodle.name, 45, (0,0,0))
        self.allsprites.add(self.score_sprite)
        self.header = Rectangle(screen_width, 50, (0,191,255,128))
        self.window.blit(self.background, (0, 0))
        
        self.monster = None
    
    
    def randomPlatform(self,top = True):
        x = randint(0, screen_width - platform_width)
        bad_y = []
        for spr in self.allsprites:
            bad_y.append((spr.y-platform_y_padding, spr.y + platform_y_padding + spr.rect.height))
        
        good = 0
        while not good:
            if top:
               y = randint(-100, 50)
            else:
                y = randint(0, screen_height)
            good = 1
            for bad_y_item in bad_y:
                if bad_y_item[0] <= y <= bad_y_item[1]:
                    good = 0
                    break
            
        dig = randint(0, 100)
        if dig < 35:
            return MovingPlatform(x,y)
        elif dig >= 35 and dig < 50:
            return CrashingPlatform(x,y)
        else:
            return Platform(x,y)
    
    
    
    def draw(self):
        if self.doodle.alive == 1:
            # create monster
            if self.monster == None:
                case = randint(-1000,5)
                if case > 0:
                    self.monster = Monster(randint(0, screen_width), randint(-50, 50))
                    self.allsprites.add(self.monster)
                    self.monster.move()
            else:
                self.monster.move()
                # touch monster
                if self.doodle.rect.colliderect(self.monster.rect):
                    self.doodle.alive = 0
                if self.monster.y >= screen_height:
                    self.allsprites.remove(self.monster)
                    self.monster = None
                    
            self.allsprites.clear(self.window, self.background)
            
            # doodler jumps
            mousePos = pygame.mouse.get_pos()
            self.doodle.inc_y_speed(-gravitation)
            if mouse_enabled:
                self.doodle.set_x(mousePos[0])
            else:
                if transparent_walls:
                    if self.doodle.x < 0:
                        self.doodle.set_x(screen_width)
                    elif self.doodle.x > screen_width:
                        self.doodle.set_x(0)
            self.doodle.move_y(-self.doodle.ySpeed)
            for spr in self.allsprites:
                # if spring  under legs
                if isinstance(spr, Spring) and self.doodle.get_legs_rect().colliderect(spr.get_top_surface()) and self.doodle.ySpeed <= 0:
                    spr.compress()
                    self.doodle.ySpeed = spring_speed
                
                # if platform under legs
                if isinstance(spr, Platform) and self.doodle.get_legs_rect().colliderect(spr.get_surface_rect()) and self.doodle.ySpeed <= 0:
                    if isinstance(spr,CrashingPlatform):
                        spr.crash()
                        break
                    self.doodle.ySpeed = jump_speed
            
                if isinstance(spr, Platform):
                    # renew platforms
                    if spr.y >= screen_height:
                        self.allsprites.remove(spr)
                        platform = self.randomPlatform()
                        self.allsprites.add(platform)
                        if isinstance(platform, Platform) and platform.spring != None:
                            self.allsprites.add(platform.spring)

                
                # move blue and crashed platforms
                if isinstance(spr,MovingPlatform) or (isinstance(spr,CrashingPlatform) and spr.crashed == 1):
                    spr.move()
            
            # moving whole world    
            if self.doodle.y < horizont:
                self.doodle.inc_score(self.doodle.ySpeed)
                for spr in self.allsprites:
                    if not isinstance(spr, TextSprite):
                        spr.move_y(self.doodle.ySpeed)
            
            
            #draw all on canvas
            self.allsprites.draw(self.window)
            self.score_sprite.setText("               %s,    %s" % (self.doodle.name, int(self.doodle.score/10)))
            self.window.blit(self.header, (0,0))
        else:
            #if dead - load exit location
            self.parent.location = GameLocation(self.parent,self.doodle.name)

    def event(self,event):
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                self.doodle.set_x(self.doodle.x - 10)
            elif event.key == K_RIGHT:
                self.doodle.set_x(self.doodle.x + 10)
            

# game stats and exit location
class ExitLocation(Location):
    def __init__(self, parent, name, score):
        Location.__init__(self, parent)
        self.background = pygame.image.load('img/background.png')
        print "Exiting"
