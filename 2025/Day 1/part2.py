from dataclasses import dataclass

from common import Puzzle


class Puzzle2(Puzzle):
    def solve(self):
        if self._answer is not None:
            return

        dial = self._dial
        cnt = 0
        for rotation in self._rotations:
            cnt += dial.rotate(rotation, return_revs=True)

        self._answer = cnt


if __name__ == '__main__':
    puzzle = Puzzle2()
    puzzle.solve()
    print(f'Answer: {puzzle.answer}')
