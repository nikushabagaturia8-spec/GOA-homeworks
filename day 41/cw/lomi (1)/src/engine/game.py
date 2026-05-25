import pygame
import time
import os
import sys

# Add project root to path to allow imports if run directly
current_dir = os.path.dirname(os.path.abspath(__file__))
# current_dir is .../src/engine
# parent is .../src
# grandparent is .../GAME which is project root
project_root = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, project_root)

# Also add src/core to path for commands import in my_program
src_dir = os.path.join(project_root, 'src')
core_dir = os.path.join(src_dir, 'core')
# We don't need src_dir in sys.path if we import as src.core
# But we need core_dir for proper resolution if needed
sys.path.insert(0, core_dir)

from src.core.karel import Karel
from src.core.world import World
from src.core.config import WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, FPS
from src.data.levels import get_level, get_level_count
from src.ui.renderer import Renderer
from src.core import commands
from src.core.translations import get_text

ASSETS_DIR = os.path.join(project_root, 'assets')
MUSIC_PATH = os.path.join(ASSETS_DIR, 'audio', 'Timeline 1.mp3')


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption(WINDOW_TITLE)

        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()

        self.current_level = 1
        self.total_levels = get_level_count()

        self.world = World()
        self.karel = None
        self.renderer = Renderer(self.screen)

        self.running = True
        self.executing = False
        self.command_queue = []
        self.command_index = 0
        self.command_delay = 0.4

        self.show_popup = False
        self.popup_message = ""
        self.popup_submessage = ""
        self.popup_type = "error"

        self.music_playing = True

        self.current_level_data = None
        self.level_goal_beepers = []
        self.level_has_beepers_to_collect = False
        
        self.current_language = "en"

        self._load_level(self.current_level)
        commands._set_game_reference(self.karel, self.world, self)
        self._load_music()

    def _load_music(self):
        try:
            pygame.mixer.music.load(MUSIC_PATH)
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)
            self.music_playing = True
            print("🎵 Music loaded and playing")
        except Exception as e:
            print(f"✗ Could not load music: {e}")
            self.music_playing = False

    def toggle_music(self):
        if self.music_playing:
            pygame.mixer.music.pause()
            self.music_playing = False
            print("🔇 Music paused")
        else:
            pygame.mixer.music.unpause()
            self.music_playing = True
            print("🔊 Music playing")
    
    def toggle_language(self):
        self.current_language = "ka" if self.current_language == "en" else "en"
        print(f"Language changed to: {'Georgian' if self.current_language == 'ka' else 'English'}")


    def _load_level(self, level_id):
        level = get_level(level_id)
        if not level:
            print(f"❌ Level {level_id} not found!")
            return False

        self.world.clear()

        start_x, start_y, start_dir = level["karel_start"]
        beepers_in_bag = level.get("karel_beepers", 10)
        self.karel = Karel(start_x, start_y, start_dir)
        self.karel.beeper_bag = beepers_in_bag

        for beeper_data in level["beepers"]:
            x, y, count = beeper_data
            self.world.add_beeper(x, y, count)

        for wall_data in level["walls"]:
            x, y, direction = wall_data
            self.world.add_wall(x, y, direction)

        self.current_level_data = level
        self.level_goal_beepers = level.get("goal_beepers", [])
        self.level_has_beepers_to_collect = len(level.get("beepers", [])) > 0

        commands._set_game_reference(self.karel, self.world, self)

        self.executing = False
        self.command_queue = []
        self.command_index = 0

        print(f"\n{'='*50}")
        print(f"📍 Level {level_id}: {level['name']}")
        print(f"📝 {level['description']}")
        print(f"{'='*50}\n")
        return True

    def load_and_run_program(self):
        commands._clear_commands()
        try:
            import importlib
            import src.my_program as my_program
            importlib.reload(my_program)
            my_program.main()
            self.command_queue = commands._get_commands()
            self.command_index = 0
            self.executing = True
            print(f"\n📋 Loaded {len(self.command_queue)} commands")
            print("▶️  Execution started...\n")
        except Exception as e:
            print(f"❌ Error loading program: {e}")

    def run(self):
        self.last_command_time = time.time()
        while self.running:
            self._handle_events()
            self._update()
            self._render()
            self.clock.tick(FPS)
        pygame.quit()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self._handle_keydown(event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = event.pos
                    if self.renderer.music_button_rect.collidepoint(mouse_pos):
                        self.toggle_music()
                    elif self.renderer.editor_button_rect.collidepoint(mouse_pos):
                        self._open_level_editor()
                    elif self.renderer.language_button_rect.collidepoint(mouse_pos):
                        self.toggle_language()

    def _handle_keydown(self, key):
        if self.show_popup:
            self.show_popup = False
            if self.popup_type == "success":
                self._next_level()
            return

        if key == pygame.K_ESCAPE or key == pygame.K_q:
            self.running = False
        elif key == pygame.K_r:
            self._reset_level()
        elif key == pygame.K_RETURN or key == pygame.K_SPACE:
            if not self.executing:
                self.load_and_run_program()
        elif key == pygame.K_n:
            self._next_level()
        elif key == pygame.K_p:
            self._prev_level()
        elif key == pygame.K_m:
            self.toggle_music()
        
        elif key == pygame.K_l:
            self.toggle_language()
        
        elif key == pygame.K_s:
            self.executing = False
            print("⏹️  Execution stopped")
        elif key == pygame.K_UP:
            self.command_delay = max(0.1, self.command_delay - 0.1)
            print(f"⏩ Speed: {1/self.command_delay:.1f}x")
        elif key == pygame.K_DOWN:
            self.command_delay = min(2.0, self.command_delay + 0.1)
            print(f"⏪ Speed: {1/self.command_delay:.1f}x")

    def _next_level(self):
        if self.current_level < self.total_levels:
            self.current_level += 1
            self._load_level(self.current_level)
        else:
            self._show_popup(" Congratulations!", "You completed all levels!", "success")

    def _prev_level(self):
        if self.current_level > 1:
            self.current_level -= 1
            self._load_level(self.current_level)

    def _reset_level(self):
        self._load_level(self.current_level)
        print("🔄 Level restarted!")
    
    def _open_level_editor(self):
        print("Opening level editor...")
        from src.editor.level_editor import open_level_editor
        
        level_data = open_level_editor()
        if level_data:
            print(f"Custom level created: {level_data['name']}")
            self._load_custom_level(level_data)
    
    def _load_custom_level(self, level_data):
        self.world.clear()
        
        start_x, start_y, start_dir = level_data["karel_start"]
        beepers_in_bag = level_data.get("karel_beepers", 10)
        self.karel = Karel(start_x, start_y, start_dir)
        self.karel.beeper_bag = beepers_in_bag
        
        for beeper_data in level_data["beepers"]:
            x, y, count = beeper_data
            self.world.add_beeper(x, y, count)
        
        for wall_data in level_data["walls"]:
            x, y, direction = wall_data
            self.world.add_wall(x, y, direction)
        
        self.current_level_data = level_data
        self.level_goal_beepers = level_data.get("goal_beepers", [])
        self.level_has_beepers_to_collect = len(level_data.get("beepers", [])) > 0
        
        commands._set_game_reference(self.karel, self.world, self)
        
        self.executing = False
        self.command_queue = []
        self.command_index = 0
        
        print(f"\n{'='*50}")
        print(f"📍 Custom Level: {level_data['name']}")
        print(f"📝 {level_data['description']}")
        print(f"{'='*50}\n")

    def _check_level_complete(self):
        if not self.current_level_data:
            return True, "Level complete!"

        goal_position = self.current_level_data.get("goal_position")
        
        if self.level_goal_beepers:
            for pos in self.level_goal_beepers:
                x, y = pos
                if (x, y) not in self.world.beepers or self.world.beepers[(x, y)] < 1:
                    return False, "Not all beepers placed at goal positions!"
            return True, "All beepers placed correctly!"
        
        elif self.level_has_beepers_to_collect:
            if len(self.world.beepers) > 0:
                return False, "Not all beepers collected!"
            if goal_position:
                goal_x, goal_y = goal_position
                if self.karel.x != goal_x or self.karel.y != goal_y:
                    return False, f"Return to position ({goal_x}, {goal_y})!"
            return True, "All beepers collected!"
        
        elif goal_position:
            goal_x, goal_y = goal_position
            if self.karel.x != goal_x or self.karel.y != goal_y:
                return False, f"Reach position ({goal_x}, {goal_y})!"
            return True, "Goal position reached!"
        
        return True, "Level complete!"


    def _update(self):
        if self.executing and self.command_queue:
            current_time = time.time()
            if current_time - self.last_command_time >= self.command_delay:
                self._execute_next_command()
                self.last_command_time = current_time

    def _execute_next_command(self):
        if self.command_index >= len(self.command_queue):
            self.executing = False
            print("Program completed!")
            
            is_complete, message = self._check_level_complete()
            if is_complete:
                self._show_popup("Level Complete!", message, "success")
            else:
                self._show_popup("Level Incomplete!", message, "error")
            return

        command_name, args = self.command_queue[self.command_index]
        self.command_index += 1

        try:
            if command_name == 'move':
                success = self.karel.move(self.world)
                if success:
                    print(f"  [{self.command_index}] move() ✓")
                else:
                    print(f"  [{self.command_index}] move() ✗ - blocked!")
                    self.executing = False
                    self._show_popup("Blocked!", "Try Again - Press R to restart", "error")
            elif command_name == 'turn_left':
                self.karel.turn_left()
                print(f"  [{self.command_index}] turn_left() ✓")
            elif command_name == 'turn_right':
                self.karel.turn_right()
                print(f"  [{self.command_index}] turn_right() ✓")
            elif command_name == 'pick_beeper':
                success = self.karel.pick_beeper(self.world)
                if success:
                    print(f"  [{self.command_index}] pick_beeper() ✓")
                else:
                    print(f"  [{self.command_index}] pick_beeper() ✗ - no beeper here!")
                    self.executing = False
                    self._show_popup("No Beeper!", "Try Again - Press R to restart", "error")
            elif command_name == 'put_beeper':
                success = self.karel.put_beeper(self.world)
                if success:
                    print(f"  [{self.command_index}] put_beeper() ✓")
                else:
                    print(f"  [{self.command_index}] put_beeper() ✗ - bag is empty!")
                    self.executing = False
                    self._show_popup(" Empty Bag!", "Try Again - Press R to restart", "error")
        except Exception as e:
            print(f"  [{self.command_index}] Error: {e}")
            self.executing = False

    def _show_popup(self, message, submessage="", popup_type="info"):
        self.show_popup = True
        self.popup_message = message
        self.popup_submessage = submessage
        self.popup_type = popup_type

    def _render(self):
        self.renderer.render(self.world, self.karel, self.current_level, self.total_levels, self.current_level_data, self.current_language)
        self.renderer.draw_music_button(self.music_playing)
        self.renderer.draw_language_button(self.current_language)
        if self.show_popup:
            self._draw_popup()
        pygame.display.flip()

    def _draw_popup(self):
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        popup_width, popup_height = 350, 180
        popup_x = (WINDOW_WIDTH - popup_width) // 2
        popup_y = (WINDOW_HEIGHT - popup_height) // 2

        if self.popup_type == "success":
            bg_color, border_color, text_color = (30, 80, 50), (100, 200, 100), (150, 255, 150)
        elif self.popup_type == "error":
            bg_color, border_color, text_color = (80, 30, 30), (200, 100, 100), (255, 150, 150)
        else:
            bg_color, border_color, text_color = (50, 50, 80), (100, 100, 150), (200, 200, 255)

        pygame.draw.rect(self.screen, bg_color, (popup_x, popup_y, popup_width, popup_height), border_radius=15)
        pygame.draw.rect(self.screen, border_color, (popup_x, popup_y, popup_width, popup_height), 3, border_radius=15)

        font = pygame.font.Font(None, 42)
        text = font.render(self.popup_message, True, text_color)
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 30))
        self.screen.blit(text, text_rect)

        small_font = pygame.font.Font(None, 24)
        if self.popup_submessage:
            sub = small_font.render(self.popup_submessage, True, (200, 200, 200))
            sub_rect = sub.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 10))
            self.screen.blit(sub, sub_rect)

        instruction = small_font.render("Press any key to continue...", True, (150, 150, 150))
        instruction_rect = instruction.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))
        self.screen.blit(instruction, instruction_rect)


def main():
    game = Game()
    game.run()


if __name__ == '__main__':
    main()
    
    

    