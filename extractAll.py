import json
from re import U
import requests
from bs4 import BeautifulSoup
import os

'''
This is a work in progress - the main purpose is to extract most of the info that I will need for everything
else. First two things are all of the Pokemon stats and moves.
'''

MasterPokemonStatsDict = {}
MasterPokemonMovesDict = {}

'''
each row has the same format
[5] = name
[7] = hp
[9] = attack
[11] = def
[13] = speed (spd)
[15] = special (spc)
'''
def extractStatsHelper(row):
    Name = row[5].text.rstrip()
    Hp = row[7].text.rstrip()
    Atk = row[9].text.rstrip()
    Def = row[11].text.rstrip()
    Spd = row[13].text.rstrip()
    Spc = row[15].text.rstrip()
    
    pokemon = {
        Name : {
            "hp"    : Hp,
            "atk"   : Atk,
            "def"   : Def,
            "spd"   : Spd,
            "spc"   : Spc
        }
    }

    MasterPokemonStatsDict.update(pokemon)

'''
each row has the same format
[1] = name
[5] = type
[9] = power
[11] = accuracy
'''
def extractMovesHelper(row):
    Name = row[1].text.rstrip()
    Type = row[5].text.rstrip()
    Power = row[9].text.rstrip()
    Accuracy = row[11].text.rstrip()

    move = {
        Name : {
            "type"  : Type,
            "power" : Power,
            "acc"   : Accuracy
        }
    }

    MasterPokemonMovesDict.update(move)

def extractStats():
    URL = 'https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_base_stats_(Generation_I)'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')

    pokemon = soup.find_all('tr')
    for row in pokemon[1:152]:
        extractStatsHelper(row.contents)

    with open('gen1Stats.json', 'w') as outfile:
        json.dump(MasterPokemonStatsDict, outfile)
    
        outfile.close()

def extractMoves():
    URL = 'http://www.psypokes.com/rby/attacks.php'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')

    movesTable = soup.select('.psypoke tr')
    for row in movesTable[1:]:
        extractMovesHelper(row)

    with open('gen1Moves.json','w') as outfile:
        json.dump(MasterPokemonMovesDict, outfile)

        outfile.close()

if __name__ == '__main__':
    extractStats()
    extractMoves()