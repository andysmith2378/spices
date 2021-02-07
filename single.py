import random, time
from score import replacementTotal
from show import Graph
from main import printIfYappy, randomGuess, divide, BIG_FLOAT

MAX_DIVISIONS, MAX_TIME = 100, 3600
DIVISION_BASE = 4
OUTFILE = "single.png"
LOGFILE = "single404.csv"
YAPPY = True

def moveSingle(leastError, bestGuess, positionList, loglines, startTime):
    err, keyList, progress, oneToMove, placeToGo = BIG_FLOAT, list(bestGuess.keys()), False, None, None
    for chosenOne in keyList:
        for x in positionList:
            for y in positionList:
                err = replacementTotal(keyList, bestGuess, chosenOne, (x, y))
                if err < leastError:
                    leastError, progress, oneToMove, placeToGo = err, True, chosenOne, (x, y)
        loglines.append("".join([str(time.time() - startTime), ",", str(leastError), "\n"]))
    return leastError, progress, oneToMove, placeToGo

def logGuess(loglines, startTime):
    error, best = randomGuess()
    loglines.append("".join([str(time.time() - startTime), ",", str(error), "\n"]))
    return error, best

if __name__ == '__main__':
    #graph = Graph(OUTFILE)
    startTime, divisions, loglines = time.time(), 1, []
    error, best = logGuess(loglines, startTime)
    oldError = BIG_FLOAT
    while error < oldError:
        oldError = error
        error, best = logGuess(loglines, startTime)
    for attempt in range(MAX_DIVISIONS):
        if time.time() > (startTime + MAX_TIME):
            break
        divisions, positions, prog = divide(divisions, startTime, DIVISION_BASE)
        while prog:
            if time.time() > (startTime + MAX_TIME):
                break
            error, prog, oneToMove, placeToGo = moveSingle(error, best, positions, loglines, startTime)
            if prog:
                best[oneToMove] = placeToGo
            printIfYappy(", ".join([str(prog), str(error), str(best)]))
            #graph.etch(bestGuess)
            loglines.append("".join([str(time.time() - startTime), ",", str(error), "\n"]))
    with open(LOGFILE, "w") as logfile:
        logfile.writelines(loglines)