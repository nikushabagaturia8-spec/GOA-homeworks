_karel = None
_world = None
_game = None
_command_queue = []


def _set_game_reference(karel, world, game):
    global _karel, _world, _game
    _karel = karel
    _world = world
    _game = game


def _add_command(command_name, *args):
    _command_queue.append((command_name, args))


def _get_commands():
    return _command_queue


def _clear_commands():
    global _command_queue
    _command_queue = []


def move():
    _add_command('move')


def turn_left():
    _add_command('turn_left')


def turn_right():
    _add_command('turn_right')


def turn_around():
    _add_command('turn_left')
    _add_command('turn_left')


def pick_beeper():
    _add_command('pick_beeper')


def put_beeper():
    _add_command('put_beeper')


def front_is_clear():
    if _karel and _world:
        return _karel.front_is_clear(_world)
    return True


def front_is_blocked():
    return not front_is_clear()


def left_is_clear():
    if _karel and _world:
        return _karel.left_is_clear(_world)
    return True


def right_is_clear():
    if _karel and _world:
        return _karel.right_is_clear(_world)
    return True


def beepers_present():
    if _karel and _world:
        return _karel.beepers_present(_world)
    return False


def no_beepers_present():
    return not beepers_present()


def beepers_in_bag():
    if _karel:
        return _karel.beepers_in_bag()
    return True


def no_beepers_in_bag():
    return not beepers_in_bag()


def facing_north():
    if _karel:
        return _karel.facing_north()
    return False


def facing_south():
    if _karel:
        return _karel.facing_south()
    return False


def facing_east():
    if _karel:
        return _karel.facing_east()
    return True


def facing_west():
    if _karel:
        return _karel.facing_west()
    return False
