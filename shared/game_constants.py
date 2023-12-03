SERVER_IP = 'Royas-MacBook-Air.local'
PORT = 5555

MIN_PLAYERS_REQUIRED = 2

ROWS, COLS = 5, 5
SQUARE_SIZE = 100

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
SCREEN_HEIGHT = 720

# Define dimensions for buttons
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 100
BUTTON_MARGIN = 50

# Define heights for notification area and card display
BOX_WIDTH = 380
BOX_HEIGHT = 300

BOARD_START_X = 300
BOARD_START_Y = 100

ROOM_SIZE = 100

CARD_WIDTH = 100
CARD_HEIGHT = 200

CARD_START_X = 850
CARD_START_Y = 450

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
KITCHEN = 'Kitchen'
BALLROOM = 'Ballroom'
CONSERVATORY = 'Conservatory'
BILLIARD_ROOM = 'Billiard Room'
LIBRARY = 'Library'
STUDY = 'Study'
HALL = 'Hall'
LOUNGE = 'Lounge'
DINING_ROOM = 'Dining Room'

ROOMS = [
    KITCHEN,
    BALLROOM,
    CONSERVATORY,
    BILLIARD_ROOM,
    LIBRARY,
    STUDY,
    HALL,
    LOUNGE,
    DINING_ROOM
]

ROOM_COORDS = {
    KITCHEN: (4, 4),
    BALLROOM: (4, 2),
    CONSERVATORY: (4, 0),
    BILLIARD_ROOM: (2, 2),
    LIBRARY: (2, 0),
    STUDY: (0, 0),
    HALL: (0, 2),
    LOUNGE: (0, 4),
    DINING_ROOM: (2, 4),
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
    STUDY_LIBRARY,
    STUDY_HALL,
    HALL_BILLIARD,
    HALL_LOUNGE,
    LOUNGE_DINING,
    LIBRARY_CONSERVATORY,
    LIBRARY_BILLIARD,
    BILLIARD_BALLROOM,
    BILLIARD_DINING,
    DINING_KITCHEN,
    CONSERVATORY_BALLROOM,
    BALLROOM_KITCHEN
]

# Constants for dropdown UI
DROPDOWN_X = 100
DROPDOWN_Y = 100
DROPDOWN_WIDTH = 200
DROPDOWN_HEIGHT = 150
DROPDOWN_BG_COLOR = (200, 200, 200)
OPTION_HEIGHT = 30
TEXT_COLOR = (0, 0, 0)
