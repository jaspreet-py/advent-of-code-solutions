import operator
from dataclasses import KW_ONLY, InitVar, dataclass, field
from pathlib import Path
from typing import Literal, overload

cwd = Path(__file__).parent


@dataclass
class Dial:
    _min: int = field(init=False, repr=False)
    _max: int = field(init=False, repr=False)
    _pos: int = field(init=False, repr=False)
    _travel: int = field(init=False, repr=False)

    _: KW_ONLY
    max: InitVar[int]
    min: InitVar[int] = 0
    pos: InitVar[None | int] = None

    def __post_init__(self, max, min, pos):
        # `min` will be an instance of `property` if no value is assigned on class initialization. Manually
        # (re-)assign default value in this case
        if isinstance(min, property):
            min = 0
        if not isinstance(min, int) or min < 0:
            raise ValueError(f"Expected 'min' value >= 0. Got {min}")
        self._min = min

        if not isinstance(max, int) or max <= self.min:
            raise ValueError(f"Expected 'max' value >= {self.min}. Got {max}")
        self._max = max

        # Similar to `min` above
        if isinstance(pos, property):
            pos = None
        if pos is None:
            pos = self._min
        if not isinstance(pos, int) or pos < self.min or pos > self.max:
            raise ValueError(f"Expected 'pos' value between {self.min} and {self.max} (inclusive). Got {pos}")
        self._pos = pos

        self._travel = self.max - self.min + 1

    @property
    def min(self):
        return self._min

    @property
    def max(self):
        return self._max

    @property
    def pos(self):
        return self._pos

    @overload
    def rotate(self, clicks: ..., *, return_revs: Literal[True]) -> int: ...
    @overload
    def rotate(self, clicks: ..., *, return_revs=...) -> None: ...
    def rotate(self, clicks: int, *, return_revs=False):
        revs = None
        if return_revs:
            img_pos = self._pos + clicks  # Imaginary position on the Dial if it continued till infinity
            revs = abs(img_pos // self._travel)  # Number of times '0' is passed over
            if (clicks > 0 and (img_pos % self._travel) == 0) or clicks < 0 and self._pos == 0:
                revs -= 1

        self._pos = (self._pos + clicks) % self._travel
        if return_revs and self._pos == 0:
            revs += 1

        return revs


@dataclass
class Puzzle:
    _answer: None | int = field(init=False, default=None)
    _dial: Dial = field(init=False)
    _rotations: list[int] = field(init=False)

    def __post_init__(self):
        self._dial = Dial(max=99, pos=50)
        self._rotations = self._load_input()

    def _process_rotation_input(self, rotation: str):
        rotation = rotation.strip()
        direction, distance = rotation[0], int(rotation[1:])
        if direction not in ('L', 'R'):
            raise Exception(f'Invalid input: {rotation}')

        return operator.neg(distance) if direction == 'L' else distance

    def _load_input(self):
        rotations = []
        with open(cwd.joinpath('input.txt')) as f:
            rotations = [self._process_rotation_input(rotation) for rotation in f.readlines()]

        return rotations

    def solve(self):
        if self._answer is not None:
            return

        dial = self._dial
        cnt = 0
        for rotation in self._rotations:
            dial.rotate(rotation)
            if dial.pos == 0:
                cnt += 1

        self._answer = cnt

    @property
    def answer(self):
        if self._answer is None:
            raise Exception('Unsolved puzzle! Please solve before trying to get answer')

        return self._answer


if __name__ == '__main__':
    puzzle = Puzzle()
    puzzle.solve()
    print(f'Answer: {puzzle.answer}')
