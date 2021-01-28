import pygame, random
from combo import Combination
from data import COMBINATIONS

MAX_DIVISIONS, DIVISION_BASE = 4, 2
OUTFILE = "double.png"
GRAPH_WIDTH, GRAPH_HEIGHT, OFFSET, GRAPH_FONT, FONT_SIZE = 800, 800, 200, 'GOTHIC.ttf', 20
MIN_INITIAL_TRIALS_EXPONENT = 4
BLUEBASE, MIN_COLOUR_COMPONENT = 1023.0, 192.0
BIG_FLOAT = float('inf')
YAPPY = True

def printIfYappy(*arguments):
    if YAPPY:
        print(*arguments)

def test(coords1, coords2, key1, key2, guessKeys, bestGuess, leastError, improvement):
    trialError = 0.0
    for outerKeyIndex, outerKey in enumerate(guessKeys):
        for innerKey in guessKeys[outerKeyIndex+1:]:
            argumentBlob = coords1, coords2, key1, key2, bestGuess
            variation = COMBINATIONS[outerKey].distance(COMBINATIONS[innerKey]) - Combination.combDist(
                Combination.getPosition(outerKey, *argumentBlob), Combination.getPosition(innerKey, *argumentBlob))
            trialError += variation * variation
    if trialError < leastError:
        leastError, improvement, bestGuess[key1], bestGuess[key2] = trialError, True, coords1, coords2
    return leastError, improvement

def initialGuess():
    leastError, bestGuess, combinationKeys, comItems = BIG_FLOAT, None, COMBINATIONS.keys(), list(COMBINATIONS.items())
    for trial in range(4 ** (DIVISION_BASE * max(MIN_INITIAL_TRIALS_EXPONENT, MAX_DIVISIONS))):
        error, guess = 0.0, dict([(comb, (random.random(), random.random())) for comb in combinationKeys])
        for indx, (name1, comb1) in enumerate(comItems):
            error += sum([Combination.getVar(comb1, comb2, name1, name2, guess) for name2, comb2 in comItems[indx+1:]])
        if error < leastError:
            leastError, bestGuess = error, guess
    printIfYappy("\n".join([str(bestGuess), str(leastError), '']))
    return leastError, bestGuess

def drawGraph(surf, guess, wide, high, blue, font):
    surf.fill((0, 0, 0), )
    [surf.blit(font.render(k, True, rgb(blue, x, y)), (int(wide * x), int(high * y))) for k, (x, y) in guess.items()]
    pygame.display.flip()
    pygame.image.save(surf, OUTFILE)

def rgb(blueFactor, x, y):
    red, green = 255.0 * x, 255.0 * y
    if red < MIN_COLOUR_COMPONENT and green < MIN_COLOUR_COMPONENT:
        return int(red), int(green), 255
    return int(red), int(green), max(0, int(BLUEBASE - blueFactor * max(red, green)))

if __name__ == '__main__':
    error, best = initialGuess()
    graphWidthLessOffset, graphHeightLessOffset = GRAPH_WIDTH - OFFSET, GRAPH_HEIGHT - OFFSET
    blueCoeff = BLUEBASE / 255.0
    pygame.init()
    nameFont = pygame.font.SysFont(GRAPH_FONT, FONT_SIZE, bold=True)
    screen, divisions = pygame.display.set_mode((GRAPH_WIDTH, GRAPH_HEIGHT),), 1
    for attempt in range(MAX_DIVISIONS):
        divisions *= DIVISION_BASE
        grain = 1.0 / divisions
        positions, progress = [division * grain for division in range(divisions+1)], True
        printIfYappy(divisions, "DIVISIONS")
        while progress:
            bestKeys, progress = list(best.keys()), False
            for keyIndex, k1 in enumerate(bestKeys):
                for k2 in bestKeys[keyIndex + 1:]:
                    for x1 in positions:
                        for y1 in positions:
                            for x2 in positions:
                                for y2 in positions:
                                    error, progress = test((x1, y1), (x2, y2), k1, k2, bestKeys, best, error, progress)
            printIfYappy(", ".join([str(error), str(best)]))
            drawGraph(screen, best, graphWidthLessOffset, graphHeightLessOffset, blueCoeff, nameFont)