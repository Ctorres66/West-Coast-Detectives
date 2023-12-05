SERVER_IP = 'Royas-MacBook-Air.local'
PORT = 5555

ROWS, COLS = 5, 5

# Define colors using RGB tuples
COLOR_RED = (255, 0, 0)
COLOR_YELLOW = (255, 255, 0)
COLOR_MAGENTA = (255, 0, 255)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_PURPLE = (75, 0, 130)
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_GRAY = (128, 128, 128)
DEFAULT_TEXT_COLOR = (0, 0, 0)

# Define your screen dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 800

# Define dimensions for buttons
BUTTON_START_X = 50
BUTTON_START_Y = 60
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 80
BUTTON_MARGIN = 25

# Define heights for notification area and card display
BOX_START_X = 850
BOX_START_Y = 60
BOX_WIDTH = 380
BOX_HEIGHT = 500

BOARD_START_X = 300
BOARD_START_Y = 60

BOARD_SIZE = 500

ROOM_SIZE = 100

CARD_WIDTH = 100
CARD_HEIGHT = 150

CARD_START_X = 300
CARD_START_Y = 580

PADDING = 10
TEXT_HEIGHT = 20  # Height for each text line

# constants for suspect names
SUSPECT = 'Suspect'

SCARLET = 'SC'
MUSTARD = 'CM'
PLUM = 'PL'
GREEN = 'GR'
WHITE = 'WH'
PEACOCK = 'PE'

SUSPECTS = [
    SCARLET,
    MUSTARD,
    PLUM,
    GREEN,
    WHITE,
    PEACOCK
]

# Dictionary mapping each suspect to their starting position
STARTING_POSITIONS = {
    SCARLET: (0, 3),  # Replace with actual coordinates or room identifiers
    MUSTARD: (1, 4),
    PLUM: (1, 0),
    GREEN: (4, 1),
    WHITE: (4, 3),
    PEACOCK: (3, 0),
    # Add other characters if needed
}

# constants for weapon names
WEAPON = 'Weapon'

ROPE = 'Rope'
LEAD_PIPE = 'Lead Pipe'
KNIFE = 'Knife'
WRENCH = 'Wrench'
CANDLESTICK = 'Candlestick'
REVOLVER = 'Revolver'

WEAPONS = [
    ROPE,
    LEAD_PIPE,
    KNIFE,
    WRENCH,
    CANDLESTICK,
    REVOLVER
]

# constants for rooms
ROOM = 'Room'

ROOMS = [
    'Kitchen',
    'Ballroom',
    'Conservatory',
    'Billiard Room',
    'Library',
    'Study',
    'Hall',
    'Lounge',
    'Dining Room'
]

ROOM_COORDS = {
    (4, 4): 'Kitchen',
    (4, 2): 'Ballroom',
    (4, 0): 'Conservatory',
    (2, 2): 'Billiard Room',
    (2, 0): 'Library',
    (0, 0): 'Study',
    (0, 2): 'Hall',
    (0, 4): 'Lounge',
    (2, 4): 'Dining Room',
}


# constants for hallways
STUDY_LIBRARY = 'study-library hallway'
STUDY_HALL = 'study-hall hallway'
HALL_BILLIARD = 'hall-billiard hallway'
HALL_LOUNGE = 'hall-lounge hallway'
LOUNGE_DINING = 'lounge-dining hallway'
LIBRARY_CONSERVATORY = 'library-conservatory hallway'
LIBRARY_BILLIARD = 'library-billiard hallway'
BILLIARD_BALLROOM = 'billiard-ballroom hallway'
BILLIARD_DINING = 'billiard-dining hallway'
DINING_KITCHEN = 'dining-kitchen hallway'
CONSERVATORY_BALLROOM = 'conservatory-ballroom hallway'
BALLROOM_KITCHEN = "ballroom-kitchen hallway"

HALLWAYS = [
    'study-library hallway',
    'study-hall hallway',
    'hall-billiard hallway',
    'hall-lounge hallway',
    'lounge-dining hallway',
    'library-conservatory hallway',
    'library-billiard hallway',
    'billiard-ballroom hallway',
    'billiard-dining hallway',
    'dining-kitchen hallway',
    'conservatory-ballroom hallway',
    'ballroom-kitchen hallway'
]

HALLWAYS_COORDS = {
    (1, 0): 'study-library hallway',
    (0, 1): 'study-hall hallway',
    (1, 2): 'hall-billiard hallway',
    (0, 3): 'hall-lounge hallway',
    (1, 4): 'lounge-dining hallway',
    (3, 0): 'library-conservatory hallway',
    (2, 1): 'library-billiard hallway',
    (3, 2): 'billiard-ballroom hallway',
    (2, 3): 'billiard-dining hallway',
    (3, 4): 'dining-kitchen hallway',
    (4, 1): 'conservatory-ballroom hallway',
    (4, 3): 'ballroom-kitchen hallway'
}

# Constants for dropdown UI
DROPDOWN_X = 100
DROPDOWN_Y = 100
DROPDOWN_WIDTH = 200
DROPDOWN_HEIGHT = 150
DROPDOWN_BG_COLOR = (200, 200, 200)
OPTION_HEIGHT = 30
TEXT_COLOR = (0, 0, 0)
