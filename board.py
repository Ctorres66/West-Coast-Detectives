class Room:
    def __init__(self, name, image):
        self.name = name
        self.image = image

class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[None for _ in range(width)] for _ in range(height)]

    def add_room(self, room, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y][x] = room
        else:
            print("Invalid coordinates.")
