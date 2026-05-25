from src.core.config import DIRECTIONS, DIRECTION_ORDER, GRID_COLS, GRID_ROWS


class Karel:
    def __init__(self, x=0, y=0, direction='east'):
        self.x = x
        self.y = y
        self.direction = direction
        self.beeper_bag = 10

    def move(self, world):
        dx, dy = DIRECTIONS[self.direction]
        new_x = self.x + dx
        new_y = self.y + dy

        if not (0 <= new_x < GRID_COLS and 0 <= new_y < GRID_ROWS):
            print("Karel can't move - boundary!")
            return False

        if world.has_wall(self.x, self.y, self.direction):
            print("Karel can't move - wall!")
            return False

        self.x = new_x
        self.y = new_y
        return True

    def turn_left(self):
        current_index = DIRECTION_ORDER.index(self.direction)
        new_index = (current_index - 1) % 4
        self.direction = DIRECTION_ORDER[new_index]

    def turn_right(self):
        current_index = DIRECTION_ORDER.index(self.direction)
        new_index = (current_index + 1) % 4
        self.direction = DIRECTION_ORDER[new_index]

    def pick_beeper(self, world):
        if world.has_beeper(self.x, self.y):
            world.remove_beeper(self.x, self.y)
            self.beeper_bag += 1
            return True
        print("No beeper here!")
        return False

    def put_beeper(self, world):
        if self.beeper_bag > 0:
            world.add_beeper(self.x, self.y)
            self.beeper_bag -= 1
            return True
        print("No beepers in bag!")
        return False

    def front_is_clear(self, world):
        dx, dy = DIRECTIONS[self.direction]
        new_x = self.x + dx
        new_y = self.y + dy
        if not (0 <= new_x < GRID_COLS and 0 <= new_y < GRID_ROWS):
            return False
        return not world.has_wall(self.x, self.y, self.direction)

    def front_is_blocked(self, world):
        return not self.front_is_clear(world)

    def left_is_clear(self, world):
        self.turn_left()
        result = self.front_is_clear(world)
        self.turn_right()
        return result

    def right_is_clear(self, world):
        self.turn_right()
        result = self.front_is_clear(world)
        self.turn_left()
        return result

    def beepers_present(self, world):
        return world.has_beeper(self.x, self.y)

    def no_beepers_present(self, world):
        return not self.beepers_present(world)

    def beepers_in_bag(self):
        return self.beeper_bag > 0

    def no_beepers_in_bag(self):
        return self.beeper_bag == 0

    def facing_north(self):
        return self.direction == 'north'

    def facing_south(self):
        return self.direction == 'south'

    def facing_east(self):
        return self.direction == 'east'

    def facing_west(self):
        return self.direction == 'west'
