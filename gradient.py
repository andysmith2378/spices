import math, copy, time
from score import total
from main import randomGuess, printIfYappy, BIG_FLOAT
from show import Graph

OUTFILE = "gradient.png"
LOGFILE = "gradientfalloff.csv"
YAPPY = False
INITIAL_SURVEY_DISTANCE, SURVEY_FALLOFF, DIRECTION_STRIDE = 0.01, 0.999, 1
MAX_SURVEYS, MAX_TIME = 100000, 3600

def initialGuess():
    error, best = randomGuess()
    leastError = error
    printIfYappy(", ".join([str(error), str(best)]))
    surveyDistance = INITIAL_SURVEY_DISTANCE
    if isinstance(DIRECTION_STRIDE, int):
        degreesRange = range(0, 360, DIRECTION_STRIDE)
    else:
        degreesRange = [DIRECTION_STRIDE * numerator for numerator in range(0, int(0.5 + 360.0 / DIRECTION_STRIDE))]
    return error, best, leastError, surveyDistance, degreesRange

def updateScore(leastError, bestDirection, unitVector):
    score = total(bestKeys, best)
    if score < leastError:
        leastError = score
        bestDirection[key] = unitVector
    return leastError

def checkDirection(degrees, leap, original, bestScore, bestDirection):
    angle = math.radians(degrees)
    unitVector = math.cos(angle), math.sin(angle)
    dx, dy = [leap * component for component in unitVector]
    best[key] = (original[key][0] + dx, original[key][1] + dy)
    return updateScore(bestScore, bestDirection, unitVector)

def updateError(bestKeys, best, leastError, loglines, startTime):
    error = total(bestKeys, best)
    printIfYappy(", ".join([str(error), str(best)]))
    loglines.append("".join([str(time.time() - startTime), ",", str(error), "\n"]))
    progress = error < leastError
    if progress:
        leastError = error
    return leastError

if __name__ == '__main__':
    startTime = time.time()
    error, best, leastError, leap, degreesRange = initialGuess()
    bestKeys, bestDirection, survey = list(best.keys()), {}, 0
    #graph = Graph(OUTFILE)
    surveyRange, loglines = range(1, MAX_SURVEYS+1), [("".join([str(time.time() - startTime),",", str(error), "\n"]))]
    for survey in surveyRange:
        if time.time() > (startTime + MAX_TIME):
            break
        original = copy.copy(best)
        leap *= SURVEY_FALLOFF
        for key in bestKeys:
            bestScore, bestDirection[key] = BIG_FLOAT, (0.0, 0.0)
            for degrees in degreesRange:
                bestScore = checkDirection(degrees, leap, original, bestScore, bestDirection)
        best, generation = original, 0
        if time.time() > (startTime + MAX_TIME):
            break
        printIfYappy("SURVEY", survey, "LEAP", leap)
        for key in bestKeys:
            best[key] = (best[key][0] + leap * bestDirection[key][0], best[key][1] + leap * bestDirection[key][1])
        leastError = updateError(bestKeys, best, leastError, loglines, startTime)
    with open(LOGFILE, "w") as logfile:
        logfile.writelines(loglines)