from random import randint
class Type:
    LONGPRESS = 0
    KEYDOWN = 1
    KEYUP = 2
    QUIT = 3
    REMOVE = 4
    RELOAD = 6

    @classmethod
    def text(cls, type):
        if type == cls.LONGPRESS:
            return 'Long Press'
        elif type == cls.KEYDOWN:
            return 'Push'
        elif type == cls.KEYUP:
            return 'Press'
        return ''

class Button:
    NONE = -1
    G1 = 1
    G2 = 2
    G3 = 3
    G4 = 4
    G5 = 5
    G6 = 6

    M1 = 7
    M2 = 8
    M3 = 9
    M4 = 10
    M5 = 11
    M6 = 12
    M7 = 13
    M8 = 14
    M9 = 15
    M10 = 16
    M11 = 17
    M12 = 18

    convertMap = {
        1: G1,
        2: G2,
        3: G3,
        4: G4,
        5: G5,
        6: G6,
        19: M1,
        20: M2,
        21: M3,
        22: M4,
        23: M5,
        24: M6,
        25: M7,
        26: M8,
        27: M9,
        28: M10,
        29: M11,
        30: M12
    }

    textMap = {
      G1: 'G1',
      G2: 'G2',
      G3: 'G3',
      G4: 'G4',
      G5: 'G5',
      G6: 'G6',
      M1: 'M1',
      M2: 'M2',
      M3: 'M3',
      M4: 'M4',
      M5: 'M5',
      M6: 'M6',
      M7: 'M7',
      M8: 'M8',
      M9: 'M9',
      M10: 'M10',
      M11: 'M11',
      M12: 'M12'
    }

    @classmethod
    def parse(cls, value):
        if value in cls.convertMap:
            return cls.convertMap[value]
        return 0

    @classmethod
    def text(cls, value):
        if value in cls.textMap:
            return cls.textMap[value]
        return ''

class Event:
    def __init__(self, type: Type, rawButton, func=None):
        self.button = Button.parse(rawButton)
        self.type = type
        self.id = randint(0, 100000)
        self.func = func

    def getButton(self):
        return self.button

    def getType(self):
        return self.type

    def getId(self):
        return id
