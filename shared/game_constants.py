
PORT = 5555

MAX_PLAYERS = 6

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

ROOM_WIDTH = 100
ROOM_HEIGHT = 100
CARD_WIDTH = 100
CARD_HEIGHT = 200

# constants for suspect names
SUSPECT = 'Suspect'

MUSTARD = 'Colonel Mustard'
SCARLET = 'Miss Scarlet'
PLUM = 'Professor Plum'
GREEN = 'Mr Green'
WHITE = 'Mrs White'
PEACOCK = 'Mrs Peacock'

SUSPECTS = [
    MUSTARD,
    SCARLET,
    PLUM,
    GREEN,
    WHITE,
    PEACOCK
]

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
