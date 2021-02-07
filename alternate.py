import random, time, copy, math
from combo import Combination
from data import COMBINATIONS
from score import test, total

TIME_LIMIT = (2, 20)
MAX_DIVISIONS, DIVISION_BASE, MAX_TIME = 4, 2, 600
OUTFILE = "alternate.png"
LOGFILE = "alternate220.csv"
MIN_INITIAL_TRIALS_EXPONENT = 4
BIG_FLOAT = float('inf')
YAPPY = True
TEST_METHOD = test
INITIAL_SURVEY_DISTANCE, SURVEY_FALLOFF, DIRECTION_STRIDE = 0.01, 0.999, 1

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
    printIfYappy("TIME FROM START", time.time() - startTime)
    return segments, [division * grain for division in range(segments + 1)], True

def initialGuess(error, best):
    leastError = error
    printIfYappy(", ".join([str(error), str(best)]))
    if isinstance(DIRECTION_STRIDE, int):
        degreesRange = range(0, 360, DIRECTION_STRIDE)
    else:
        degreesRange = [DIRECTION_STRIDE * numerator for numerator in range(0, int(0.5 + 360.0 / DIRECTION_STRIDE))]
    return error, best, leastError, degreesRange

def updateScore(key, leastError, bestDirection, unitVector):
    score = total(bestKeys, best)
    if score < leastError:
        leastError = score
        bestDirection[key] = unitVector
    return leastError

def updateError(bestKeys, best, leastError, loglines, startTime):
    error = total(bestKeys, best)
    printIfYappy(", ".join([str(error), str(best)]))
    loglines.append("".join([str(time.time() - startTime), ",", str(error), "\n"]))
    progress = error < leastError
    if progress:
        leastError = error
    return leastError

def checkDirection(key, degrees, leap, original, bestScore, bestDirection):
    angle = math.radians(degrees)
    unitVector = math.cos(angle), math.sin(angle)
    dx, dy = [leap * component for component in unitVector]
    best[key] = (original[key][0] + dx, original[key][1] + dy)
    return updateScore(key, bestScore, bestDirection, unitVector)

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

def doubleSection(best, divisions, positions, narrowDiv, error, sectionStart, startTime, loglines):
    if narrowDiv:
        divisions, positions, prog = divide(divisions, startTime)
    else:
        prog = True
    printIfYappy(divisions, "DIVISIONS")
    while prog:
        if time.time() > (sectionStart + TIME_LIMIT[0]):
            narrowDiv = False
            break
        error, prog = movePair(error, best, positions, loglines, startTime)
        printIfYappy(", ".join([str(error), str(best)]))
        loglines.append("".join([str(time.time() - startTime), ",", str(error), "\n"]))
        narrowDiv = True
    return divisions, positions, narrowDiv, error, best

def gradientSection(leap, best, bestKeys, leastError, secStart):
    while time.time() <= (secStart + TIME_LIMIT[1]):
        original = copy.copy(best)
        leap *= SURVEY_FALLOFF
        for key in bestKeys:
            bestScore, bestDirection[key] = BIG_FLOAT, (0.0, 0.0)
            for degrees in degreesRange:
                bestScore = checkDirection(key, degrees, leap, original, bestScore, bestDirection)
        best = original
        if time.time() > (secStart + MAX_TIME):
            break
        printIfYappy("LEAP", leap)
        for key in bestKeys:
            best[key] = (best[key][0] + leap * bestDirection[key][0], best[key][1] + leap * bestDirection[key][1])
        leastError = updateError(bestKeys, best, leastError, loglines, startTime)
    return best, leastError

if __name__ == '__main__':
    startTime, divs = time.time(), 1
    err, best = randomGuess()
    loglines = [("".join([str(time.time() - startTime),",", str(err), "\n"]))]
    leap, narrow, pos = INITIAL_SURVEY_DISTANCE, True, None
    while time.time() <= (startTime + MAX_TIME):
        secStart = time.time()
        while time.time() <= (secStart + TIME_LIMIT[0]):
            divs, pos, narrow, err, best = doubleSection(best, divs, pos, narrow, err, secStart, startTime, loglines)
        secStart = time.time()
        err, best, leastError, degreesRange = initialGuess(err, best)
        bestKeys, bestDirection = list(best.keys()), {}
        loglines.append("".join([str(time.time() - startTime),",", str(err), "\n"]))
        best, err = gradientSection(leap, best, bestKeys, leastError, secStart)
        guessValues = best.values()
        minX, minY = [min([coord[indx] for coord in guessValues]) for indx in (0, 1)]
        for key, (x, y) in best.items():
            best[key] = (x - minX, y - minY)
    with open(LOGFILE, "w") as logfile:
        logfile.writelines(loglines)







