import pygame
import pygame.freetype
from pygame.sprite import Sprite
from pygame.rect import Rect
from enum import Enum, auto

def create_surface_with_text(text, font_size, text_rgb, background_rgb):
    font = pygame.freetype.SysFont(name="courier", size=font_size, bold=True)
    surface, _ = font.render(text=text, fgcolor=text_rgb, bgcolor=background_rgb)
    return surface.convert_alpha()
class UIElement(Sprite):
    def __init__(self, center_position, text, font_size, background_rgb, text_rgb, action=None):
        
        super().__init__()
        
        self.mouse_over = False
        
        default_image = create_surface_with_text(text, font_size, text_rgb, background_rgb)
        
        highlighted_image = create_surface_with_text(text, font_size * 1.2, text_rgb=(200,0,0), background_rgb=background_rgb)
        
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
        
def build_ui_elements(screen: pygame.Surface, title_card: UIElement | None, ui_specs: list[dict[str, any]]):
    
    screen_height = screen.get_height()
    screen_center_x = screen.get_width() / 2

    elements = [title_card]
    
    top_button_y = screen_height * 0.35
    ui_element_spacing = 30 # pixels
    
    for idx, specs in enumerate(ui_specs):
            uielement_pos = (screen_center_x, top_button_y + (idx * ui_element_spacing))
            
            ui_element = UIElement(
                center_position=uielement_pos,
                font_size=30,
                background_rgb=(0,0,0),
                text_rgb=(255,0,0),
                **specs
            )
            elements.append(ui_element)
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
            center_position=(screen_center_x, screen_height * 0.1),
            text="BULLET HELL",
            text_rgb=(255,0,0),
            font_size=60,
            background_rgb=(0,0,0),
            action=None
        )
        
        self.ui_elements = build_ui_elements(screen=screen, 
                                             title_card=self.title_card, 
                                             ui_specs=[
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
        
        self.paused_title = UIElement(
            center_position=(screen_center_x, screen_height * 0.1),
            text="GAME PAUSED",
            text_rgb=(255,0,0),
            font_size=50,
            background_rgb=(0,0,0),
            action=None
        )
        
        self.ui_elements = build_ui_elements(screen=screen,
                                             title_card=self.paused_title,
                                             ui_specs=[
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
        
        title_position = screen_height * 0.1
        
        self.title_card = UIElement(
            center_position=(screen_center_x, title_position),
            text="CHOOSE DIFFICULTY",
            text_rgb=(255,0,0),
            font_size=50,
            background_rgb=(0,0,0),
            action=None
        )
        
        self.ui_elements = build_ui_elements(screen=screen,
                                        title_card=self.title_card,
                                        ui_specs=[
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