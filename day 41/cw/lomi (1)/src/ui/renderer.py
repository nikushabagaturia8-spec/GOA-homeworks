import pygame
import os

from src.core.config import WINDOW_WIDTH, WINDOW_HEIGHT, GRID_SIZE, GRID_ROWS, GRID_COLS, COLORS
from src.core.translations import get_text

ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'assets', "photo")
BACKGROUND_PATH = os.path.join(ASSETS_DIR, 'background', 'background_1.png')
CHARACTER_PATH = os.path.join(ASSETS_DIR, 'character', 'char_1.png')
BLOCK_PATH = os.path.join(ASSETS_DIR, 'block_colission', 'bock_1.png')
BLOCK_WALL_PATH = os.path.join(ASSETS_DIR, 'block_colission', 'bock_wall.png')
SOUND_ON_PATH = os.path.join(ASSETS_DIR, 'sound', 'Sound_on.png')
SOUND_OFF_PATH = os.path.join(ASSETS_DIR, 'sound', 'Sound_off.png')


class Renderer:
    def __init__(self, screen):
        self.screen = screen
        # Use a font that supports Georgian (Sylfaen is common on Windows)
        font_names = "Sylfaen, Arial Unicode MS, DejaVu Sans, sans-serif"
        self.font = pygame.font.SysFont(font_names, 24)
        self.small_font = pygame.font.SysFont(font_names, 18)
        self.offset_x = (WINDOW_WIDTH - GRID_COLS * GRID_SIZE) // 2
        self.offset_y = (WINDOW_HEIGHT - GRID_ROWS * GRID_SIZE) // 2
        self.current_level = 1
        self.total_levels = 1
        self._load_assets()

    def _load_assets(self):
        try:
            self.background_img = pygame.image.load(BACKGROUND_PATH).convert()
            self.background_img = pygame.transform.scale(self.background_img, (WINDOW_WIDTH, WINDOW_HEIGHT))
            print("✓ Background loaded")
        except Exception as e:
            print(f"✗ Could not load background: {e}")
            self.background_img = None

        try:
            self.character_img = pygame.image.load(CHARACTER_PATH).convert_alpha()
            char_size = int(GRID_SIZE * 0.8)
            self.character_img = pygame.transform.scale(self.character_img, (char_size, char_size))
            self.character_sprites = {
                'east': self.character_img,
                'north': pygame.transform.rotate(self.character_img, 90),
                'west': pygame.transform.rotate(self.character_img, 180),
                'south': pygame.transform.rotate(self.character_img, 270),
            }
            print("✓ Character sprite loaded")
        except Exception as e:
            print(f"✗ Could not load character: {e}")
            self.character_sprites = None

        try:
            self.block_wall = pygame.image.load(BLOCK_WALL_PATH).convert_alpha()
            self.block_wall = pygame.transform.scale(self.block_wall, (GRID_SIZE, GRID_SIZE))

            self.block_img = pygame.image.load(BLOCK_PATH).convert_alpha()
            self.block_img = pygame.transform.scale(self.block_img, (GRID_SIZE, GRID_SIZE))
            print("✓ Block sprite loaded")
        except Exception as e:
            print(f"✗ Could not load block: {e}")
            self.block_img = None

        try:
            self.sound_on_img = pygame.image.load(SOUND_ON_PATH).convert_alpha()
            self.sound_on_img = pygame.transform.scale(self.sound_on_img, (40, 40))
            self.sound_off_img = pygame.image.load(SOUND_OFF_PATH).convert_alpha()
            self.sound_off_img = pygame.transform.scale(self.sound_off_img, (40, 40))
            
            # Define button position (bottom-left corner)
            self.music_button_rect = pygame.Rect(10, WINDOW_HEIGHT - 50, 40, 40)
            print("✓ Sound icons loaded")
        except Exception as e:
            print(f"✗ Could not load sound icons: {e}")
            self.sound_on_img = None
            self.music_button_rect = pygame.Rect(10, WINDOW_HEIGHT - 50, 40, 40)
        
        self.editor_button_rect = pygame.Rect(60, WINDOW_HEIGHT - 50, 100, 40)
        self.language_button_rect = pygame.Rect(170, WINDOW_HEIGHT - 50, 60, 40)

    def draw_music_button(self, is_playing):
        """Draw music toggle button."""
        if self.sound_on_img and self.sound_off_img:
            img = self.sound_on_img if is_playing else self.sound_off_img
            self.screen.blit(img, self.music_button_rect)
        else:
            # Fallback text button
            color = (50, 200, 50) if is_playing else (200, 50, 50)
            pygame.draw.rect(self.screen, color, self.music_button_rect, border_radius=5)
            text = self.small_font.render("Music", True, (255, 255, 255))
            text_rect = text.get_rect(center=self.music_button_rect.center)
            self.screen.blit(text, text_rect)
    
    def draw_editor_button(self):
        color = (100, 100, 200)
        pygame.draw.rect(self.screen, color, self.editor_button_rect, border_radius=5)
        pygame.draw.rect(self.screen, (200, 200, 255), self.editor_button_rect, 2, border_radius=5)
        text = self.small_font.render("Level Editor", True, (255, 255, 255))
        text_rect = text.get_rect(center=self.editor_button_rect.center)
        self.screen.blit(text, text_rect)
    
    def draw_language_button(self, current_lang):
        color = (80, 120, 80)
        pygame.draw.rect(self.screen, color, self.language_button_rect, border_radius=5)
        pygame.draw.rect(self.screen, (150, 200, 150), self.language_button_rect, 2, border_radius=5)
        lang_display = "🇬🇪 ქარ" if current_lang == "ka" else "🇬🇧 ENG"
        text = self.small_font.render(lang_display, True, (255, 255, 255))
        text_rect = text.get_rect(center=self.language_button_rect.center)
        self.screen.blit(text, text_rect)

    def world_to_screen(self, x, y):
        return self.offset_x + x * GRID_SIZE, self.offset_y + y * GRID_SIZE

    def render(self, world, karel, current_level=1, total_levels=1, level_data=None, language="en"):
        self.current_level = current_level
        self.total_levels = total_levels
        self.current_level_data = level_data
        self.current_language = language

        if self.background_img:
            self.screen.blit(self.background_img, (0, 0))
        else:
            self.screen.fill(COLORS['background'])

        self._draw_grid()
        self._draw_beepers(world)
        self._draw_walls(world)
        self._draw_karel(karel)
        self._draw_info(karel)

    def _draw_grid(self):
        for row in range(GRID_ROWS):
            for col in range(GRID_COLS):
                screen_x, screen_y = self.world_to_screen(col, row)
                if not self.block_img:
                    pygame.draw.rect(self.screen, (100, 100, 150, 128), (screen_x, screen_y, GRID_SIZE, GRID_SIZE), 1)
                else:
                    self.screen.blit(self.block_wall, (screen_x, screen_y))

        pygame.draw.rect(self.screen, COLORS['grid_border'],
                         (self.offset_x, self.offset_y, GRID_COLS * GRID_SIZE, GRID_ROWS * GRID_SIZE), 3)

    def _draw_beepers(self, world):
        for (x, y), count in world.beepers.items():
            screen_x, screen_y = self.world_to_screen(x, y)
            center_x = screen_x + GRID_SIZE // 2
            center_y = screen_y + GRID_SIZE // 2
            pygame.draw.circle(self.screen, COLORS['beeper'], (center_x, center_y), GRID_SIZE // 4)
            pygame.draw.circle(self.screen, (200, 150, 0), (center_x, center_y), GRID_SIZE // 4, 2)
            if count > 1:
                count_text = self.small_font.render(str(count), True, (0, 0, 0))
                text_rect = count_text.get_rect(center=(center_x, center_y))
                self.screen.blit(count_text, text_rect)

    def _draw_walls(self, world):
        drawn_walls = set()
        for x, y, direction in world.walls:
            wall_key = (x, y, direction)
            if wall_key in drawn_walls:
                continue
            drawn_walls.add(wall_key)
            screen_x, screen_y = self.world_to_screen(x, y)

            if self.block_img:
                wall_block = pygame.transform.scale(self.block_img, (GRID_SIZE // 3, GRID_SIZE)) \
                    if direction in ['east', 'west'] else pygame.transform.scale(self.block_img, (GRID_SIZE, GRID_SIZE // 3))

                if direction == 'north':
                    pos_x, pos_y = screen_x, screen_y - GRID_SIZE // 6
                elif direction == 'south':
                    pos_x, pos_y = screen_x, screen_y + GRID_SIZE - GRID_SIZE // 6
                elif direction == 'east':
                    pos_x, pos_y = screen_x + GRID_SIZE - GRID_SIZE // 6, screen_y
                elif direction == 'west':
                    pos_x, pos_y = screen_x - GRID_SIZE // 6, screen_y
                self.screen.blit(wall_block, (pos_x, pos_y))
            else:
                if direction == 'north':
                    start, end = (screen_x, screen_y), (screen_x + GRID_SIZE, screen_y)
                elif direction == 'south':
                    start, end = (screen_x, screen_y + GRID_SIZE), (screen_x + GRID_SIZE, screen_y + GRID_SIZE)
                elif direction == 'east':
                    start, end = (screen_x + GRID_SIZE, screen_y), (screen_x + GRID_SIZE, screen_y + GRID_SIZE)
                elif direction == 'west':
                    start, end = (screen_x, screen_y), (screen_x, screen_y + GRID_SIZE)
                pygame.draw.line(self.screen, COLORS['wall'], start, end, 4)

    def _draw_karel(self, karel):
        screen_x, screen_y = self.world_to_screen(karel.x, karel.y)
        center_x = screen_x + GRID_SIZE // 2
        center_y = screen_y + GRID_SIZE // 2

        if self.character_sprites:
            sprite = self.character_sprites[karel.direction]
            sprite_rect = sprite.get_rect(center=(center_x, center_y))
            self.screen.blit(sprite, sprite_rect)
        else:
            size = GRID_SIZE * 0.6
            half_size = size // 2
            pygame.draw.rect(self.screen, COLORS['karel'],
                             (center_x - half_size, center_y - half_size, size, size), border_radius=5)

    def _draw_info(self, karel):
        info_y = 10

        level_text = self.font.render(f"Level {self.current_level} / {self.total_levels}", True, (255, 255, 100))
        level_bg = pygame.Surface((150, 30))
        level_bg.set_alpha(180)
        level_bg.fill((30, 30, 50))
        level_x = (WINDOW_WIDTH - 150) // 2
        self.screen.blit(level_bg, (level_x, 5))
        level_rect = level_text.get_rect(center=(WINDOW_WIDTH // 2, 20))
        self.screen.blit(level_text, level_rect)

        info_bg = pygame.Surface((200, 85))
        info_bg.set_alpha(180)
        info_bg.fill((30, 30, 50))
        self.screen.blit(info_bg, (5, 5))

        pos_text = self.font.render(f"{get_text('position', self.current_language)} ({karel.x}, {karel.y})", True, (255, 255, 255))
        self.screen.blit(pos_text, (10, info_y))

        direction_names = {
            'north': get_text('north', self.current_language),
            'south': get_text('south', self.current_language),
            'east': get_text('east', self.current_language),
            'west': get_text('west', self.current_language)
        }
        dir_text = self.font.render(f"{get_text('facing', self.current_language)} {direction_names[karel.direction]}", True, (255, 255, 255))
        self.screen.blit(dir_text, (10, info_y + 25))

        bag_text = self.font.render(f"{get_text('beepers', self.current_language)} {karel.beeper_bag}", True, (255, 255, 255))
        self.screen.blit(bag_text, (10, info_y + 50))

        if self.current_level_data:
            req_bg = pygame.Surface((220, 180))
            req_bg.set_alpha(180)
            req_bg.fill((30, 30, 50))
            self.screen.blit(req_bg, (WINDOW_WIDTH - 225, 5))

            req_title = self.font.render(get_text('level_goal', self.current_language), True, (255, 255, 100))
            self.screen.blit(req_title, (WINDOW_WIDTH - 220, 10))

            level_name_key = "name_ka" if self.current_language == "ka" else "name"
            level_name = self.small_font.render(self.current_level_data.get(level_name_key, ""), True, (200, 200, 255))
            self.screen.blit(level_name, (WINDOW_WIDTH - 220, 35))

            desc_key = "description_ka" if self.current_language == "ka" else "description"
            desc_lines = self._wrap_text(self.current_level_data.get(desc_key, ""), 200)
            for i, line in enumerate(desc_lines):
                desc_text = self.small_font.render(line, True, (200, 200, 200))
                self.screen.blit(desc_text, (WINDOW_WIDTH - 220, 55 + i * 18))

            goal_y = 55 + len(desc_lines) * 18 + 10
            
            if self.current_level_data.get("goal_beepers"):
                goal_text = self.small_font.render(f"{get_text('place_beepers', self.current_language)}", True, (255, 200, 100))
                self.screen.blit(goal_text, (WINDOW_WIDTH - 220, goal_y))
                goal_count = len(self.current_level_data["goal_beepers"])
                count_text = self.small_font.render(f"{goal_count} {get_text('positions', self.current_language)}", True, (255, 255, 255))
                self.screen.blit(count_text, (WINDOW_WIDTH - 220, goal_y + 18))
            elif self.current_level_data.get("beepers"):
                beeper_count = sum(b[2] for b in self.current_level_data["beepers"])
                goal_text = self.small_font.render(f"{get_text('collect', self.current_language)} {beeper_count} {get_text('beeper_s', self.current_language)}", True, (255, 200, 100))
                self.screen.blit(goal_text, (WINDOW_WIDTH - 220, goal_y))
                if self.current_level_data.get("goal_position"):
                    gx, gy = self.current_level_data["goal_position"]
                    pos_text = self.small_font.render(f"{get_text('return_to', self.current_language)} ({gx}, {gy})", True, (255, 255, 255))
                    self.screen.blit(pos_text, (WINDOW_WIDTH - 220, goal_y + 18))

        controls_bg = pygame.Surface((220, 200))
        controls_bg.set_alpha(180)
        controls_bg.fill((30, 30, 50))
        self.screen.blit(controls_bg, (WINDOW_WIDTH - 225, WINDOW_HEIGHT - 205))

        controls = [
            get_text('controls', self.current_language),
            get_text('run', self.current_language),
            get_text('speed', self.current_language),
            get_text('next_level', self.current_language),
            get_text('prev_level', self.current_language),
            get_text('restart', self.current_language),
            get_text('music_toggle', self.current_language),
            get_text('stop', self.current_language),
            get_text('quit', self.current_language),
            "",
            get_text('code_file', self.current_language)
        ]
        for i, text in enumerate(controls):
            control_text = self.small_font.render(text, True, (255, 255, 255))
            self.screen.blit(control_text, (WINDOW_WIDTH - 220, WINDOW_HEIGHT - 200 + i * 17))

    def _wrap_text(self, text, max_width):
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            test_surface = self.small_font.render(test_line, True, (255, 255, 255))
            if test_surface.get_width() <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines
