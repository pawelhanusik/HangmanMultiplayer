class Player:
    def __init__(self, username, address = None):
        self.username = username
        self.address = address
    
    def __eq__(self, other):
        return self.username == other.username

class Game:
    def __init__(self):
        self.players = []
    
    def getPlayersStr(self):
        ret = ''
        first = True

        for p in self.players:
            if first:
                first = False
            else:
                ret += '\n'
            
            ret += p.username
        
        return ret
    
    def addPlayer(self, player :Player):
        if player in self.players:
            return False
        
        self.players += [player]
        return True
