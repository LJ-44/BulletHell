import pygame
import pygame.freetype
from pygame.locals import *
from pygame.sprite import Sprite, Group
from enum import Enum, auto
from abc import ABC, abstractmethod
from typing import Optional, Tuple, Union, List, Dict, Any
import src.sprites as sprite

class GameStateID(Enum):
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
    
def create_surface(
    size: Tuple[int, int],
    color: Optional[str] = "red",
    alpha: bool = False
) -> pygame.Surface:
    
    surface = pygame.Surface(size, pygame.SRCALPHA if alpha else 0)
    if color:
        surface.fill(color)
    return surface.convert_alpha() if alpha else surface.convert()

def create_surface_with_text(text: str, 
                             font_size: int, 
                             text_color: pygame.Color, 
                             font_path="assets/font/BulletHell_font.ttf"
                        )->pygame.Surface:
    font = pygame.freetype.Font(file=font_path, size=font_size)
    surface, _ = font.render(text=text, fgcolor=text_color)
    return surface.convert_alpha()

class UIElement(Sprite):
    def __init__(self, position, text, font_size, text_color):
        super().__init__()

class GameState(ABC):
    
    def __init__(self, manager):
        self.manager = manager  # Reference to state manager
        self.screen = pygame.display.get_surface()
        self.ui_elements = Group()
    
    @abstractmethod
    def handle_events(self, events): pass
    
    @abstractmethod
    def update(self, dt): pass
    
    @abstractmethod
    def draw(self, screen): pass
    
    
class MainMenu(GameState):
    
    def __init__(self, manager):
        super().__init__(manager)
    
    def handle_events(self, events): pass
    
    def update(self, dt): pass 
        
    def draw(self, screen): pass
        
class GamePlay(GameState):
    
    def __init__(self, manager):
        super().__init__(manager)
    
    def handle_events(self, events): pass
    
    def update(self, dt): pass
        
    def draw(self, screen): pass
        
class Settings(GameState):
    
    def __init__(self, manager):
        super().__init__(manager)
    
    def handle_events(self, events): pass
    
    def update(self, dt): pass
        
    def draw(self, screen): pass
    ...
class ChooseDifficulty(GameState):
    
    def __init__(self, manager):
        super().__init__(manager)
    
    def handle_events(self, events): pass
    
    def update(self, dt): pass
        
    def draw(self, screen): pass
    ...

class Paused(GameState):
    
    def __init__(self, manager):
        super().__init__(manager)
    
    def handle_events(self, events): pass
    
    def update(self, dt): pass
        
    def draw(self, screen): pass
    ...
class GameOver(GameState):
    
    def __init__(self, manager):
        super().__init__(manager)
    
    def handle_events(self, events): pass
    
    def update(self, dt): pass
        
    def draw(self, screen): pass
    ...
    
class StateManager:
    def __init__(self):
        self.states = {
            GameStateID.MAIN_MENU: MainMenu(self),
            GameStateID.SETTINGS: Settings(self),
            GameStateID.CHOOSE_DIFFICULTY: ChooseDifficulty(self),
            GameStateID.GAMEPLAY: GamePlay(self),
            GameStateID.PAUSED: Paused(self),
            GameStateID.GAME_OVER: GameOver(self),
            GameStateID.QUIT: GameStateID.QUIT
        }
        
        self.current_state = self.states[GameStateID.MAIN_MENU]
        self.player_mode = None
        self.difficulty = None
    
    def change_state(self, new_state):
        if new_state == GameStateID.QUIT:
            return False
        
        self.current_state = self.states[new_state]
        return True
        
    def handle_events(self, event):
        result = self.current_state.handle_events(event)
        if result:
            return self.change_state(result)
        return True
    
    def update(self, dt): pass
    
    def draw(self, screen): pass
        

# pygame.init()
# monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]
# screen = pygame.display.set_mode((500, 500), RESIZABLE)
# clock = pygame.time.Clock()
# #pic = pygame.image.load("assets/images/megaman.png")  # You need an example picture in the same folder as this file!

# fullscreen = False
# running = True
# while running:
    
#     screen.fill('blue')
    
#     pygame.draw.rect(surface=screen,
#                      color='black',
#                      rect=pygame.Rect((screen.get_width() / 2, screen.get_height() / 2), (10, 10)))
    
#     pygame.event.pump()
#     event = pygame.event.wait()
#     if event.type == QUIT:
#         running = False
#     elif event.type == KEYDOWN:
#         if event.key == K_ESCAPE:
#             running = False
#         elif event.key == K_f:
#             fullscreen = not fullscreen
#             if fullscreen:
#                 screen = pygame.display.set_mode(monitor_size, FULLSCREEN)
#             else:
#                 screen = pygame.display.set_mode((screen.get_width(), screen.get_height()), RESIZABLE)
#     elif event.type == VIDEORESIZE:
#         if not fullscreen:
#             screen = pygame.display.set_mode((event.w, event.h), RESIZABLE)
        
#     pygame.display.update()
#     clock.tick(60)
        
# pygame.quit()
        