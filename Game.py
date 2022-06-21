import random
from Hangmans import HANGMANPICS

class Player:
    def __init__(self, username, address = None):
        self.username = username
        self.address = address
    
    def __eq__(self, other):
        return self.username == other.username

class Game:
    def __init__(self):
        self.players = []
        self.scoreboard = []
        self.round_counter = 1
        self.word = ""
        self.attempts = {}
        self.max_lifes = len(HANGMANPICS)
        self.correctLetters = 0
    
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

    def choosePlayerCreatingWord(self):
        return random.choice(self.players).username
    
    def setWord(self, word):
        self.word = word
        self.correctLetters = len(word)
    
    def updateWordForUser(self, username):
        user_db = self.attempts[username]
        user_letters = user_db[1]
        new_user_word = ""
        for char in self.word:
            if char in user_letters:
                new_user_word += f'{char} '
            else:
                new_user_word += '_ '
        self.attempts[username][0] = new_user_word
        print(self.attempts)
        return new_user_word
    
    def resetRound(self):
        self.word = ""
        self.attempts = {}
        self.max_lifes = len(HANGMANPICS)
        self.correctLetters = 0
