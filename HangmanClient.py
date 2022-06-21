#!/usr/bin/env python3

from cProfile import run
from pydoc import cli
import socket
import struct
import time
import json 

from network.packet.Packet import Packet
from network.packet.SGameEndPacket import SGameEndPacket
from network.packet.SServerInfoPacket import SServerInfoPacket
from network.packet.CJoinPacket import CJoinPacket
from network.packet.SJoinPacket import SJoinPacket
from network.packet.SNewPlayerPacket import SNewPlayerPacket
from network.packet.CStartGamePacket import CStartGamePacket
from network.packet.SStartRoundPacket import SStartRoundPacket
from network.packet.CSelectWordPacket import CSelectWordPacket
from network.packet.SWordReadyPacket import SWordReadyPacket
from network.packet.CGuessLetterPacket import CGuessLetterPacket
from network.packet.SGuessLetterPacket import SGuessLetterPacket
from network.packet.SRoundEndPacket import SRoundEndPacket

from network.Client import Client
from Hangmans import HANGMANPICS

from enum import IntEnum

username = input("Select username: ")
client = Client()

print("Waiting for server...")

class GameState(IntEnum):
    CONNECTING = 0
    WAITING_FOR_PLAYERS = 1
    GAME_READY = 2

gameState = GameState.CONNECTING
running = True
address = None
guessing = True
players = []


def makeAGuess():
    guess = ""
    while len(guess) != 1:
        guess = input("Type a letter: ")
    client.sendPacketTo(CGuessLetterPacket(guess, username), address)

while running:
    if gameState == GameState.CONNECTING:
        packet, recvAddress = client.recvPacketFrom()
    else:
        packet = client.recvPacket()
    
    if gameState == GameState.CONNECTING:
        if isinstance(packet, SServerInfoPacket):
            address = recvAddress
            print(
                "Server name:", packet.serverName,
                "\tServer IP:", address
            )

            client.sendPacketTo(CJoinPacket(username), address)
            gameState = GameState.WAITING_FOR_PLAYERS

    elif gameState == GameState.WAITING_FOR_PLAYERS:
        if isinstance(packet, SJoinPacket):
            if not packet.isUsernameAccepted:
                print(packet.playersList)
                print("Incorrect username! Please try other.")
                username = input("Select username: ")
                gameState = GameState.CONNECTING
            else:
                players = packet.playersList.split("\n")
                #print("Players:", players)
        elif isinstance(packet, SNewPlayerPacket):
            if packet.username not in players:
                players += [packet.username]
            #print("Players:", players)
        elif isinstance(packet, SStartRoundPacket):
            print("-" * 30)
            gameState = GameState.GAME_READY
            scoreboard = json.loads(packet.scoreboard)
            print("Current scoreboard: ")
            print(scoreboard)
            print("-" * 30)
            if username != packet.pickerUsername:
                continue
            word = input("Input word: ")
            guessing = False
            client.sendPacketTo(CSelectWordPacket(word), address)

    elif gameState == GameState.GAME_READY:
        print(packet)
        if isinstance(packet, SRoundEndPacket):
            print(f"Winner of this round is: {packet.who_won}")
            print(f"Correct word was: {packet.game_word}")
            print(f"Current scoreboard is:\n")
            guessing = True
            gameState = GameState.WAITING_FOR_PLAYERS
            if username==packet.who_won:
                client.sendPacketTo(CStartGamePacket(), address)
            print(json.loads(packet.scoreboard))
        elif isinstance(packet, SGameEndPacket):
            print(f"Final winner/s:")
            for winner in json.loads(packet.winners):
                print(f"{winner}\n")
            print("Congratulations!!!")
            running = False
        elif isinstance(packet, SWordReadyPacket) and guessing == True:
            print("-" * 30)
            print("Word: ", packet.word)
            makeAGuess()
        elif isinstance(packet, SGuessLetterPacket) and guessing == True:
            print("GUESS LETTER")
            print(packet.word)
            print(packet.remainingLifes)
            print("-" * 30)
            print(HANGMANPICS[ packet.remainingLifes ])
            print(packet.word)
            print("PACKET RECEIVED")
            makeAGuess()
       

