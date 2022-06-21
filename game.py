#!/usr/bin/python3
from random import random

nplayers = 0
while nplayers <= 2:
    try:
        nplayers = int(input('Number of players: '))
    except ValueError:
        print('Integer number expected. Press Control-C to exit')
    except KeyboardInterrupt:
        print('Bye')
        exit()

# nplayers = 3
human_i = -2
wild_ones = False
print(nplayers)
class Player():
    human = False
    name = None
    def __init__(self):
        self.dices = [0] * 5
    def __repr__(self) -> str:
        return '%s: %s'%(self.name, self.dices)
players = [Player() for p in range(nplayers)]
players[human_i].name = 'You'
players[human_i].human = True
botn = 1
for p in players:
    if p != players[human_i]:
        p.name = 'Bot %d'%botn
        botn += 1

def roll():
    if (len(players) <= 1):
        return
    print('New round. Rolling dices')
    for player in players:
        for d in range(len(player.dices)):
            player.dices[d] = int(1+random()*6)
        player.dices = sorted(player.dices)
    if debug:
        show_table()

def bot(player: Player):
    unknown_dices = sum(len(p.dices) for p in players if p != player)
    expected_count = unknown_dices/6 + player.dices.count(call[0]) + (player.dices.count(1) if wild_ones and call[0] != 1 else 0)
    if call[1] > expected_count:
        return None
    return call[0], max(call[1]+1, int(expected_count))

def check_call(new_call):
    return new_call is None or new_call > call and new_call[1] > 0

def show_table():
    for p in players:
        print(p.name, '\t', p.dices)

def is_lie():
    print('Opening table...')
    show_table()
    count = 0
    for p in players:
        for d in p.dices:
            if d == call[0] or wild_ones and d == 1:
                count += 1
    print('The actual count', count, 'of', call[0], 'faces is', 'less' if count < call[1] else '>=','than the call of', call[1])
    
    loser_i = pi-1 if count < call[1] else pi
    loser = players[loser_i]
    print(conjugate(loser, 'lose') + ' one dice')
    loser.dices.pop()
    if not loser.dices:
        players.pop(loser_i)
        print(loser.name + (' are' if loser.human else ' is') + ' out of the game')
    return loser_i

def conjugate(subject, verb):
    return subject.name + ' ' + verb + ('' if subject.human else 's')


from re import match
call = 1, 0
debug = False
roll()
print('You can input bids by separating count and face values by space or comma or nothing.\n'
'If you enter "d" for debug all dices are shown.\n'
'Enter "w" to enable wild ones mode')

pi = 0
while len(players)>1:
    if pi >= len(players):
        pi = 0
    p = players[pi]
    if p.human:
        invalid_call = False
        if not debug:
            print('Your dices', p.dices)
        ans = None
        while True:
            if invalid_call and not ans in 'dw':
                print('Invalid call! Reenter')
            ans = input('Face value, Count for raise or [l]iar: ')
            m = match('(\d)[ ,]*(\d+)', ans)
            if m:
                new_call = tuple([int(n) for n in m.groups()])
                if check_call(new_call):
                    break
                invalid_call = True
            elif ans == 'l' and call[1]:
                new_call = None
                break
            elif ans == 'd':
                debug = not debug
                if debug:
                    show_table()
                invalid_call = True
            elif ans == 'w':
                wild_ones = not wild_ones
                print('Wild 1s mode', 'on' if wild_ones else 'off')
                invalid_call = True
    else:
        new_call = bot(p)

    if new_call:
        print(conjugate(p, 'raise'), new_call)
        call = new_call
        pi += 1
    else:
        print(conjugate(p, 'challenge'), players[pi-1].name)
        pi = is_lie()
        call = 1, 0
        roll()
    
print(conjugate(players[0], 'win') + '!')
