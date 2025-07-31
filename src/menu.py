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
    
    def update(self, mouse_pos, mouse_up):
        if self.rect.collidepoint(mouse_pos):
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
    GAME_OVER = auto()
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

class MusicVolumeSlider(Sprite):
    def __init__(self,
                 center_pos, 
                 slider_width: int = 200, 
                 slider_height: int = 20, 
                 handle_width: int = 10, 
                 handle_height:int = 30, 
                 current_volume: float = 0.5,
                 min_volume: float = 0.0,
                 max_volume: float = 1.0):
        super().__init__()
        
        self.slider_width = slider_width
        self.slider_height = slider_height
        self.handle_width = handle_width
        self.handle_height = handle_height
        self.current_volume = current_volume
        self.min_volume = min_volume
        self.max_volume = max_volume
        self.dragging_slider = False
        
        self.slider = pygame.Surface((slider_width, slider_height))
        self.slider.fill((200,0,0))
        
        self.handle = pygame.Surface((handle_width, handle_height))
        self.handle.fill((255,0,0))
        
        self.image = pygame.Surface((slider_width, handle_height)).convert_alpha()
        self.image.blit(self.slider, (0, (handle_height - slider_height) // 2))
        
        self.update_handle_pos()
        
        self.rect = self.image.get_rect(center=center_pos)
        
    def update_handle_pos(self):
        handle_xpos = int((self.current_volume - self.min_volume) / 
                          (self.max_volume - self.min_volume) * 
                          (self.slider_width - self.handle_width))
        
        self.image.fill((0,0,0,0))
        self.image.blit(self.slider, (0, (self.handle_height - self.slider_height) // 2))
        self.image.blit(self.handle, (handle_xpos, 0))
        
    def update(self, mouse_pos, mouse_clicked):
        
        if not self.dragging_slider and mouse_clicked:
            
            handle_xpos = int((self.current_volume - self.min_volume) / 
                          (self.max_volume - self.min_volume) * 
                          (self.rect.width - self.handle_width))
            
            handle_rect = pygame.Rect(self.rect.x + handle_xpos,
                                  self.rect.y,
                                  self.handle_width,
                                  self.handle_height)
            
            if handle_rect.collidepoint(mouse_pos):
                self.dragging_slider = True
            ...
        if self.dragging_slider:
            relative_xpos = mouse_pos[0] - self.rect.x
            self.current_volume = (relative_xpos / self.rect.width) * (self.max_volume - self.min_volume) + self.min_volume
            
            self.current_volume = max(self.min_volume, min(self.max_volume, self.current_volume))
            pygame.mixer.music.set_volume(self.current_volume)
            self.update_handle_pos()
            
        if not mouse_clicked:
            self.dragging_slider = False
        
    def draw(self, surface):
        surface.blit(self.image, self.rect)
        
    def get_volume(self):
        return int(self.current_volume * 100)
class SfxVolumeSlider(Sprite):
    
    def __init__(self,
                 center_pos, 
                 slider_width: int = 200, 
                 slider_height: int = 20, 
                 handle_width: int = 10, 
                 handle_height:int = 30, 
                 current_volume: float = 0.5,
                 min_volume: float = 0.0,
                 max_volume: float = 1.0):
        super().__init__()
        
        from src.sound import set_sfx_volume
        self.set_sfx_volume = set_sfx_volume
        
        self.slider_width = slider_width
        self.slider_height = slider_height
        self.handle_width = handle_width
        self.handle_height = handle_height
        self.current_volume = current_volume
        self.min_volume = min_volume
        self.max_volume = max_volume
        self.dragging_slider = False
        
        self.slider = pygame.Surface((slider_width, slider_height))
        self.slider.fill((200,0,0))
        
        self.handle = pygame.Surface((handle_width, handle_height))
        self.handle.fill((255,0,0))
        
        self.image = pygame.Surface((slider_width, handle_height)).convert_alpha()
        self.image.blit(self.slider, (0, (handle_height - slider_height) // 2))
        
        self.update_handle_pos()
        
        self.rect = self.image.get_rect(center=center_pos)
        
    def update_handle_pos(self):
        handle_xpos = int((self.current_volume - self.min_volume) / 
                          (self.max_volume - self.min_volume) * 
                          (self.slider_width - self.handle_width))
        
        self.image.fill((0,0,0,0))
        self.image.blit(self.slider, (0, (self.handle_height - self.slider_height) // 2))
        self.image.blit(self.handle, (handle_xpos, 0))
        
    def update(self, mouse_pos, mouse_clicked):
        
        if not self.dragging_slider and mouse_clicked:
            
            handle_xpos = int((self.current_volume - self.min_volume) / 
                          (self.max_volume - self.min_volume) * 
                          (self.rect.width - self.handle_width))
            
            handle_rect = pygame.Rect(self.rect.x + handle_xpos,
                                  self.rect.y,
                                  self.handle_width,
                                  self.handle_height)
            
            if handle_rect.collidepoint(mouse_pos):
                self.dragging_slider = True
            ...
        if self.dragging_slider:
            relative_xpos = mouse_pos[0] - self.rect.x
            self.current_volume = (relative_xpos / self.rect.width) * (self.max_volume - self.min_volume) + self.min_volume
            
            self.current_volume = max(self.min_volume, min(self.max_volume, self.current_volume))
            self.set_sfx_volume(self.current_volume)
            self.update_handle_pos()
            
        if not mouse_clicked:
            self.dragging_slider = False
        
    def draw(self, surface):
        surface.blit(self.image, self.rect) 
        
    def get_volume(self):
        return int(self.current_volume * 100)

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
                                             ],
                                             other_ui_specs=[
                                                 {   
                                                     "center_position": (screen_width / 2 , screen_height * 0.56),
                                                     "text": "Music Volume",
                                                     "action": None #TODO: figure this out
                                                 },
                                                 {
                                                     "center_position": (screen_width / 2 , screen_height * 0.67),
                                                     "text": "Sfx Volume",
                                                     "action": None #TODO: figure this out
                                                 },
                                                 {
                                                     "center_position": (screen_width * 0.13 , screen_height * 0.94),
                                                     "text": "Back to Main Menu",
                                                     "action": GameState.MAIN_MENU
                                                 }
                                             ])
        
        self.music_volume_slider = MusicVolumeSlider(center_pos=(screen_width / 2, screen_height * 0.615))
        self.sfx_volume_slider = SfxVolumeSlider(center_pos = (screen_width / 2, screen_height * 0.725))
        
class GameOverScreen:
    def __init__(self):
        screen = pygame.display.get_surface()
        screen_height = screen.get_height()
        screen_center_x = screen.get_width() / 2
        
        title_position = (screen_center_x, screen_height * 0.25)
        
        self.title_card = UIElement(
            center_position=(title_position),
            text="GAME OVER",
            font_size=50,
            text_rgb=(255,0,0),
            action=None
        )
        
        self.ui_elements = build_ui_elements(screen=screen,
                                             spaced_ui_specs=[
                                                 {
                                                     "text":"TRY AGAIN?",
                                                     "action": PlayerMode.ONE_PLAYER #TODO: fix for two player
                                                 },
                                                 {
                                                     "text":"MAIN MENU",
                                                     "action": GameState.MAIN_MENU
                                                 },
                                                 {
                                                     "text": "QUIT GAME",
                                                     "action": GameState.QUIT
                                                 }
                                             ])