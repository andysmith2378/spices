from combo import Combination

TOMATO = 0, 1
PARSLEY = 1, 1
STOCK = 2, 2
ERYTHRITOL = 3, 2
MSG = 4, 2
MUSHROOM = 5, 2
IG = 6, 2
TEA = 7, 2
ONION = 8, 2
ANNATTO = 9, 2
SUMAC = 10, 2
BIRDSEYE = 11, 16
TURMERIC = 12, 2
CUMIN = 13, 2
CITRIC = 14, 8
CELERY_SEEDS = 15, 2
CAROB = 16, 2
BLACK_SALT = 17, 2
PAPRIKA = 18, 2
MUSTARD_POWDER = 19, 2
VINEGAR = 20, 4
AMCHUR = 21, 2
SOY_SAUCE = 22, 2
COCOA = 23, 2
PEPPER = 24, 2
CHILLI_FLAKES = 25, 4
HABANERO = 26, 32
CELERY_SALT = 27, 2
CINNAMON = 28, 2
GINGER = 29, 2
CARDAMOM = 30, 2
LEMON_PEPPER = 31, 2
CLOVES = 32, 2
FENNEL = 33, 2

COMBINATIONS = {
    "SUMLIN": Combination((TOMATO, 40), (PARSLEY, 24), (STOCK, 8), (ERYTHRITOL, 8), (MSG, 8), (MUSHROOM, 8), (IG, 4)),
    "TYRELL'S NIECE": Combination((TEA, 60), (STOCK, 8), (MSG, 8), (ONION, 8), (MUSHROOM, 8), (IG, 4)),
    "UBIK": Combination((ANNATTO, 52), (SUMAC, 12), (STOCK, 8), (MSG, 8), (MUSHROOM, 8), (ERYTHRITOL, 6), (IG, 4),
                        (BIRDSEYE, 2)),
    "LEMON DEGEORGE": Combination((TURMERIC, 35), (STOCK, 15), (CUMIN, 15), (MSG, 15), (MUSHROOM, 15), (CITRIC, 5),
                                  (IG, 5)),
    "THE BEAST RABBAN": Combination((CELERY_SEEDS, 20), (CAROB, 16), (ONION, 16), (MSG, 12), (MUSHROOM, 12),
                                    (ERYTHRITOL, 8), (BLACK_SALT, 4), (BIRDSEYE, 4), (CITRIC, 4), (IG, 4)),
    "INGSOC": Combination((ERYTHRITOL, 30), (PAPRIKA, 30), (MUSTARD_POWDER, 20), (BLACK_SALT, 10), (VINEGAR, 10)),
    "ATLASSIAN JIRA": Combination((AMCHUR, 1), (ERYTHRITOL, 1), (SOY_SAUCE, 1)),
    "28-82": Combination((COCOA, 48), (ERYTHRITOL, 40), (BLACK_SALT, 8), (BIRDSEYE, 4)),
    "ORANGE CLAW HAMMER": Combination((PEPPER, 20), (ANNATTO, 30), (SUMAC, 40), (BLACK_SALT, 10)),
    "NORSTRILIA": Combination((PEPPER, 1), (CELERY_SALT, 1), (CINNAMON, 1), (STOCK, 1), (CUMIN, 1), (GINGER, 1),
                              (CARDAMOM, 1), (ERYTHRITOL, 1), (LEMON_PEPPER, 1), (ONION, 1), (SUMAC, 1),
                              (TURMERIC, 1)),
    "FEYD RAUTHA": Combination((PEPPER, 25), (FENNEL, 25), (AMCHUR, 15), (ONION, 15), (CAROB, 15), (STOCK, 15)),
    "FLIBBERTY JIB": Combination((CLOVES, 40), (LEMON_PEPPER, 35), (PAPRIKA, 15), (PEPPER, 10)),
}