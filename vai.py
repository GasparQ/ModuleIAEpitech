import random
import re
import sys

import GAME_DATA
import monster_game
from ai import AI


class VAI(AI):
    def __init__(self, index, is_ghost, ai):
        super().__init__(index, is_ghost)
        self.ai = ai
        self.game = monster_game.Game(monster_game.Board(), [self.ai])
        self.currentTurn = -1
        self.miniTurnBegun = False
        self.pickedTile = None
        self.powerChoice = None
        self.moved = False
        self.power_handlers = {
            GAME_DATA.RED: self.handle_red_power,
            GAME_DATA.PINK: self.handle_pink_power,
            GAME_DATA.BLUE: self.handle_blue_power,
            GAME_DATA.GRAY: self.handle_gray_power,
            GAME_DATA.BLACK: self.handle_black_power,
            GAME_DATA.WHITE: self.handle_white_power,
            GAME_DATA.PURPLE: self.handle_purple_power,
            GAME_DATA.BROWN: self.handle_brown_power
        }
        self.move_regex = re.compile('positions disponibles : {([0-9 ,]+)}')
        self.white_regex = re.compile('([a-z]+)-[0-9]-[a-z]+, positions disponibles :.*')

    def play(self, line):
        self.game.Replicate(self.state)

        response = ""

        if int(self.state.turn) > self.currentTurn:
            if self.currentTurn > -1:
                self.ai.OnTurnEnds(self.game)
            self.ai.OnTurnBegins(self.game, self.game.tiles)

        if line.startswith("Tuiles disponibles :"):
            if self.currentTurn > -1:
                self.ai.OnMiniTurnEnds(self.game, self.game.tiles)
            self.ai.OnMiniTurnBegins(self.game, self.game.tiles)
            self.moved = False
            self.pickedTile = self.ai.PickTile(self.game, self.game.tiles)
            if self.pickedTile is not None:
                response = str(self.game.tiles.index(self.pickedTile))
        elif line.startswith("Voulez-vous activer le pouvoir (0/1) ?"):
            self.powerChoice = self.ai.GetPowerChoice(self.game, self.pickedTile)
            response = '0' if self.powerChoice is None or self.powerChoice is False else '1'
        elif line.startswith("positions disponibles :"):
            move = self.ai.GetMove(self.game, self.pickedTile)
            response = str(move)

            match = self.move_regex.match(line)
            if match:
                possibles = match.group(1).replace(' ', '').split(',')
                if response not in possibles:
                    print('Trying to move at', response, 'but possible moves are', possibles, file=sys.stderr)
                    if self.pickedTile is not None:
                        char = self.game.board.GetCharacter(self.pickedTile)
                        print(char, file=sys.stderr)

            self.moved = True
        elif self.pickedTile in self.power_handlers.keys() and self.powerChoice is not None:
            response = self.power_handlers[self.pickedTile](line)

        self.currentTurn = int(self.state.turn)

        if len(response) == 0:
            response = str(random.randrange(0, 9))

        print(line, '=>', response)

        return response

    def handle_red_power(self, line):
        # do nothing
        return ''

    def handle_pink_power(self, line):
        # do nothing
        return ''

    def handle_blue_power(self, line):
        if line.startswith('Quelle salle bloquer ?'):
            return str(self.powerChoice[0])
        elif line.startswith('Quelle sortie ? Chosir parmi :'):
            return str(self.powerChoice[1])
        return ''

    def handle_gray_power(self, line):
        if line.startswith('Quelle salle obscurcir ?'):
            return str(self.powerChoice)
        return ''

    def handle_black_power(self, line):
        # do nothing
        return ''

    def handle_white_power(self, line):
        match = self.white_regex.match(line)
        if match:
            color_text = match.group(1)
            color = GAME_DATA.FRENCH_TILES[color_text]
            if color in self.powerChoice.keys():
                return str(self.powerChoice[color])
            char = self.game.board.GetCharacter(color)
            print('Cannot move character ', GAME_DATA.TILE_NAMES[char.color],
                  ' => available choice:', self.powerChoice,
                  ' => position: ', char.position,
                  ', alone: ', char.alone, ', innocent: ', char.innocent,
                  file=sys.stderr)
        return ''

    def handle_purple_power(self, line):
        if line.startswith('Avec quelle couleur échanger (pas violet!) ?'):
            return str(GAME_DATA.TILE_NAMES[self.powerChoice])
        return ''

    def handle_brown_power(self, line):
        # do nothing
        return ''

    def end(self):
        # self.ai.SaveTo(self.path)
        pass
