from GUI import *

class BulletHell:
    def __init__(self):
        pygame.mixer.pre_init()
        pygame.mixer.init()
        sound.play_music()
        pygame.init()
        pygame.display.set_caption("Bullet Hell")
        self.resolutions = Resolution()
        if self.resolutions.fullscreen:
            self.window_surface = pygame.display.set_mode(self.resolutions.resolution, FULLSCREEN)
        else:
            self.window_surface = pygame.display.set_mode(self.resolutions.resolution)
            
        self.ui_manager = UIManager(self.resolutions.resolution,
                                    theme_path="data/themes/bullet_hell_theme.json")
        
        self.game_state = MAINMENU
        self.player_mode = None
        self.difficulty = None
        
        self.player = Player()
        self.bullet = Bullet()
        self.homing_bullet = HomingBullet()
        self.exploding_bullet = ExplodingBullet()
        
        self.players = Group()
        self.bullets = Group()
        
        self.music_volume_slider = UIHorizontalSlider(pygame.Rect((int(self.rect.width / 2),
                                                           int(self.rect.height * 0.70)),
                                                          (240, 25)),
                                              50.0,
                                              (0.0, 100.0),
                                              self.ui_manager,
                                              container=self,
                                              click_increment=5)
        
            
    def check_resolution_changed(self):
        
        ...
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.button == pygame.K_ESCAPE:
                    self.running = False
            
            
        
        
        ...
        
    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000.0
            
            self.handle_events()
            
            self.ui_manager.update(dt)
            
            self.ui_manager.draw_ui(self.window_surface)
            
            pygame.display.update()
        ...
    
if __name__ == "__main__":
    game = BulletHell()
    game.run()