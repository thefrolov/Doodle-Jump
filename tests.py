" Module Tests "
# -*- coding: utf-8 -*-
import unittest
from sprites import *

class TestSprite(unittest.TestCase):

    def setUp(self):
        pygame.init()
        window = pygame.display.set_mode((screen_width, screen_height))
    
    
    def test_sprite_creation(self):
        sprite = Sprite(0,0)
        self.assertEqual('Sprite', type(sprite).__name__)
    
    
    
    def test_moving_x(self):
        
        sprite = Monster(0,0)
        sprite.move_x(5)
        self.assertEqual(5, sprite.x)
        
    def test_moving_y(self):        
        sprite = Monster(0,0)
        sprite.move_y(15)
        self.assertEqual(15, sprite.y)
        
        
    def test_image_initialisation(self):
        sprite = Monster(0,0)
        self.assertFalse(sprite.image == None)