import instruction_follower as if_

def _level(*args, **kwargs):
    def wrapper(program):
        return if_.HRM(program, *args, **kwargs)
    return wrapper

level1 = _level()
level2 = _level()
level3 = _level(6, {0: 'U', 1: 'J', 2: 'X', 3: 'G', 4: 'B', 5: 'E'})
level4 = _level(3)
level6 = _level(3)
level7 = _level(9)
level8 = _level(3)
level9 = _level(9)
level10 = _level(5)
level11 = _level(3)
level12 = _level(5)
level41 = _level(25, {24: 0})
