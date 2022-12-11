from django.shortcuts import render
from django.http import JsonResponse

import random
import json

GAME_STATE = {}
RANDOM_STATE = {}
CUR_PLAYER = {}
TERMINATE = {}
COLS = [[x for x in range(s, s + 21, 5)] for s in range(5)]
ROWS = [[x for x in range(s, s + 5)] for s in range(0, 21, 5)]
DIAG = [[4*x for x in range(1,6)], [6*x for x in range(5)]]


# Create your views here.
def start(request, me, oppo):
    randomState = list(range(1, 26))
    random.shuffle(randomState)
    RANDOM_STATE[me] = randomState
    players = min(me, oppo) + max(me, oppo)
    CUR_PLAYER[players] = max(me, oppo)
    context = {
        "me": me,
        "oppo": oppo,
        'randomState': randomState
    }
    if players in GAME_STATE:
        context['gamestate'] = GAME_STATE[players]
    else:
        context['gamestate'] = {}

    return render(request, 'game/playground.html', context=context)

def processGameState(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode())

        players = min(data['me'], data['oppo']) + max(data['me'], data['oppo'])
        if players in GAME_STATE:
            GAME_STATE[players].append(int(data['clicked']))
        else:
            GAME_STATE[players] = [int(data['clicked'])]

        CUR_PLAYER[players] = data['oppo']
    
    return JsonResponse(
        {"Foo": "Bar"}
    )

def check_Status(player, players):
    WIN_STATE = []
    
    for row in ROWS:
        ran = []
        for cell in row:
            if RANDOM_STATE[player][cell] not in GAME_STATE[players]:
                break
            ran.append(RANDOM_STATE[player][cell])
        else:
            WIN_STATE.append(ran)

    for col in COLS:
        ran = []
        for cell in col:
            if RANDOM_STATE[player][cell] not in GAME_STATE[players]:
                break
            ran.append(RANDOM_STATE[player][cell])
        else:
            WIN_STATE.append(ran)

    for diag in DIAG:
        ran = []
        for cell in diag:
            if RANDOM_STATE[player][cell] not in GAME_STATE[players]:
                break
            ran.append(RANDOM_STATE[player][cell])
        else:
            WIN_STATE.append(ran)
        
    return WIN_STATE

def refGame(request, me, oppo):
    players = min(me, oppo) + max(me, oppo)
    if players not in GAME_STATE:
        GAME_STATE[players] = []
    
    WIN_STATE_ME = check_Status(me, players)
    WIN_STATE_OPPO = check_Status(oppo, players)

    data = {
        "gamestate": GAME_STATE[players],
        "winstate": WIN_STATE_ME,
        "curplayer": CUR_PLAYER[players]
    }

    if len(WIN_STATE_OPPO) >= 5:
        data['curplayer'] = 'gameover' + oppo
        TERMINATE[me] = True

    if len(WIN_STATE_ME) >= 5:
        data['curplayer'] = 'gameover' + me
        TERMINATE[me] = True
    
    if me in TERMINATE and TERMINATE[me] and oppo in TERMINATE and TERMINATE[oppo]:
        GAME_STATE[players] = []
        CUR_PLAYER[players] = ''
        RANDOM_STATE[me] = []
        RANDOM_STATE[oppo] = []

    return JsonResponse(
        data
    )