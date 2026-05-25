import pygame
import json
import os
from src.core.config import GRID_SIZE, GRID_COLS, GRID_ROWS, COLORS, WINDOW_WIDTH, WINDOW_HEIGHT

EDITOR_WIDTH = 1000
EDITOR_HEIGHT = 700
TOOL_PANEL_WIDTH = 150


class EditMode:
    PLACE_BEEPER = "beeper"
    PLACE_WALL = "wall"
    SET_KAREL = "karel"
    ERASE = "erase"


class LevelEditor:
    def __init__(self):
        self.screen = pygame.display.set_mode((EDITOR_WIDTH, EDITOR_HEIGHT))
        pygame.display.set_caption("Karel Level Editor")
        
        self.clock = pygame.time.Clock()
        # Use a font that supports Georgian (Sylfaen is common on Windows)
        font_names = "Sylfaen, Arial Unicode MS, DejaVu Sans, sans-serif"
        self.font = pygame.font.SysFont(font_names, 24)
        self.small_font = pygame.font.SysFont(font_names, 18)
        
        self.running = True
        self.current_tool = EditMode.PLACE_BEEPER
        
        self.offset_x = TOOL_PANEL_WIDTH + 20
        self.offset_y = 50
        
        self.beepers = {}
        self.walls = []
        self.karel_start = [0, 0, "east"]
        self.karel_beepers = 10
        
        self.level_name = "Custom Level"
        self.level_description = "Create your own level!"
        
        self.buttons = self._create_buttons()
        
    def _create_buttons(self):
        buttons = []
        tool_y = 100
        
        tools = [
            (EditMode.PLACE_BEEPER, "Beeper"),
            (EditMode.PLACE_WALL, "Wall"),
            (EditMode.SET_KAREL, "Karel"),
            (EditMode.ERASE, "Erase")
        ]
        
        for mode, label in tools:
            btn = {
                'rect': pygame.Rect(10, tool_y, TOOL_PANEL_WIDTH - 20, 40),
                'mode': mode,
                'label': label
            }
            buttons.append(btn)
            tool_y += 50
            
        buttons.append({
            'rect': pygame.Rect(10, EDITOR_HEIGHT - 100, TOOL_PANEL_WIDTH - 20, 40),
            'action': 'save',
            'label': 'Save'
        })
        
        buttons.append({
            'rect': pygame.Rect(10, EDITOR_HEIGHT - 50, TOOL_PANEL_WIDTH - 20, 40),
            'action': 'cancel',
            'label': 'Cancel'
        })
        
        return buttons
    
    def world_to_screen(self, x, y):
        return self.offset_x + x * GRID_SIZE, self.offset_y + y * GRID_SIZE
    
    def screen_to_world(self, screen_x, screen_y):
        x = (screen_x - self.offset_x) // GRID_SIZE
        y = (screen_y - self.offset_y) // GRID_SIZE
        if 0 <= x < GRID_COLS and 0 <= y < GRID_ROWS:
            return x, y
        return None
    
    def run(self):
        while self.running:
            self._handle_events()
            self._render()
            self.clock.tick(60)
        
        return self._export_level()
    
    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self._handle_click(event.pos)
                elif event.button == 3:
                    self._handle_right_click(event.pos)
                    
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
    
    def _handle_click(self, pos):
        for btn in self.buttons:
            if btn['rect'].collidepoint(pos):
                if 'mode' in btn:
                    self.current_tool = btn['mode']
                elif btn.get('action') == 'save':
                    self.running = False
                    return
                elif btn.get('action') == 'cancel':
                    self.running = False
                    return
                return
        
        world_pos = self.screen_to_world(pos[0], pos[1])
        if world_pos:
            x, y = world_pos
            
            if self.current_tool == EditMode.PLACE_BEEPER:
                if (x, y) in self.beepers:
                    self.beepers[(x, y)] += 1
                else:
                    self.beepers[(x, y)] = 1
                    
            elif self.current_tool == EditMode.PLACE_WALL:
                wall_dir = self._get_wall_direction(pos, x, y)
                if wall_dir:
                    wall_tuple = (x, y, wall_dir)
                    if wall_tuple in self.walls:
                        self.walls.remove(wall_tuple)
                    else:
                        self.walls.append(wall_tuple)
                    
            elif self.current_tool == EditMode.SET_KAREL:
                self.karel_start = [x, y, "east"]
                
            elif self.current_tool == EditMode.ERASE:
                if (x, y) in self.beepers:
                    del self.beepers[(x, y)]
                
                walls_to_remove = [(wx, wy, wd) for wx, wy, wd in self.walls if wx == x and wy == y]
                for wall in walls_to_remove:
                    self.walls.remove(wall)
    
    def _get_wall_direction(self, pos, grid_x, grid_y):
        screen_x, screen_y = self.world_to_screen(grid_x, grid_y)
        local_x = pos[0] - screen_x
        local_y = pos[1] - screen_y
        
        threshold = GRID_SIZE // 4
        
        if local_y < threshold:
            return "north"
        elif local_y > GRID_SIZE - threshold:
            return "south"
        elif local_x < threshold:
            return "west"
        elif local_x > GRID_SIZE - threshold:
            return "east"
        
        return None
    
    def _handle_right_click(self, pos):
        world_pos = self.screen_to_world(pos[0], pos[1])
        if world_pos:
            x, y = world_pos
            if (x, y) in self.beepers and self.beepers[(x, y)] > 1:
                self.beepers[(x, y)] -= 1
            elif (x, y) in self.beepers:
                del self.beepers[(x, y)]
    
    def _render(self):
        self.screen.fill((40, 40, 50))
        
        self._draw_tool_panel()
        self._draw_grid()
        self._draw_walls()
        self._draw_beepers()
        self._draw_karel()
        
        pygame.display.flip()
    
    def _draw_tool_panel(self):
        pygame.draw.rect(self.screen, (30, 30, 40), (0, 0, TOOL_PANEL_WIDTH, EDITOR_HEIGHT))
        
        title = self.font.render("Tools", True, (255, 255, 100))
        self.screen.blit(title, (10, 10))
        
        for btn in self.buttons:
            is_selected = btn.get('mode') == self.current_tool
            color = (100, 150, 100) if is_selected else (60, 60, 80)
            
            if btn.get('action') == 'save':
                color = (50, 150, 50)
            elif btn.get('action') == 'cancel':
                color = (150, 50, 50)
            
            pygame.draw.rect(self.screen, color, btn['rect'], border_radius=5)
            pygame.draw.rect(self.screen, (200, 200, 200), btn['rect'], 2, border_radius=5)
            
            label = self.small_font.render(btn['label'], True, (255, 255, 255))
            label_rect = label.get_rect(center=btn['rect'].center)
            self.screen.blit(label, label_rect)
        
        info_y = 350
        info_texts = [
            f"Karel Beepers: {self.karel_beepers}",
            f"Total Beepers: {sum(self.beepers.values())}",
            f"Walls: {len(self.walls)}"
        ]
        
        for text in info_texts:
            rendered = self.small_font.render(text, True, (200, 200, 200))
            self.screen.blit(rendered, (10, info_y))
            info_y += 25
    
    def _draw_grid(self):
        for row in range(GRID_ROWS):
            for col in range(GRID_COLS):
                screen_x, screen_y = self.world_to_screen(col, row)
                pygame.draw.rect(self.screen, (80, 80, 100), 
                               (screen_x, screen_y, GRID_SIZE, GRID_SIZE), 1)
        
        pygame.draw.rect(self.screen, (150, 150, 200),
                        (self.offset_x, self.offset_y, 
                         GRID_COLS * GRID_SIZE, GRID_ROWS * GRID_SIZE), 3)
    
    def _draw_walls(self):
        for x, y, direction in self.walls:
            screen_x, screen_y = self.world_to_screen(x, y)
            
            if direction == 'north':
                start = (screen_x, screen_y)
                end = (screen_x + GRID_SIZE, screen_y)
            elif direction == 'south':
                start = (screen_x, screen_y + GRID_SIZE)
                end = (screen_x + GRID_SIZE, screen_y + GRID_SIZE)
            elif direction == 'east':
                start = (screen_x + GRID_SIZE, screen_y)
                end = (screen_x + GRID_SIZE, screen_y + GRID_SIZE)
            elif direction == 'west':
                start = (screen_x, screen_y)
                end = (screen_x, screen_y + GRID_SIZE)
            
            pygame.draw.line(self.screen, (200, 50, 50), start, end, 6)
    
    def _draw_beepers(self):
        for (x, y), count in self.beepers.items():
            screen_x, screen_y = self.world_to_screen(x, y)
            center_x = screen_x + GRID_SIZE // 2
            center_y = screen_y + GRID_SIZE // 2
            
            pygame.draw.circle(self.screen, COLORS['beeper'], 
                             (center_x, center_y), GRID_SIZE // 4)
            pygame.draw.circle(self.screen, (200, 150, 0), 
                             (center_x, center_y), GRID_SIZE // 4, 2)
            
            if count > 1:
                count_text = self.small_font.render(str(count), True, (0, 0, 0))
                text_rect = count_text.get_rect(center=(center_x, center_y))
                self.screen.blit(count_text, text_rect)
    
    def _draw_karel(self):
        x, y, direction = self.karel_start
        screen_x, screen_y = self.world_to_screen(x, y)
        center_x = screen_x + GRID_SIZE // 2
        center_y = screen_y + GRID_SIZE // 2
        
        size = GRID_SIZE * 0.6
        half_size = size // 2
        pygame.draw.rect(self.screen, COLORS['karel'],
                        (center_x - half_size, center_y - half_size, size, size), 
                        border_radius=5)
        
        arrow_text = {'north': '↑', 'south': '↓', 'east': '→', 'west': '←'}
        arrow = self.font.render(arrow_text[direction], True, (255, 255, 255))
        arrow_rect = arrow.get_rect(center=(center_x, center_y))
        self.screen.blit(arrow, arrow_rect)
    
    def _export_level(self):
        beepers_list = [[x, y, count] for (x, y), count in self.beepers.items()]
        
        level_data = {
            "id": "custom",
            "name": self.level_name,
            "description": self.level_description,
            "karel_start": tuple(self.karel_start),
            "beepers": beepers_list,
            "walls": self.walls,
            "karel_beepers": self.karel_beepers
        }
        
        return level_data


def open_level_editor():
    editor = LevelEditor()
    level_data = editor.run()
    return level_data
