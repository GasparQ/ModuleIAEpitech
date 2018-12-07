from monsterpiece import MonsterPiece


class Phantom(MonsterPiece):
    def __init__(self):
        MonsterPiece.__init__(self)

    def GetReward(self, game):
        bonus = 0
        malus = game.GetNumberOfInnocent()
        if self.lastGameState is not None:
            bonus = self.lastGameState.GetPotentialPhantomScoring() * 10
            malus -= self.lastGameState.GetNumberOfInnocent()
        return bonus - malus
