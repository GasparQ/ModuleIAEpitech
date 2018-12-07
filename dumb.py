from ai import AI
import random
from runnable_ai import runai


class Dumb(AI):
    def __init__(self, index, is_ghost):
        super().__init__(index, is_ghost)

    def play(self, line):
        return str(random.randrange(0, 9))

    def end(self):
        pass


def lancer_ghost():
    runai(Dumb(1, True))


def lancer_inspector():
    runai(Dumb(0, False))
