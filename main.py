#  Import Modules
import random


#  Functions
def chooseDifficulty():
    """Select the Minesweeper difficulty"""
    validChoice = False
    while not validChoice:
        print('Difficulty : (E)asy / (M)edium / (H)ard / e(X)treme')
        answer = input('Please select a difficulty setting: ')
        if answer.upper() not in ['E', 'M', 'H', 'X']:
            continue
        else:
            validChoice = True

    if answer.upper() == 'E':
        return 'Easy'
    elif answer.upper() == 'M':
        return 'Medium'
    elif answer.upper() == 'H':
        return 'Hard'
    else:
        return 'Extreme'


def createGameLogic(chosenDif, DIFFICULTY):
    logicList = []
    for row in range(DIFFICULTY[chosenDif]['Rows']):
        rowList = []
        for col in range(DIFFICULTY[chosenDif]['Cols']):
            rowList.append(' ')
        logicList.append(rowList)

    insertMines(chosenDif, DIFFICULTY, logicList)
    adjacentCells(logicList)

    return logicList


def insertMines(chosenDif, DIFFICULTY, gameLogic):
    """Randomly selects and positions the mines onto the game grid"""
    for mine in range(DIFFICULTY[chosenDif]['Mines']):
        validChoice = False
        while not validChoice:
            x = random.randint(0, DIFFICULTY[chosenDif]['Rows'] - 1)
            y = random.randint(0, DIFFICULTY[chosenDif]['Cols'] - 1)

            if gameLogic[x][y] == ' ':
                validChoice = True

        gameLogic[x][y] = 'X'


def adjacentCells(gameLogic):
    for x, row in enumerate(gameLogic):
        for y, cel in enumerate(row):
            if cel == ' ':
                cellCount = 0

                if x != 0:
                    if gameLogic[x - 1][y] == 'X':
                        cellCount += 1
                    if y != 0:
                        if gameLogic[x-1][y-1] == 'X':
                            cellCount += 1
                    if y != len(gameLogic[0]) - 1:
                        if gameLogic[x-1][y+1] == 'X':
                            cellCount += 1

                if y != 0:
                    if gameLogic[x][y - 1] == 'X':
                        cellCount += 1
                if y != len(gameLogic[0]) - 1:
                    if gameLogic[x][y + 1] == 'X':
                        cellCount += 1

                if x != len(gameLogic) - 1:
                    if gameLogic[x + 1][y] == 'X':
                        cellCount += 1
                    if y != 0:
                        if gameLogic[x+1][y-1] == 'X':
                            cellCount += 1
                    if y != len(gameLogic[0]) - 1:
                        if gameLogic[x+1][y+1] == 'X':
                            cellCount += 1
                if cellCount > 0:
                    gameLogic[x][y] = str(cellCount)


def createGameDict(gameLogic):
    ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    cellDict = {}
    for x, row in enumerate(gameLogic):
        for y, cell in enumerate(row):
            cellDict[(x, y)] = {'Cell Ref': ALPHABET[y]+str(x+1), 'Cell Value': gameLogic[x][y], 'Cell Vis': 'Hidden'}
    return cellDict


def makeSelection(gamedictionary):
    validChoice = False
    while not validChoice:
        answer = input('Please Select a Cell to uncover (A1) : ')
        for keys, values in gamedictionary.items():
            if answer in values['Cell Ref'] and values['Cell Vis'] == 'Hidden':
                validChoice = True
                answerGrid = keys
                print(answerGrid)
                break

    return answerGrid


def inputSelectionOntoGameLogic(selection, gameLogic, gameDict):
    x, y = selection
    if gameLogic[x][y] == ' ':
        gameLogic[x][y] = '_'

        gameDict[(x, y)]['Cell Vis'] = 'Visible'
        checkAllAdjacentCells(selection, gameLogic, gameDict)
    elif gameLogic[x][y].isdigit():
        gameDict[(x, y)]['Cell Vis'] = 'Visible'
    elif gameLogic[x][y] == 'X':
        gameDict[(x, y)]['Cell Vis'] = 'Visible'


def printGameScreen(gameLogic, gameDict):
    ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    print(' Minesweeper '.center(100, '_'))
    print('Cells Remaining: ')
    topLine = '   |'
    for i in range(len(gameLogic[0])):
        topLine += f' {ALPHABET[i]} |'
    print(topLine)
    rowLine = ''
    for i, row in enumerate(gameLogic):
        rowLine = f'{i+1}'.ljust(3, ' ') + '|'
        for j, cell in enumerate(row):
            if gameDict[(i, j)]['Cell Vis'] != 'Hidden':
                rowLine += f'{gameLogic[i][j]}'.center(3, ' ')+'|'
            else:
                rowLine += f' # |'
        print(rowLine)


