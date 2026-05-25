from src.core.config import GRID_COLS, GRID_ROWS


class World:
    def __init__(self, cols=GRID_COLS, rows=GRID_ROWS):
        self.cols = cols
        self.rows = rows
        self.beepers = {}
        self.walls = set()

    def add_beeper(self, x, y, count=1):
        if (x, y) in self.beepers:
            self.beepers[(x, y)] += count
        else:
            self.beepers[(x, y)] = count

    def remove_beeper(self, x, y):
        if (x, y) in self.beepers and self.beepers[(x, y)] > 0:
            self.beepers[(x, y)] -= 1
            if self.beepers[(x, y)] == 0:
                del self.beepers[(x, y)]
            return True
        return False

    def has_beeper(self, x, y):
        return (x, y) in self.beepers and self.beepers[(x, y)] > 0

    def get_beeper_count(self, x, y):
        return self.beepers.get((x, y), 0)

    def add_wall(self, x, y, direction):
        self.walls.add((x, y, direction))
        opposite = self._get_opposite_wall(x, y, direction)
        if opposite:
            self.walls.add(opposite)

    def _get_opposite_wall(self, x, y, direction):
        if direction == 'north' and y > 0:
            return (x, y - 1, 'south')
        elif direction == 'south' and y < self.rows - 1:
            return (x, y + 1, 'north')
        elif direction == 'east' and x < self.cols - 1:
            return (x + 1, y, 'west')
        elif direction == 'west' and x > 0:
            return (x - 1, y, 'east')
        return None

    def remove_wall(self, x, y, direction):
        self.walls.discard((x, y, direction))
        opposite = self._get_opposite_wall(x, y, direction)
        if opposite:
            self.walls.discard(opposite)

    def has_wall(self, x, y, direction):
        return (x, y, direction) in self.walls

    def clear(self):
        self.beepers.clear()
        self.walls.clear()

    def load_from_dict(self, data):
        self.clear()
        if 'beepers' in data:
            for beeper in data['beepers']:
                self.add_beeper(beeper['x'], beeper['y'], beeper.get('count', 1))
        if 'walls' in data:
            for wall in data['walls']:
                self.add_wall(wall['x'], wall['y'], wall['direction'])

    def to_dict(self):
        beepers_list = [
            {'x': x, 'y': y, 'count': count}
            for (x, y), count in self.beepers.items()
        ]
        seen_walls = set()
        walls_list = []
        for x, y, direction in self.walls:
            wall_key = tuple(sorted([(x, y, direction), self._get_opposite_wall(x, y, direction) or (x, y, direction)]))
            if wall_key not in seen_walls:
                seen_walls.add(wall_key)
                walls_list.append({'x': x, 'y': y, 'direction': direction})
        return {
            'cols': self.cols,
            'rows': self.rows,
            'beepers': beepers_list,
            'walls': walls_list,
        }
