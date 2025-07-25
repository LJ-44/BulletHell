import pygame
import pygame.freetype
from pygame.sprite import Sprite
from pygame.rect import Rect
from enum import Enum, auto

def create_surface_with_text(text, font_size, text_rgb, background_rgb):
    font = pygame.freetype.SysFont(name="Courier", size=font_size, bold=True)
    surface, _ = font.render(text=text, fgcolor=text_rgb, bgcolor=background_rgb)
    return surface.convert_alpha()

class UIElement(Sprite):
    def __init__(self, center_position, text, font_size, background_rgb, text_rgb, action=None):
        
        super().__init__()
        
        self.mouse_over = False
        
        default_image = create_surface_with_text(text, font_size, text_rgb, background_rgb)
        
        highlighted_image = create_surface_with_text(text, font_size * 1.2, text_rgb, background_rgb)
        
        self.images = [default_image, highlighted_image]
        self.rects = [
            default_image.get_rect(center=center_position),
            highlighted_image.get_rect(center=center_position)
        ]
        
        self.action = action
        
    @property
    def image(self):
        return self.images[1] if self.mouse_over else self.images[0]
    
    @property
    def rect(self):
        return self.rects[1] if self.mouse_over else self.rects[0]
    
    def update(self, mouse_position, mouse_up):
        if self.rect.collidepoint(mouse_position):
            self.mouse_over = True
            if mouse_up:
                return self.action
        else: 
            self.mouse_over = False
            
    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, self.rect)
            
class GameState(Enum):
    MAIN_MENU = auto()
    GAMEPLAY = auto()
    SETTINGS = auto()
    PAUSED = auto()
    QUIT = auto()

class PlayerState(Enum):
    ONE_PLAYER = auto()
    TWO_PLAYER = auto()
    
class Difficulty(Enum):
    EASY = auto()
    MEDIUM = auto()
    HARD = auto()
    INSANE = auto()
    HELL = auto()

class MainMenu:
    def __init__(self):
        
        self.screen = pygame.display.get_surface()
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()
        self.screen_middle_x = self.screen_width / 2
        
        self.title_card_position = (self.screen_middle_x, (self.screen_height * (0.15)))
        self.singleplayer_button_position = (self.screen_middle_x, (self.screen_height * (0.3)))
        self.two_player_button_position = (self.screen_middle_x, (self.screen_height * (0.45)))
        self.settings_button_position = (self.screen_middle_x, (self.screen_height * (0.6)))
        self.quit_button_position = (self.screen_middle_x, (self.screen_height * (0.75)))
        
        self.title_card = UIElement(
            center_position=(self.title_card_position),
            font_size=30,
            background_rgb=(0,0,0),
            text_rgb=(255,0,0),
            text="Bullet Hell",
            action=None
        )
        
        self.singleplayer_button = UIElement(
            center_position=(self.singleplayer_button_position),
            font_size=30,
            background_rgb=(0,0,0),
            text_rgb=(255,0,0),
            text="Single Player",
            action=GameState.GAMEPLAY
        )

        self.two_player_button = UIElement(
            center_position=(self.two_player_button_position),
            font_size=30,
            background_rgb=(0,0,0),
            text_rgb=(255,0,0),
            text="Two Player",
            action=GameState.GAMEPLAY
        )
        
        self.settings_button = UIElement(
            center_position=(self.settings_button_position),
            font_size=30,
            background_rgb=(0,0,0),
            text_rgb=(255,0,0),
            text="Settings",
            action=GameState.SETTINGS
        )
        
        self.quit_button = UIElement(
            center_position=(self.quit_button_position),
            font_size=30,
            background_rgb=(0,0,0),
            text_rgb=(255,0,0),
            text="Exit",
            action=GameState.QUIT
        )
        
        self.buttons = [self.title_card, self.singleplayer_button, self.two_player_button, self.settings_button, self.quit_button]
            
    
    