# Game mechanics to be used by game state manager.
from typing import List
from tile import Tile, Number
from itertools import combinations

# Defin meld


class Meld:
    """Three or four tiles that are the same or in sequence.
    self.suit must match,
    then numbers"""

    MELD_SIZE = 3
    KONG_SIZE = 4

    def __init__(self, tiles: List[Tile], meld_type: str):
        self.tiles = tiles
        self.meld_type = meld_type


class Meld_recognizer:
    # - pung chow kong pair

    # static methods as should NOT alter hands
    @staticmethod
    def isPong(tiles: List[Tile]) -> bool:
        if len(tiles) != 3:
            return False
        return tiles[0] == tiles[1] == tiles[2]

    @staticmethod
    def isChow(tiles: List[Tile]) -> bool:
        if len(tiles) != 3:
            return False

        # must be number tiles and same suit
        if not all(isinstance(tile, Number) for tile in tiles):
            return False
        if not all(tile.suit == tiles[0].suit for tile in tiles):
            return False

        # Check if consecutive values
        values = sorted([tile.value for tile in tiles])
        return values[1] == values[0] + 1 and values[2] == values[1] + 1

    @staticmethod
    def isKong(tiles: List[Tile]) -> bool:
        if len(tiles) != 4:
            return False

        return tiles[0] == tiles[1] == tiles[2] == tiles[3]

    @staticmethod
    def isPair(tiles: List[Tile]) -> bool:
        if len(tiles) != 2:
            return False
        return tiles[0] == tiles[1]

    @staticmethod
    def all_possible_melds(tiles: List[Tile]) -> List[Meld]:
        """For a list of tiles, check all melds
        When Meld matches create a new instance of Meld
        With tiles and type of meld"""
        melds = []

        # 4-tile melds (Kong)
        for combo in combinations(range(len(tiles)), 4):
            combo_tiles = [tiles[i] for i in combo]
            if Meld_recognizer.is_kong(combo_tiles):
                melds.append(Meld(combo_tiles, 'kong'))

        # 3-tile melds (Pung or Chow)
        for combo in combinations(range(len(tiles)), 3):
            combo_tiles = [tiles[i] for i in combo]
            if Meld_recognizer.is_pung(combo_tiles):
                melds.append(Meld(combo_tiles, 'pung'))
            elif Meld_recognizer.is_chow(combo_tiles):
                melds.append(Meld(combo_tiles, 'chow'))

        return melds
