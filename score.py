from combo import Combination
from data import COMBINATIONS

def test(coord1, coord2, key1, key2, guessKeys, best, leastError, improvement):
    trialErr = 0.0
    for n, outer in enumerate(guessKeys):
        trialErr += sum([accumulate(best, coord1, coord2, inner, key1, key2, outer) for inner in guessKeys[n + 1:]])
    return improve(best, coord1, coord2, improvement, key1, key2, leastError, trialErr)

def total(guessKeys, best):
    trialErr = 0.0
    for n, outer in enumerate(guessKeys):
        for inner in guessKeys[n + 1:]:
            variation = Combination.distance(COMBINATIONS[outer], COMBINATIONS[inner]) - Combination.combDist(
                best[inner], best[outer])
            trialErr += variation * variation
    return trialErr

def replacementTotal(guessKeys, best, replacementKey, relpacementCoords):
    trialErr = 0.0
    for n, outer in enumerate(guessKeys):
        rightCoords = chooseCoords(best, outer, relpacementCoords, replacementKey)
        for inner in guessKeys[n + 1:]:
            variation = Combination.distance(COMBINATIONS[outer], COMBINATIONS[inner]) - Combination.combDist(
                chooseCoords(best, inner, relpacementCoords, replacementKey), rightCoords)
            trialErr += variation * variation
    return trialErr

def chooseCoords(best, outer, relpacementCoords, replacementKey):
    if outer == replacementKey:
        return relpacementCoords
    return best[outer]

def improve(bestGuess, coords1, coords2, improvement, key1, key2, leastError, trialError):
    if trialError < leastError:
        leastError, improvement, bestGuess[key1], bestGuess[key2] = trialError, True, coords1, coords2
    return leastError, improvement

def accumulate(bestGuess, coords1, coords2, rightKey, firstReplacement, secondReplacement, leftKey):
    argumentBlob = coords1, coords2, firstReplacement, secondReplacement, bestGuess
    variation = Combination.distance(COMBINATIONS[leftKey], COMBINATIONS[rightKey]) - Combination.combDist(
        Combination.getPosition(leftKey, *argumentBlob), Combination.getPosition(rightKey, *argumentBlob))
    return variation * variation

def testPair(coord1, coord2, key1, key2, guessKeys, bestGuess, leastError, improvement):
    err = 0.0
    for memb in key1, key2:
        err += sum([accumulate(bestGuess, coord1, coord2, key, key1, key2, memb) for key in guessKeys if memb != key])
    return improve(bestGuess, coord1, coord2, improvement, key1, key2, leastError, err)