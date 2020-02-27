import re
import string


class HRMException(Exception):
    pass


class TileError(HRMException):
    def __init__(self, data):
        super().__init__(
            "Bad tile address! "
            "Tile with address {} does not exist! "
            "Where do you think you're going?"
            .format(data))


class OutOfBoundsError(HRMException):
    def __init__(self):
        super().__init__(
            "Overflow! "
            "Each data unit is restricted to values between -999 and 999. "
            "That should be enough for anybody.")


class OperandsError(HRMException):
    def __init__(self, operator):
        super().__init__(
            "You can't {0} with mixed operands! "
            "{0}'ing between one letter and one number is invalid. "
            "Only nice respectable pairs of two letters or two numbers are allowed.! "
            .format(operator))


class HRMType:
    letters = set()
    def get(self, *_):
        return self.data


class Empty(HRMType):
    def __init__(self, data):
        self.data = data


class Number(HRMType):
    letters = set(string.digits)
    def __init__(self, data):
        self.data = int(data)


class Word(HRMType):
    letters = set(string.ascii_letters)
    def __init__(self, data):
        self.data = str(data)


class Pointer:
    letters = set('[]')
    def __init__(self, other):
        self.other = other
        self.letters |= other.letters
        self.pointer = False
        self.data = None

    def __call__(self, data):
        data = str(data)
        self.pointer = False
        if data[0] == '[':
            if data[-1] != ']':
                raise HRMException("Mismatched parenths")
            self.pointer = True
            data = data[1:-1]
        self.data = self.other(data).get()
        return self

    def get(self, hrm):
        if self.pointer:
            d = hrm[self.data]
            return d.data if isinstance(d, HRMBox) else d
        return self.data


class HRMBox:
    def __init__(self, data):
        if isinstance(data, HRMBox):
            self.word = data.word
            self.data = data.data
            return
        self.word = False
        data = str(data)
        if set(data) <= set(string.digits + '-'):
            data = int(data)
        elif not len(data):
            raise ValueError("HRMBox needs to be at least a size of one.")
        elif set(data) <= set(string.ascii_letters):
            self.word = True
            data = ord(data[0].upper()) - 64
        else:
            raise ValueError("HRMBox can only be numbers and digits.")
        self.data = data

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        if value >= 1000 or value <= -1000:
            raise OutOfBoundsError()
        self._data = value

    @property
    def item(self):
        if self.word:
            return chr(self.data + 64)
        return self.data

    def __int__(self):
        if self.word:
            pass
        return self.data

    def __index__(self):
        return self.__int__()

    def __repr__(self):
        return 'HRMBox({})'.format(self.item)

    def __sub__(self, other):
        if not isinstance(other, HRMBox):
            other = HRMBox(other)
        if self.word is not other.word:
            raise OperandsError('')
        return HRMBox(self.data - other.data)

    def __add__(self, other):
        if not isinstance(other, HRMBox):
            other = HRMBox(other)
        if self.word is not other.word:
            raise OperandsError('')
        return HRMBox(self.data + other.data)

    def __eq__(self, other):
        if not isinstance(other, HRMBox):
            other = HRMBox(other)
        return self.data == other.data

    def __lt__(self, other):
        if not isinstance(other, HRMBox):
            other = HRMBox(other)
        return self.data < other.data


COMMANDS = {}
def hrm_fn(*types):
    def wrap(fn):
        def call(self, *args):
            def data():
                fn(self, *[t(a).get(self) for t, a in zip(types, args)])
            return data
        call.letters = [t.letters for t in types]
        COMMANDS[fn.__name__.upper()[1:]] = call
        return call
    return wrap


class HRM:
    def __init__(self, program, tiles=0, tile_defaults=None):
        if tile_defaults is None:
            tile_defaults = {}
        self.tokens = list(remove_invalid_tokens(tokenise(program)))
        self.labels = {
            places[0]: i
            for i, (command, places) in enumerate(self.tokens)
            if command == 'LABEL'
        }
        self.tiles = [None for _ in range(tiles)]
        for tile, value in tile_defaults.items():
            self.tiles[tile] = HRMBox(value)
        self.hand = None

    @property
    def hand(self):
        return self._hand

    @hand.setter
    def hand(self, value):
        if value is None:
            self._hand = HRMBox(value)
        self._hand = value

    def __getitem__(self, index):
        try:
            return self.tiles[index]
        except IndexError:
            raise MemoryError(index)

    def __setitem__(self, index, value):
        try:
            self.tiles[index] = HRMBox(value)
        except IndexError:
            raise MemoryError(index)

    def __call__(self, input):
        self.input = iter(input)
        self.output = []
        self.command = 0
        self.hand = None
        commands = [
            COMMANDS[command](self, *value)
            for command, value in self.tokens
        ]
        while True:
            try:
                commands[self.command]()
            except IndexError: # No more commands
                break
            except StopIteration: # No more input
                break
            self.command += 1
        return self.output

    @hrm_fn(Empty)
    def _inbox(self):
        self.hand = HRMBox(next(self.input))

    @hrm_fn(Empty)
    def _outbox(self):
        self.output.append(self.hand.item)
        self.hand = None

    @hrm_fn(Pointer(Number))
    def _copyfrom(self, index):
        self.hand = self[index]

    @hrm_fn(Pointer(Number))
    def _copyto(self, index):
        self[index] = self.hand

    @hrm_fn(Pointer(Number))
    def _add(self, index):
        self.hand += self[index]

    @hrm_fn(Pointer(Number))
    def _sub(self, index):
        self.hand -= self[index]

    @hrm_fn(Pointer(Number))
    def _bumpup(self, index):
        self[index] += 1
        self.hand = self[index]

    @hrm_fn(Pointer(Number))
    def _bumpdn(self, index):
        self[index] -= 1
        self.hand = self[index]

    @hrm_fn(Word)
    def _jump(self, label):
        self.command = self.labels[label]

    @hrm_fn(Word)
    def _jumpz(self, label):
        if self.hand == 0:
            self.command = self.labels[label]

    @hrm_fn(Word)
    def _jumpn(self, label):
        if self.hand < 0:
            self.command = self.labels[label]

    @hrm_fn(Number)
    def _comment(self, comment):
        pass

    @hrm_fn(Word)
    def _label(self, label):
        pass


COMMAND_TYPES = {command: fn.letters for command, fn in COMMANDS.items()}
def tokenise(hrm_string):
    for line in hrm_string.split('\n'):
        line = line.strip()
        if re.match('--', line) is not None:
            continue
        label = re.match('(\w+):', line)
        if label is not None:
            yield 'LABEL', label.group(1)
            continue
        expression = line.split()
        if expression and all(re.match('\w+|\[\w+\]$', e) for e in expression):
            yield expression
            continue


def remove_invalid_tokens(tokens):
    for command, *values in tokens:
        command = command.upper()
        command_types = COMMAND_TYPES.get(command, None)
        if (command_types is not None and
            all(set(v) <= c for c, v in zip(command_types, values))):
            yield command, values
