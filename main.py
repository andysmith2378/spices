import random, time
from combo import Combination
from data import COMBINATIONS
from score import test, testPair
from show import Graph

MAX_DIVISIONS, DIVISION_BASE, MAX_TIME = 4, 2, 18000
OUTFILE = "double.png"
LOGFILE = "double204.csv"
MIN_INITIAL_TRIALS_EXPONENT = 4
BIG_FLOAT = float('inf')
YAPPY = True
TEST_METHOD = test

def printIfYappy(*arguments):
    if YAPPY:
        print(*arguments)

def randomGuess(leastError=BIG_FLOAT, bestGuess=None):
    combinationKeys, comItems = COMBINATIONS.keys(), list(COMBINATIONS.items())
    for trial in range(int(4 ** (DIVISION_BASE * max(MIN_INITIAL_TRIALS_EXPONENT, MAX_DIVISIONS-1)))):
        error, guess = 0.0, dict([(comb, (random.random(), random.random())) for comb in combinationKeys])
        for indx, (name1, comb1) in enumerate(comItems):
            error += sum([Combination.getVar(comb1, comb2, name1, name2, guess) for name2, comb2 in comItems[indx+1:]])
        if error < leastError:
            leastError, bestGuess = error, guess
    printIfYappy("\n".join([str(bestGuess), str(leastError), '']))
    return leastError, bestGuess

def divide(segments, startTime, base=DIVISION_BASE):
    segments = int(segments * base)
    grain = 1.0 / segments
    printIfYappy(segments, "DIVISIONS")
    printIfYappy("TIME FROM START", time.time() - startTime)
    return segments, [division * grain for division in range(segments + 1)], True

def movePair(error, best, positionList, loglines, startTime):
    bestKeys, progress = list(best.keys()), False
    for keyIndex, k1 in enumerate(bestKeys):
        for k2 in bestKeys[keyIndex + 1:]:
            for x1 in positionList:
                for y1 in positionList:
                    for x2 in positionList:
                        for y2 in positionList:
                            error, progress = TEST_METHOD((x1, y1), (x2, y2), k1, k2, bestKeys, best, error, progress)
        loglines.append("".join([str(time.time() - startTime), ",", str(error), "\n"]))
    return error, progress

if __name__ == '__main__':
    #graph = Graph(OUTFILE)
    startTime, divisions = time.time(), 1
    error, best = randomGuess()
    loglines = [("".join([str(time.time() - startTime),",", str(error), "\n"]))]
    for attempt in range(MAX_DIVISIONS):
        if time.time() > (startTime + MAX_TIME):
            break
        divisions, positions, prog = divide(divisions, startTime)
        while prog:
            if time.time() > (startTime + MAX_TIME):
                break
            error, prog = movePair(error, best, positions, loglines, startTime)
            printIfYappy(", ".join([str(error), str(best)]))
            #graph.etch(bestGuess)
            loglines.append("".join([str(time.time() - startTime), ",", str(error), "\n"]))
    with open(LOGFILE, "w") as logfile:
        logfile.writelines(loglines)