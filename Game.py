class Game:
    def __init__(self):
        self.players = []
    
    def getPlayers(self):
        return self.players
    
    def addPlayer(self, username):
        self.players += [username]
