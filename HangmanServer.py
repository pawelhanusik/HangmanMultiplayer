#!/usr/bin/env python3

from cgi import print_form
from hashlib import new
import socket
import sys, syslog
import daemon
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
from network.packet.SRoundEndPacket import SRoundEndPacket
from network.packet.SGameEndPacket import SGameEndPacket

from Game import Game, Player
import time
import json

from network.Server import Server

def log(*args, sep=' '):
    """
    Log into syslog. Call this function as you would call print()
    """

    s = ''
    first = True
    for a in args:
        if first:
            first = False
        else:
            s += str(sep)
        s += str(a)
    syslog.syslog(syslog.LOG_DEBUG, s)

# Run server as Daemon
with daemon.DaemonContext():
    syslog.openlog(sys.argv[0])

    serverName = 'GameServer'
    game = Game()
    server = Server()
    scoreboard = "test"

    lobby_starting_timestamp = int(time.time())
    LOBBY_CLOSE_TIME = 20
    LOBBY_OPEN = True
    log("Lobby creation timestamp: ", lobby_starting_timestamp)
    log(f"Server will stop accepting new users after: {LOBBY_CLOSE_TIME} seconds")
    
    # Outputs basic lobby info to syslog
    def logLobbyDetails():
        global game
        log("Current lobby: ")
        log("User count: ", len(game.players))
        for player in game.players:
            log(player.username, ' - ', player.address)
        log("Lobby open? ", LOBBY_OPEN)
        log("Current round: ", game.round_counter)
        log("Scoreboard: ", game.scoreboard)
        log("-" * 30)

    chosenPlayer = ""
    finishedPlayers = 0

    lobby_starting_timestamp = int(time.time())
    round_starting_timestamp = int(time.time())
    LOBBY_CLOSE_TIME = 15
    ROUND_TIME = 120
    MAX_ROUNDS = 4
    LOBBY_OPEN = True
    log("Lobby creation timestamp: ", lobby_starting_timestamp)
    log(f"Server will stop accepting new users after: {LOBBY_CLOSE_TIME} seconds")

    #Functions controlling all activities that should be done before next round
    def roundEnded(winner):
        global finishedPlayers

        for scoreboard in game.scoreboard:
            if scoreboard[0] == winner:
                scoreboard[1] += 1
        scoreboardJsoned = json.dumps(game.scoreboard)
        if finishedPlayers == (len(game.players) - 1):
            server.sendPacket(
                SRoundEndPacket(scoreboardJsoned, winner, game.word)
            )
            game.round_counter += 1
            
            #Resetting variables in game
            game.resetRound()
            for player in game.players:
                # 0 -> word, 1 -> guessed letters, 2 -> wrong guesses counter, 3 -> good guess
                game.attempts[player.username] = ["", " ", 0, 0]
            round_starting_timestamp = int(time.time())

    while True:
        server.sendPacket(SServerInfoPacket(serverName))
        def onPacketRecv(packet, address):
            global finishedPlayers
            
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
                # Send false if there was an error adding new player to the lobby
                if not hasNewPlayerBeenAdded:
                    server.sendPacketTo(
                        SJoinPacket('', False),
                        newPlayer.address
                    )
                # Player successfully added to the lobby
                else:
                    server.sendPacketTo(
                        SJoinPacket(game.getPlayersStr(), True),
                        newPlayer.address
                    )
                    server.sendPacket(
                        SNewPlayerPacket(newPlayer.username)
                    )
            # Sending packet announcing start of a new round
            elif isinstance(packet, CStartGamePacket):
                global chosenPlayer
                chosenPlayer = game.choosePlayerCreatingWord()
                scoreboardJsoned = json.dumps(game.scoreboard)
                server.sendPacket(SStartRoundPacket(chosenPlayer, scoreboardJsoned))
                log("Sending start round packet")
            # Getting a new guess word from a player
            elif isinstance(packet, CSelectWordPacket):
                log("========== New word selected ==========")
                log(f"========== {packet.word.lower()} ==========")
                game.setWord(packet.word.lower())
                
                # After the word has been selected, censor it and send it to all users
                server.sendPacket(SWordReadyPacket('_ ' * len(game.word)))
            # Player has sent a guess letter
            elif isinstance(packet, CGuessLetterPacket):
                log(chosenPlayer)
                guessing_username = packet.username
                guessing_letter = packet.letter
                log("Got a guess from: ", guessing_username)
                for player in game.players:
                    if player.username == guessing_username:
                        player_address = player.address
                game.attempts[guessing_username][1] += guessing_letter

                #Wrong guess
                if guessing_letter not in game.word:
                    game.attempts[guessing_username][2] += 1
                #Correct guess
                else:
                    #New letter
                    if guessing_letter not in game.attempts[guessing_username][1]:
                        correctLetters = len([i for i, x in enumerate(game.word) if x == guessing_letter])
                        game.attempts[guessing_username][3] += correctLetters
                    #Letter used before
                    else:
                        print("You fool! You have used that letter before. Great waste of round.")
                new_censored_word = game.updateWordForUser(guessing_username)
                if game.attempts[guessing_username][3] == game.correctLetters:
                    finishedPlayers += 1
                    roundEnded(guessing_username)
                elif game.attempts[guessing_username][2] == 6:
                    log(chosenPlayer)
                    finishedPlayers += 1
                    if finishedPlayers == (len(game.players) - 1):
                        roundEnded(chosenPlayer)
                else:
                    log("SENDING PACKET")
                    server.sendPacketTo(
                    SGuessLetterPacket(new_censored_word, game.attempts[guessing_username][2]),
                    player_address
                )

        server.select(onPacketRecv, 2)
        round_age = int(time.time()) - round_starting_timestamp

        #Controlling round time
        if round_age >= ROUND_TIME:
            roundEnded(chosenPlayer)
            for scoreboard in game.scoreboard:
                if scoreboard[0] == chosenPlayer:
                    scoreboard[1] += 1
        
        #Controlling rounds count
        if game.round_counter == MAX_ROUNDS + 1:
            sorted_scoreboard = sorted(game.scoreboard, key=lambda x: x[1], reverse=True)
            log(f"Sorted scoreboard: {sorted_scoreboard}")
            first_player = sorted_scoreboard[0]
            players_with_same_points = [first_player[0]]
            sorted_scoreboard.pop(0)
            for scoreboard in sorted_scoreboard:
                log(scoreboard)
                if scoreboard[1] == first_player[1]:
                    players_with_same_points.append(scoreboard[0])
            server.sendPacket(SGameEndPacket(json.dumps(players_with_same_points)))
            exit(0)
        # If lobby closed, send info to all connected players that the round is starting
        # Game can only start if LOBBY_CLOSE_TIME has passed and there are at least 2 connected players
        lobby_age = int(time.time()) - lobby_starting_timestamp
        if lobby_age >= LOBBY_CLOSE_TIME and LOBBY_OPEN == True and len(game.players) >= 2:
            for player in game.players:
                # 0 -> word, 1 -> guessed letters, 2 -> wrong guesses counter, 3 -> good guess
                game.attempts[player.username] = ["", " ", 0, 0]
            chosenPlayer = game.choosePlayerCreatingWord()
            game.scoreboard = [ [player.username, 0] for player in game.players]
            scoreboardJsoned = json.dumps(game.scoreboard)
            server.sendPacket(
                SStartRoundPacket(chosenPlayer, scoreboardJsoned)
            )
            log("========== Sending start round packet ==========")
            LOBBY_OPEN = False

        # logLobbyDetails()
        time.sleep(2)
