from enum import Enum
from typing import List


class TileType(Enum):
    """Enumerate all tile types"""
    NUMBER = "number"        # 1-9 of pin, bamboo, character
    WIND = "wind"            # N, E, S, W
    DRAGON = "dragon"        # Red, Green, White
    FLOWER = "flower"        # Optional seasonal tiles
    SEASON = "season"        # Optional seasonal tiles


class Suit(Enum):
    """Enumerate suits"""
    PIN = "pin"
    BAMBOO = "bamboo"
    CHARACTER = "character"
    WIND = "wind"
    DRAGON = "dragon"
    FLOWER = "flower"        # Optional
    SEASON = "season"        # Optional


class Tile:
    """Base tile class with proper attributes"""

    def __init__(self, tile_type: TileType,
                 suit: Suit,
                 value: int,
                 display_name: str):
        self.tile_type = tile_type
        self.suit = suit
        self.value = value
        self.display_name = display_name


class Wind(Tile):
    """Wind tiles for NESW
    wind_code is N, E, S, W which is unpacked into
    str, value pair for use in tile class"""
    WINDS = {
        'N': ('North', 0),
        'E': ('East', 1),
        'S': ('South', 2),
        'W': ('West', 3)
    }

    def __init__(self, wind_code: str):
        display_name, value = self.WINDS[wind_code]
        super.__init__(TileType.WIND, Suit.WIND, value, display_name)
        self.wind_code = wind_code


class Dragon(Tile):
    """Dragon tiles
    Takes RGW and unpacks into colour and value.
    Use Pythonic notation"""
    DRAGONS = {
        'R': ('Red Dragon', 0),
        'G': ('Green Dragon', 1),
        'W': ('White Dragon', 2),
    }

    def __init__(self, dragon_code: str):
        display_name, value = self.DRAGONS[dragon_code]
        super().__init__(TileType.DRAGON, Suit.DRAGON, value, display_name)
        self.dragon_code = dragon_code


class Number(Tile):
    """Number Tiles 1-9 of pin, bamboo, char"""

    # check for value valid
    def __init__(self, suit: str, value: int):
        if not 1 <= value <= 9:
            raise ValueError("Invalid value!")
        if suit not in ['pin', 'bamboo', 'character']:
            raise ValueError("Invalid suit!")

        suit_enum = Suit(suit)
        display_name = f"{value} {suit.capitalize()}"
        super.__init__(TileType.NUMBER, suit_enum, value, display_name)


# helper function to create tiles
def create_tile(tile_code: str) -> Tile:
    """Create a tile from two char code
    1p -> One of Pins
    Follows mahjong notation (1-7 honor)"""

    if len(tile_code) != 2:
        raise ValueError("Invalid Tile Code!")

    # get value and suit from code
    value_code = tile_code[:-1]
    suit_code = tile_code[-1]

    suit_map = {
        'p': ('pin', TileType.NUMBER),
        's': ('bamboo', TileType.NUMBER),
        'm': ('character', TileType.NUMBER),
        'z': None  # honor tiles
    }

    if suit_code == 'z':
        value = int(value_code)
        if value in [1, 2, 3, 4]:  # Winds
            wind_map = {1: 'E', 2: 'S', 3: 'W', 4: 'N'}
            return Wind(wind_map[value])
        elif value in [5, 6, 7]:  # Dragons
            dragon_map = {5: 'G', 6: 'R', 7: 'W'}
            return Dragon(dragon_map[value])
    else:
        suit_name, _ = suit_map[suit_code]
        value = int(value_code)
        return Number(suit_name, value)


class Deck:
    """Deck class. Use create tile helper to loop through suit and value
    136 tiles, 4 each number, 3 each honors"""

    def __init__(self):
        """With type checking"""
        self.tiles: List[Tile] = []
        self.used_tiles: List[Tile] = []
        self._create_deck()

    def _create_deck(self):
        for i in range(1, 10):
            for _ in range(4):
                # create number tiles with helper function
                self.tiles.append(create_tile(f"{i}p"))
                self.tiles.append(create_tile(f"{i}s"))
                self.tiles.append(create_tile(f"{i}m"))
        for i in range(1, 8):
            for _ in range(3):
                # create honor tiles with helper function
                self.tiles.append(create_tile(f"{i}z"))

    # Create shuffle func
    # Draw func
    # Discard func
    # Create dead wall
