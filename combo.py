import math

class Combination(dict):
    distance = lambda x, y: 1.0 - sum([min(value, y[key]) for key, value in x.items() if key in y])

    def __init__(self, *keyValuePairs):
        valueTotal = float(sum([value * float(key[1]) for key, value in keyValuePairs]))
        dict.__init__(self, [(key, float(key[1]) * value / valueTotal) for key, value in keyValuePairs])

    @staticmethod
    def dist(x1, x2, y1, y2):
        x, y = x1 - x2, y1 - y2
        return math.sqrt(x * x + y * y)

    @staticmethod
    def combDist(comb1, comb2):
        return Combination.dist(comb1[0], comb2[0], comb1[1], comb2[1])

    @staticmethod
    def getVar(comb1, comb2, name1, name2, guess):
        squareroot = comb1.distance(comb2) - Combination.combDist(guess[name1], guess[name2])
        return squareroot * squareroot

    @staticmethod
    def getPosition(targetkey, coords1, coords2, firstkey, secondkey, guess):
        if firstkey == targetkey:
            return coords1
        if secondkey == targetkey:
            return coords2
        return guess[targetkey]