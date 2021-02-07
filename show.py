import pygame

WIDTH, HEIGHT, OFFSET, FONT, SIZE, BLUEBASE, MIN_COLOUR_COMPONENT = 800, 800, 200, 'GOTHIC.ttf', 20, 1023.0, 192.0
B = BLUEBASE / 255.0

class Graph(object):
    def __init__(self, outfile):
        pygame.init()
        self.x, self.y, self.outfile = WIDTH - OFFSET, HEIGHT - OFFSET, outfile
        self.font, self.screen = pygame.font.SysFont(FONT, SIZE, bold=True), pygame.display.set_mode((WIDTH, HEIGHT), )

    def etch(self, guess):
        self.screen.fill((0, 0, 0), )
        [self.screen.blit(self.font.render(k, True, Graph.rgb(B, x, y)), (int(self.x * x), int(self.y * y)))
         for k, (x, y) in guess.items()]
        pygame.display.flip()
        pygame.image.save(self.screen, self.outfile)

    @staticmethod
    def stretch(guess):
        guessValues = guess.values()
        xCoords, yCoords = [[coord[indx] for coord in guessValues] for indx in (0, 1)]
        minX = min(xCoords)
        minY = min(yCoords)
        xSpan = max(xCoords) - minX
        ySpan = max(yCoords) - minY
        xStretch = 1.0 if xSpan < 1.0 else 1.0 / xSpan
        yStretch = 1.0 if ySpan < 1.0 else 1.0 / ySpan
        result = {}
        for key, (x, y) in guess.items():
            result[key] = (xStretch * (x - minX), yStretch * (y - minY))
        return result

    @staticmethod
    def rgb(blueFactor, x, y):
        red, green = 255.0 * x, 255.0 * y
        if red < MIN_COLOUR_COMPONENT and green < MIN_COLOUR_COMPONENT:
            return int(red), int(green), 255
        return int(red), int(green), max(0, int(BLUEBASE - blueFactor * max(red, green)))