def checkAllAdjacentCells(cellCoord, gameLogic, gameDict):
    x, y = cellCoord
    nx, ny = x, y

    if nx != 0:
        if gameLogic[nx-1][ny] == ' ' or gameLogic[nx-1][ny].isdigit()\
                and gameDict[(nx-1, ny)]['Cell Vis'] == 'Hidden':
            gameDict[(nx-1, ny)]['Cell Vis'] = 'Visible'
            if gameLogic[nx-1][ny] == ' ':
                gameLogic[nx-1][ny] = '_'
                checkAllAdjacentCells((nx-1, ny), gameLogic, gameDict)
        if ny != 0:
            if gameLogic[nx - 1][ny - 1] == ' ' or gameLogic[nx - 1][ny - 1].isdigit()\
                    and gameDict[(nx - 1, ny - 1)]['Cell Vis'] == 'Hidden':
                gameDict[(nx - 1, ny - 1)]['Cell Vis'] = 'Visible'
                if gameLogic[nx - 1][ny - 1] == ' ':
                    gameLogic[nx - 1][ny - 1] = '_'
                    checkAllAdjacentCells((nx - 1, ny -1), gameLogic, gameDict)
        if ny != len(gameLogic[0])-1:
            if gameLogic[nx - 1][ny + 1] == ' ' or gameLogic[nx - 1][ny + 1].isdigit()\
                    and gameDict[(nx - 1, ny + 1)]['Cell Vis'] == 'Hidden':
                gameDict[(nx - 1, ny + 1)]['Cell Vis'] = 'Visible'
                if gameLogic[nx - 1][ny + 1] == ' ':
                    gameLogic[nx - 1][ny + 1] = '_'
                    checkAllAdjacentCells((nx - 1, ny + 1), gameLogic, gameDict)

    if nx != len(gameLogic)-1:
        if gameLogic[nx+1][ny] == ' ' or gameLogic[nx+1][ny].isdigit()\
                and gameDict[(nx+1, ny)]['Cell Vis'] == 'Hidden':
            gameDict[(nx+1, ny)]['Cell Vis'] = 'Visible'
            if gameLogic[nx+1][ny] == ' ':
                gameLogic[nx + 1][ny] = '_'
                checkAllAdjacentCells((nx+1, ny), gameLogic, gameDict)
        if ny != 0:
            if gameLogic[nx + 1][ny - 1] == ' ' or gameLogic[nx + 1][ny - 1].isdigit()\
                    and gameDict[(nx + 1, ny - 1)]['Cell Vis'] == 'Hidden':
                gameDict[(nx + 1, ny - 1)]['Cell Vis'] = 'Visible'
                if gameLogic[nx + 1][ny - 1] == ' ':
                    gameLogic[nx + 1][ny - 1] = '_'
                    checkAllAdjacentCells((nx + 1, ny -1), gameLogic, gameDict)
        if ny != len(gameLogic[0])-1:
            if gameLogic[nx + 1][ny + 1] == ' ' or gameLogic[nx + 1][ny + 1].isdigit()\
                    and gameDict[(nx + 1, ny + 1)]['Cell Vis'] == 'Hidden':
                gameDict[(nx + 1, ny + 1)]['Cell Vis'] = 'Visible'
                if gameLogic[nx + 1][ny + 1] == ' ':
                    gameLogic[nx + 1][ny + 1] = '_'
                    checkAllAdjacentCells((nx + 1, ny + 1), gameLogic, gameDict)

    if ny != 0:
        if gameLogic[nx][ny - 1] == ' ' or gameLogic[nx][ny - 1].isdigit() \
                and gameDict[(nx, ny - 1)]['Cell Vis'] == 'Hidden':
            gameDict[(nx, ny - 1)]['Cell Vis'] = 'Visible'
            if gameLogic[nx][ny - 1] == ' ':
                gameLogic[nx][ny - 1] = '_'
                checkAllAdjacentCells((nx, ny - 1), gameLogic, gameDict)
    if ny != len(gameLogic[0]) - 1:
        if gameLogic[nx][ny + 1] == ' ' or gameLogic[nx][ny + 1].isdigit() \
                and gameDict[(nx, ny + 1)]['Cell Vis'] == 'Hidden':
            gameDict[(nx, ny + 1)]['Cell Vis'] = 'Visible'
            if gameLogic[nx][ny + 1] == ' ':
                gameLogic[nx][ny + 1] = '_'
                checkAllAdjacentCells((nx, ny + 1), gameLogic, gameDict)



def checkForWinLose(gameLogic, gameDict):
    TOTALMINES = DIFFICULTY[chooseDif]['Mines']
    TOTALCELLS = DIFFICULTY[chooseDif]['Rows']*DIFFICULTY[chooseDif]['Cols']
    AVCELLS = TOTALCELLS - TOTALMINES
    visibleCells = 0
    for values in gameDict.values():
        if values['Cell Vis'] != 'Hidden':
            visibleCells += 1
        if values['Cell Value'] == 'X' and values['Cell Vis'] != 'Hidden':
            print('KKKKKKKKKKKKKAAAAAAAAAAAAAAAAABBBBBBBBBBBBBBBOOOOOOOOOOOOOOOOMMMMMMMMMMMMMMM')
            return False
    if visibleCells == AVCELLS:
        print('Congratulations, You have won!!')
        return False
    else:
        return True

#  Dictionaries and Lists
DIFFICULTY = {
    'Easy': {'Rows': 10, 'Cols': 10, 'Mines': 10},
    'Medium': {'Rows': 15, 'Cols': 15, 'Mines': 20},
    'Hard': {'Rows': 20, 'Cols': 20, 'Mines': 40},
    'Extreme': {'Rows': 25, 'Cols': 25, 'Mines': 80},
}

#  Variables
chooseDif = chooseDifficulty()
gameLogic = createGameLogic(chooseDif, DIFFICULTY)
gameDict = createGameDict(gameLogic)


#  Call Functions


#  rungame

for _ in gameLogic:
    print(_)

RUNGAME = True
while RUNGAME:
    printGameScreen(gameLogic, gameDict)
    selection = makeSelection(gameDict)
    inputSelectionOntoGameLogic(selection, gameLogic, gameDict)
    RUNGAME = checkForWinLose(gameLogic, gameDict)
    printGameScreen(gameLogic, gameDict)