import enum

class Status(enum.Enum):
    freeze = '0'
    move = '1'
    jump = '2'
    attack_freeze = '3'
    attack_move = '4'
    attack_jump = '5'
    die = '6'
class Direction(enum.Enum):
    right = '0'
    left = '1'
class F_gane(enum.Enum):
    f_game_1 = './font_game/f_game.otf'
    f_game_2 = './font_game/f_game.ttf'

arr_random_status_soldier = [
    Status.freeze, 
    Status.move, 
    Status.jump, 
    Status.attack_freeze, 
    Status.attack_move, 
    Status.attack_jump
]