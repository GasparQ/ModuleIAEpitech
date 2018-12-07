from monsterpiece import MonsterPiece


class Inspector(MonsterPiece):

    def __init__(self):
        MonsterPiece.__init__(self)

    def GetReward(self, game):
        bonus = game.GetNumberOfInnocent()
        malus = 0
        if self.lastGameState is not None:
            bonus -= self.lastGameState.GetNumberOfInnocent()
            malus = self.lastGameState.GetPotentialPhantomScoring()
        return bonus - malus
