class Bolts:
    x = 0
    y = 0
    speed = -13  # constant
    bolt_width = 5  # constant
    bolt_height = 23  #constant
    isPlayers = False

    # constructor
    def __init__(self, x, y, players=False):
        self.x = x
        self.y = y
        self.isPlayers = players

    # move up or down depend on shooter
    def move(self):
        if self.isPlayers:
            self.y += self.speed
        else:
            self.y -= self.speed
