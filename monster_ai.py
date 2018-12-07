class AI:
    def OnTurnBegins(self, game, tiles):
        pass

    def OnTurnEnds(self, game):
        pass

    def OnMiniTurnBegins(self, game, tilesLeft):
        pass

    def OnMiniTurnEnds(self, game, tilesLeft):
        pass

    def PickTile(self, game, tiles):
        raise NotImplemented("Method PickTile is not implemented")

    def GetPowerChoice(self, game, tile):
        raise NotImplemented("Method UsePowerBeforeMove is not implemented")

    def GetMove(self, game, tile):
        raise NotImplemented("Method Move is not implemented")
