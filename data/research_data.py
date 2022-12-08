import sys

import numpy as np
from numpy.linalg import norm

def getTotalMoves(g, color):
    if len(g) % 2 == 0:
        return len(g) // 2
    elif color == 1:
        return (len(g) // 2) + 1
    elif color == 0:
        return len(g) // 2


def getCounts(g, pred, playerAccDict, playerNames):
    game_count = 0
    white_count = 0
    black_count = 0
    white_correct = 0
    black_correct = 0
    white = True

    for i in range(len(g)):
        game_count += 1
        if white:
            white_count += 1
        else:
            black_count += 1
        if g[i] == pred[i]:
            if white:
                white_correct += 1
            else:
                black_correct += 1
        white = not white
    # if printS:
    #     print(f'total: {(white_correct + black_correct)}/{game_count} ({round((white_correct + black_correct)/game_count, 2)})\n\twhite: {white_correct}/{white_count} ({round(white_correct/white_count, 2)})\n\tblack: {black_correct}/{black_count} ({round(black_correct/black_count, 2)})')
    #     print([[playerAccDict[playerNames[0]][0][0] + white_correct, playerAccDict[playerNames[0]][0][1] + white_count], playerAccDict[playerNames[0]][1]])

    playerAccDict[playerNames[0]] = [[playerAccDict[playerNames[0]][0][0] + white_correct, playerAccDict[playerNames[0]][0][1] + white_count], playerAccDict[playerNames[0]][1]]
    playerAccDict[playerNames[1]] = [playerAccDict[playerNames[1]][0], [playerAccDict[playerNames[1]][1][0] + black_correct, playerAccDict[playerNames[1]][1][1] + black_count]]

    return [game_count, white_count, black_count, white_correct, black_correct]


def getGames():
    file_name = './data/2008_SCT_LadiesOpen.pgn'
    f = open(file_name, "r")
    games = []
    game = []
    while f:
        line = f.readline()
        if line == "":
            break
        if line[0] != "[":
            preppedLineList = line.strip("\n").split()
            if len(preppedLineList) > 0:
                game = game + preppedLineList
            else:
                if "{" in game or len(game) == 0:
                    continue
                game = [x for x in game if "." not in x]
                games.append(game[:len(game) - 1])
                game = []
    f.close()
    return games


def getNames():
    file_name = './data/2008_SCT_LadiesOpen.pgn'
    f = open(file_name, "r")
    names = []
    match_names = []
    while f:
        line = f.readline()
        if line == "":
            break
        if line[0:7] == "[White ":
            white_name = eval(line.strip("\n")[7:len(line.strip("\n")) - 1])
            match_names.append(white_name)
        if line[0:7] == "[Black ":
            black_name = eval(line.strip("\n")[7:len(line.strip("\n")) - 1])
            match_names.append(black_name)
        if len(match_names) == 2:
            names.append(match_names)
            match_names = []
    f.close()
    return names


def getPredictionNames():
    file_name = "./data/maiastats.txt"
    f = open(file_name, "r")
    names_predictions = []
    match_names_predictions = []
    while f:
        line = f.readline()
        if line == "":
            break
        if line[0:7] == "[White ":
            white_name = eval(line.strip("\n")[7:len(line.strip("\n")) - 1])
            match_names_predictions.append(white_name)
        if line[0:7] == "[Black ":
            black_name = eval(line.strip("\n")[7:len(line.strip("\n")) - 1])
            match_names_predictions.append(black_name)
        if len(match_names_predictions) == 2:
            names_predictions.append(match_names_predictions)
            match_names_predictions = []
    f.close()
    return names_predictions


def getPredictionGames():
    file_name = "./data/maiastats.txt"
    f = open(file_name, "r")
    games_predictions = []
    while f:
        line = f.readline()
        if line == "":
            break
        if line[0:7] != "[White " and line[0:7] != "[Black " and line[0] != '\n':
            games_predictions.append(eval(line.strip('\n')))
    f.close()
    return games_predictions


def initDictionaryWithNames(names):
    d = {}
    for names_in_game in names:
        if names_in_game[0] not in d.keys():
            d[names_in_game[0]] = [[0, 0], [0, 0]]
        if names_in_game[1] not in d.keys():
            d[names_in_game[1]] = [[0, 0], [0, 0]]
    return d


def getData():
    games = getGames()
    names = getNames()
    games_predictions = getPredictionGames()
    names_predictions = getPredictionNames()
    games_count_dictionary = initDictionaryWithNames(names)

    global_game_count = 0
    global_white_count = 0
    global_black_count = 0
    global_white_correct = 0
    global_black_correct = 0

    for i in range(len(names)):
        if names[i][1] != names_predictions[i][1] or len(names) != len(names_predictions):
            # print("games and predictions do not match names or size")
            pass
    for i in range(len(games)):
        prediction_raw = games_predictions[i]
        game = games[i]
        if '#' in game[len(game) - 1]:
            prediction = prediction_raw[:len(prediction_raw)]
        else:
            prediction = prediction_raw[:len(prediction_raw) - 1]
        if len(prediction) != len(game):
            # print("games are different size!", "check game:", i)
            pass
        gameCounts = getCounts(games[i], prediction, games_count_dictionary, names[i])
        global_game_count += gameCounts[0]
        global_white_count += gameCounts[1]
        global_black_count += gameCounts[2]
        global_white_correct += gameCounts[3]
        global_black_correct += gameCounts[4]

    # print(games_count_dictionary)
    # print(f'global acc - no color {round((global_black_correct + global_white_correct) / global_game_count, 3)}')
    # print(f'global acc - white {round(global_white_correct / global_white_count, 3)}')
    # print(f'global acc - black {round(global_black_correct / global_black_count, 3)}')

    id_to_player = {}
    player_to_id = {}
    player_acc_dict = {}
    idx = 0
    for player in games_count_dictionary.keys():
        player_to_id[player] = idx
        id_to_player[idx] = player
        white_count = games_count_dictionary[player][0]
        black_count = games_count_dictionary[player][1]
        # print(player)
        acc_arr = []
        if (black_count[1] + white_count[1]) != 0:
            # print(f'\tacc - no color: {round((black_count[0] + white_count[0]) / (black_count[1] + white_count[1]), 3)}')
            acc_arr.append((black_count[0] + white_count[0]) / (black_count[1] + white_count[1]))
        else:
            # print(f'\tacc - no color: N/A')
            acc_arr.append(-1)
        if white_count[1] != 0:
            # print(f'\tacc - white: {round(white_count[0] / white_count[1], 3)}')
            acc_arr.append(white_count[0] / white_count[1])
        else:
            # print(f'\tacc - white: N/A')
            acc_arr.append(-1)
        if black_count[1] != 0:
            # print(f'\tacc - black: {round(black_count[0] / black_count[1], 3)}')
            acc_arr.append(black_count[0] / black_count[1])
        else:
            # print(f'\tacc - black: N/A')
            acc_arr.append(-1)
        player_acc_dict[player] = acc_arr
        idx += 1

    return player_acc_dict, games_count_dictionary

