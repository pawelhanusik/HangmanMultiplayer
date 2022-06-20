#!/usr/bin/env python3

from hashlib import new
import socket
import sys, syslog
from daemon import runner
from struct import pack

from network.packet.CStartGamePacket import CStartGamePacket
from network.packet.Packet import Packet
from network.packet.SServerInfoPacket import SServerInfoPacket
from network.packet.CJoinPacket import CJoinPacket
from network.packet.SJoinPacket import SJoinPacket
from network.packet.SNewPlayerPacket import SNewPlayerPacket
from network.packet.SStartRoundPacket import SStartRoundPacket
from network.packet.CSelectWordPacket import CSelectWordPacket
from network.packet.SWordReadyPacket import SWordReadyPacket
from network.packet.CGuessLetterPacket import CGuessLetterPacket
from network.packet.SGuessLetterPacket import SGuessLetterPacket

from Game import Game, Player
import time
import json

from network.Server import Server

serverName = 'GameServer'
game = Game()
server = Server()
scoreboard = "test"

def log(*args, sep=' '):
    s = ''
    first = True
    for a in args:
        if first:
            first = False
        else:
            s += str(sep)
        s += str(a)
    syslog.syslog(syslog.LOG_DEBUG, s)

class App():
    def __init__(self):
        self.stdin_path = '/dev/null'
        # self.stdout_path = '/dev/tty'
        self.stdout_path = 'stdout'
        # self.stderr_path = '/dev/tty'
        self.stderr_path = 'stderr'
        self.pidfile_path =  '/tmp/foo.pid'
        self.pidfile_timeout = 5

        syslog.openlog(sys.argv[0])

    def __logLobbyDetails():
        global game
        log("Current lobby: ")
        log("User count: ", len(game.players))
        for player in game.players:
            log(player.username, ' - ', player.address)
        log("Lobby open? ", LOBBY_OPEN)
        log("Current round: ", game.round_counter)
        log("Scoreboard: ", game.scoreboard)
        log("-" * 30)

    def run(self):
        lobby_starting_timestamp = int(time.time())
        LOBBY_CLOSE_TIME = 20
        LOBBY_OPEN = True
        log("Lobby creation timestamp: ", lobby_starting_timestamp)
        log(f"Server will stop accepting new users after: {LOBBY_CLOSE_TIME} seconds")

        while True:
            server.sendPacket(SServerInfoPacket(serverName))
            def onPacketRecv(packet, address):
                if isinstance(packet, CJoinPacket):
                    global game

                    newPlayer = Player(packet.username, address)
                    # Dont add player if he tried to join after more than 30 seconds from lobby creation
                    lobby_age = int(time.time()) - lobby_starting_timestamp
                    if lobby_age >= LOBBY_CLOSE_TIME:
                        server.sendPacketTo(
                            SJoinPacket('Lobby closed! Better luck next time :)', False),
                            newPlayer.address
                        )
                        return
                    hasNewPlayerBeenAdded = game.addPlayer(newPlayer)
                    if not hasNewPlayerBeenAdded:
                        server.sendPacketTo(
                            SJoinPacket('', False),
                            newPlayer.address
                        )
                    else:
                        server.sendPacketTo(
                            SJoinPacket(game.getPlayersStr(), True),
                            newPlayer.address
                        )
                        server.sendPacket(
                            SNewPlayerPacket(newPlayer.username)
                        )
                
                elif isinstance(packet, CStartGamePacket):
                    chosenPlayer = game.choosePlayerCreatingWord()
                    server.sendPacket(SStartRoundPacket(chosenPlayer, scoreboard))
                    log("Sending start round packet")
                    
                elif isinstance(packet, CSelectWordPacket):
                    log("========== New word selected ==========")
                    log(f"========== {packet.word.lower()} ==========")
                    game.setWord(packet.word.lower())
                    
                    # After the word has been selected, censor it and send it to all users
                    server.sendPacket(SWordReadyPacket('_ ' * len(game.word)))

                elif isinstance(packet, CGuessLetterPacket):
                    guessing_username = packet.username
                    guessing_letter = packet.letter
                    log("Got a guess from: ", guessing_username)
                    for player in game.players:
                        if player.username == guessing_username:
                            player_address = player.address
                    game.attempts[guessing_username][1] += guessing_letter
                    if guessing_letter not in game.word:
                        game.attempts[guessing_username][2] += 1
                    else:
                        pass
                    new_censored_word = game.updateWordForUser(guessing_username)
                    server.sendPacketTo(
                        SGuessLetterPacket(new_censored_word, game.attempts[guessing_username][2] ),
                        player_address
                    )

            server.select(onPacketRecv, 2)
            
            # If lobby closed, send info to all connected players that the round is starting
            # Game can only start if LOBBY_CLOSE_TIME has passed and there are at least 2 connected players
            lobby_age = int(time.time()) - lobby_starting_timestamp
            if lobby_age >= LOBBY_CLOSE_TIME and LOBBY_OPEN == True and len(game.players) >= 2:
                for player in game.players:
                    # 0 -> word, 1 -> guessed letters, 2 -> wrong guesses counter
                    game.attempts[player.username] = ["", " ", 0]
                chosenPlayer = game.choosePlayerCreatingWord()
                game.scoreboard = [ [player.username, 0] for player in game.players]
                scoreboardJsoned = json.dumps(game.scoreboard)
                server.sendPacket(
                    SStartRoundPacket(chosenPlayer, scoreboardJsoned)
                )
                log("========== Sending start round packet ==========")
                LOBBY_OPEN = False

            self.__logLobbyDetails()
            time.sleep(2)

app = App()
daemon_runner = runner.DaemonRunner(app)
daemon_runner.do_action()
