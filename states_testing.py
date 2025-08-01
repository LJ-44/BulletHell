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

def create_surface_with_text(text: str, 
                             font_size: int, 
                             text_color: pygame.Color, 
                             font_path="assets/font/BulletHell_font.ttf"
)->pygame.Surface:
    
    font = pygame.freetype.Font(file=font_path, size=font_size)
    surface, _ = font.render(text=text, fgcolor=text_color)
    return surface.convert_alpha()

class UIElement(Sprite):
    def __init__(self,
                 relative_pos: Tuple[float, float],
                 text: str,
                 base_font_size: int,
                 text_color: Tuple[int, int, int] = (255,0,0),
                 highlight_color: Tuple[int, int, int] = (200,0,0),
                 highlight_scale: float = 1.2,
                 action: Optional[Any] = None,
                 reference_resolution: Tuple[int, int] = (1280, 720)):
        super().__init__()
        
        #visual states
        self.relative_pos = relative_pos
        self.reference_res = reference_resolution
        self.base_font_size = base_font_size
        self.text = text
        self.text_color = text_color
        self.highlight_color = highlight_color
        self.highlight_scale = highlight_scale
        self.is_highlighted = False
        self.action = action
        
        self.create_surfaces()
        
        self.rect = self.normal_surface.get_rect(center=relative_pos)
        self.is_clickable = True
        ...
        
    def get_scale_factor(self):
        current_res = pygame.display.get_surface().get_size()
        return current_res[0] / self.reference_res[0]
        ...
        
    def create_surfaces(self):
        
        scale = self.get_scale_factor()
        
        self.normal_surface = create_surface_with_text(
            text=self.text,
            font_size=int(self.base_font_size * scale),
            text_color=self.text_color
        )
        
        self.highlighted_surface = create_surface_with_text(
            text=self.text,
            font_size=int(self.base_font_size * scale * self.highlight_scale),
            text_color=self.text_color
        )
        
        self.image = self.normal_surface
        self.update_position()
        
    def update_position(self):
        screen_width, screen_height = pygame.display.get_surface().get_size()
        x_pos = self.relative_pos[0] * screen_width
        y_pos = self.relative_pos[1] * screen_height
        self.rect = self.image.get_rect(center=(x_pos, y_pos))
        ...
        
    def handle_resize(self):
        self.create_surfaces()
        ...
    
    def update(self, mouse_pos, mouse_up):
        
        if not self.is_clickable:
            return None
        
        self.is_highlighted = self.rect.collidepoint(mouse_pos)
        self.image = self.highlighted_surface if self.is_highlighted else self.normal_surface
        
        if self.is_highlighted and mouse_up:
            return self.action
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        ...
        
    def disable(self):
        self.is_clickable = False
        self.is_highlighted = False
        self.image = self.normal_surface
        ...
        
    def enable(self):
        self.is_clickable = True
        ...
        
    @property
    def is_highlighted(self):
        return self.is_highlighted and self.is_clickable
class GameState(ABC):
    
    def __init__(self, manager):
        self.manager = manager  # Reference to state manager
        self.screen = pygame.display.get_surface()
        self.ui_elements = Group()
    
    @abstractmethod
    def handle_events(self, events): pass
    
    @abstractmethod
    def update(self): pass
    
    @abstractmethod
    def draw(self, screen): pass
    
    
class MainMenu(GameState):
    
    def __init__(self, manager):
        super().__init__(manager)
        
        self.ui_elements = [
            UIElement(
                relative_pos=(0.5, 0.3),
                text="Bullet Hell",
                base_font_size=50,
                action=None
            ),
            UIElement(
                relative_pos=(0.5, 0.3),
                text="ONE PLAYER MODE",
                base_font_size=30,
                action=(PlayerMode.ONE_PLAYER, GameStateID.CHOOSE_DIFFICULTY)
            ),
            UIElement(
                relative_pos=(0.5, 0.3),
                text="TWO PLAYER MODE",
                base_font_size=30,
                action=(PlayerMode.TWO_PLAYER, GameStateID.CHOOSE_DIFFICULTY)
            ),
            UIElement(
                relative_pos=(0.5, 0.3),
                text="SETTINGS",
                base_font_size=30,
                action=GameStateID.SETTINGS
            ),
            UIElement(
                relative_pos=(0.5, 0.3),
                text="EXIT",
                base_font_size=30,
                action=GameStateID.QUIT
            )
        ]
        
        for element in self.ui_elements:
            self.ui_elements.add(element)
    
    def handle_events(self, events):
        mouse_pos = pygame.mouse.get_pos()
        mouse_up = any(event.type == pygame.MOUSEBUTTONUP and event.button == 1 for event in events)
        
        for element in self.ui_elements:
            action = element.update(mouse_pos, mouse_up)
            if action:
                if isinstance(action, tuple):
                    self.manager.player_mode = action[0]
                    return action[1]
                return action
        return None
    
    def update(self): pass 
        
    def draw(self, screen):
        self.ui_elements.draw(screen)
        
class GamePlay(GameState):
    
    def __init__(self, manager):
        super().__init__(manager)
    
    def handle_events(self, events): pass
    
    def update(self): pass
        
    def draw(self, screen): pass
        
class Settings(GameState):
    
    def __init__(self, manager):
        super().__init__(manager)
    
    def handle_events(self, events): pass
    
    def update(self): pass
        
    def draw(self, screen): pass
    ...
class ChooseDifficulty(GameState):
    
    def __init__(self, manager):
        super().__init__(manager)
    
    def handle_events(self, events): pass
    
    def update(self): pass
        
    def draw(self, screen): pass
    ...

class Paused(GameState):
    
    def __init__(self, manager):
        super().__init__(manager)
    
    def handle_events(self, events): pass
    
    def update(self): pass
        
    def draw(self, screen): pass
    ...
class GameOver(GameState):
    
    def __init__(self, manager):
        super().__init__(manager)
    
    def handle_events(self, events): pass
    
    def update(self): pass
        
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
        
        self.screen = pygame.display.get_surface()
        
        self.score = 0
        self.lives = 3
    
    def change_state(self, new_state: GameStateID):
        if new_state == GameStateID.QUIT:
            return False
        
        self.current_state = self.states[new_state]
        return True
        
    def handle_events(self, event):
        result = self.current_state.handle_events(event)
        if result:
            if isinstance(result, tuple):
                mode, state = result
                self.player_mode = mode
                return self.change_state(state)
            return self.change_state(result)
        return True
    
    def update(self):
        self.current_state.update()
    
    def draw(self, screen):
        self.current_state.draw(screen)
        

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
        