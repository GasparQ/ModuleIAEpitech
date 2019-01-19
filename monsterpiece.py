import random

import sys

import GAME_DATA
from monster_ai import AI
import action


class MonsterPiece(AI):
    def __init__(self):
        self.possibleActions = None
        self.values = {}
        for i in range(0, 9):
            for j in range(0, 9):
                for k in range(0, 9):
                    for l in range(0, 9):
                        if i + j + k + l == 8:
                            self.values['{}-{}-{}-{}'.format(i, j, k, l)] = 0.0
        self.transitions = []
        self.epsilon = 0.9
        self.choosenAction = None
        self.moved = False
        self.lastGameState = None
        self.turns = 0

    def OnMiniTurnEnds(self, game, tilesLeft):
        self.lastGameState = game.Clone()

    """
        Train the model
        Updates values for each states from a given reward
    """

    def OnTurnEnds(self, game):
        reward = self.GetReward(game)
        self.UpdateValues(reward)
        self.UpdateEpsilon()

    """
        Generates the possible actions for a turn and pick one in function of values
    """

    def OnMiniTurnBegins(self, game, tilesLeft):
        self.GeneratePossibleActions(game, tilesLeft)
        self.ChooseAction()
        if self.choosenAction is None:
            self.choosenAction = action.Action(game, [None, None, None, None], game)
        self.transitions.append(self.choosenAction)
        self.moved = False
        # print('Mini turn begins: ', self.choosenAction, file=sys.stderr)

    def SaveTo(self, filename):
        file = open(filename, 'w')
        print(self.epsilon, file=file)
        for key, value in self.values.items():
            print(key, value, file=file)
        file.close()

    def Load(self, data):
        pass

    def LoadFrom(self, filename):
        file = open(filename, 'r')
        self.epsilon = float(file.readline())
        for line in file.readlines():
            key, value = line.split(' ')
            self.values[key] = float(value)
        file.close()

    @staticmethod
    def GetPowerStates(actions, color, which):
        newActions = []
        for curract in actions:
            if which == action.POST_POWER and curract.actions[action.PRE_POWER] is not None:
                newActions.append(curract)
                continue
            character = curract.next_state.board.GetCharacter(color)
            choices = character.GetPowerChoices(curract.next_state)
            for choice in choices:
                currAction = curract.Clone()
                currAction.next_state = currAction.next_state.Clone()
                currAction.actions[which] = choice
                character.UsePower(currAction.next_state, choice)
                newActions.append(currAction)
        return newActions

    @staticmethod
    def GetMovesStates(actions, color):
        newActions = []
        for curract in actions:
            moves = curract.next_state.board.GetPossibleMoves(color)
            for move in moves:
                currAction = curract.Clone()
                currAction.actions[action.MOVE] = move
                currAction.next_state = currAction.next_state.Clone()
                currAction.next_state.board.MovePlayer(color, move)
                newActions.append(currAction)
        return newActions

    def GeneratePossibleActions(self, game, tilesLeft):
        self.possibleActions = []

        # print('tiles left: ', tilesLeft, file=sys.stderr)
        for tile in tilesLeft:
            actions = [action.Action(game, [tile, None, None, None], game)]
            character = game.board.GetCharacter(tile)

            if character.GetPowerTiming() & GAME_DATA.BEFORE:
                actions = MonsterPiece.GetPowerStates(actions, character.color, action.PRE_POWER)

            actions = MonsterPiece.GetMovesStates(actions, character.color)

            if character.GetPowerTiming() & GAME_DATA.AFTER:
                actions = MonsterPiece.GetPowerStates(actions, character.color, action.POST_POWER)

            self.possibleActions += actions

    def ChooseAction(self):
        if random.uniform(0, 1) < self.epsilon:
            self.choosenAction = random.choice(self.possibleActions)
        else:
            self.choosenAction = None
            maxValue = 0
            for currAct in self.possibleActions:
                val = self.values[currAct.next_state.board.GetStateHash()]
                if self.choosenAction is None or val > maxValue:
                    maxValue = val
                    self.choosenAction = currAct
        # print('Actions:', self.possibleActions, file=sys.stderr)
        # print('Choose:', self.choosenAction, file=sys.stderr)

    def GetReward(self, game):
        raise NotImplemented("Method GetReward is not implemented")

    def UpdateValues(self, reward):
        for transition in reversed(self.transitions):
            state_hash = transition.state.board.GetStateHash()
            next_state_hash = transition.next_state.board.GetStateHash()
            if reward == 0:
                self.values[state_hash] += 0.001 * (self.values[next_state_hash] - self.values[state_hash])
            else:
                self.values[state_hash] += 0.001 * (reward - self.values[state_hash])

        self.transitions = []

    def UpdateEpsilon(self):
        self.turns += 1
        if self.turns % 10 == 0:
            self.turns = 0
            self.epsilon = max(self.epsilon * 0.96, 0.05)

    def PickTile(self, game, tiles):
        return self.choosenAction.actions[action.PICK]

    def GetPowerChoice(self, game, tile):
        if self.choosenAction is None:
            return None
        if self.moved:
            return self.choosenAction.actions[action.POST_POWER]
        return self.choosenAction.actions[action.PRE_POWER]

    def GetMove(self, game, tile):
        self.moved = True
        if self.choosenAction is None:
            return None
        return self.choosenAction.actions[action.MOVE]
