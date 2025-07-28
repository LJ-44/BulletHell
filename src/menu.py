import pygame
import pygame.freetype
from pygame.sprite import Sprite
from pygame.rect import Rect
from enum import Enum, auto
from typing import Optional, Any

def create_surface_with_text(text, font_size, text_rgb, font_path="assets/font/BulletHell_font.ttf"):
    font = pygame.freetype.Font(file=font_path, size=font_size)
    surface, _ = font.render(text=text, fgcolor=text_rgb)
    return surface.convert_alpha()

class UIElement(Sprite):
    def __init__(self, center_position, text, font_size, text_rgb, action=None):
        
        super().__init__()
        
        self.mouse_over = False
        
        default_image = create_surface_with_text(text=text, font_size=font_size, text_rgb=text_rgb)
        highlighted_image = create_surface_with_text(text=text, font_size=font_size * 1.2, text_rgb=(200,0,0))
        
        self.images = [default_image, highlighted_image]
        self.rects = [
            default_image.get_rect(center=center_position),
            highlighted_image.get_rect(center=center_position)
        ]
        
        self.action = action
        
    @property
    def image(self):
        # highlight element if mouse over
        return self.images[1] if self.mouse_over else self.images[0]
    
    @property
    def rect(self):
        # highlight element if mouse over
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
        
def build_ui_elements(screen: pygame.Surface, 
                      spaced_ui_specs: list[dict[str, Any]],
                      title_card: Optional[UIElement] = None, 
                      other_ui_specs: Optional[list[dict[str, Any]]] = None
                      ) -> list[UIElement]:
    
    screen_height = screen.get_height()
    screen_center_x = screen.get_width() / 2

    elements = [title_card]
    
    top_button_y = screen_height * 0.45
    ui_element_spacing = 40 # pixels
    
    for idx, spaced_specs in enumerate(spaced_ui_specs):
            spaced_uielement_pos = (screen_center_x, top_button_y + (idx * ui_element_spacing))
            
            spaced_ui_element = UIElement(
                center_position=spaced_uielement_pos,
                font_size=30,
                text_rgb=(255,0,0),
                **spaced_specs
            )
            elements.append(spaced_ui_element)

    if other_ui_specs is not None:
        for idx, other_specs in enumerate(other_ui_specs):
            
            other_ui_element = UIElement(
                font_size=30,
                text_rgb=(255,0,0),
                **other_specs
            )
            elements.append(other_ui_element)

    return elements
            
class GameState(Enum):
    MAIN_MENU = auto()
    GAMEPLAY = auto()
    CHOOSE_DIFFICULTY = auto()
    SETTINGS = auto()
    PAUSED = auto()
    QUIT = auto()

class PlayerMode(Enum):
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
        
        screen = pygame.display.get_surface()
        screen_height = screen.get_height()
        screen_center_x = screen.get_width() / 2
        
        self.title_card = UIElement(
            center_position=(screen_center_x, screen_height * 0.25),
            text="BULLET HELL",
            text_rgb=(255,0,0),
            font_size=75,
            action=None
        )
        
        self.ui_elements = build_ui_elements(screen=screen, 
                                             title_card=self.title_card, 
                                             spaced_ui_specs=[
            {
                "text":"ONE PLAYER MODE",
                "action": PlayerMode.ONE_PLAYER
            },
            {
                "text":"TWO PLAYER MODE",
                "action": PlayerMode.TWO_PLAYER
            },
            {
                "text":"SETTINGS",
                "action": GameState.SETTINGS
            },
            {
                "text":"QUIT",
                "action": GameState.QUIT
            }
                                             ])
            
class PauseScreen:
    def __init__(self):
        
        screen = pygame.display.get_surface()
        screen_height = screen.get_height()
        screen_center_x = screen.get_width() / 2

        title_position = (screen_center_x, screen_height * 0.25)
        
        self.paused_title = UIElement(
            center_position=(title_position),
            text="GAME PAUSED",
            text_rgb=(255,0,0),
            font_size=50,
            action=None
        )
        
        self.ui_elements = build_ui_elements(screen=screen,
                                             title_card=self.paused_title,
                                             spaced_ui_specs=[
                {
                    "text":"CONTINUE",
                    "action": GameState.GAMEPLAY
                },
                {
                    "text":"MAIN MENU",
                    "action": GameState.MAIN_MENU
                },
                {
                    "text":"QUIT GAME",
                    "action": GameState.QUIT
                }
                                             ])
        
class DifficultyScreen:
    def __init__(self):
        
        screen = pygame.display.get_surface()
        screen_height = screen.get_height()
        screen_center_x = screen.get_width() / 2
        
        title_position = (screen_center_x, screen_height * 0.25)
        
        self.title_card = UIElement(
            center_position=(title_position),
            text="CHOOSE DIFFICULTY",
            text_rgb=(255,0,0),
            font_size=50,
            action=None
        )
        
        self.ui_elements = build_ui_elements(screen=screen,
                                        title_card=self.title_card,
                                        spaced_ui_specs=[
                {
                    "text":"EASY",
                    "action": Difficulty.EASY
                },
                {
                    "text":"MEDIUM",
                    "action": Difficulty.MEDIUM
                },
                {
                    "text":"HARD",
                    "action": Difficulty.HARD
                },
                {
                    "text":"INSANE",
                    "action": Difficulty.INSANE
                },
                {
                    "text":"HELL",
                    "action": Difficulty.HELL
                }
                                        ])
        
class SettingsScreen:
    def __init__(self):

        screen = pygame.display.get_surface()
        screen_height = screen.get_height()
        screen_width = screen.get_width()
        screen_center_x = screen.get_width() / 2

        title_position = (screen_center_x, screen_height * 0.25)

        self.title_card = UIElement(
            center_position=(title_position),
            text="SETTINGS",
            text_rgb=(255,0,0),
            font_size=50,
            action=None
        )

        self.ui_elements = build_ui_elements(screen=screen,
                                             title_card=self.title_card,
                                             spaced_ui_specs=[
                                                 {
                                                     "text": "Full Screen",
                                                     "action": None #TODO: figure this out
                                                 },
                                                 {
                                                     "text": "Windowed",
                                                     "action": None #TODO: figure this out
                                                 },
                                                 {
                                                     "text": "Music",
                                                     "action": None #TODO: figure this out
                                                 },
                                                 {
                                                     "text": "Sound Effects",
                                                     "action": None #TODO: figure this out
                                                 }
                                             ],
                                             other_ui_specs=[
                                                 {
                                                     "center_position": (screen_width * 0.1 , screen_height * 0.9),
                                                     "text": "Back to Main Menu",
                                                     "action": GameState.MAIN_MENU
                                                 }
                                             ])