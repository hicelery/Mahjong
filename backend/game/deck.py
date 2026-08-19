from typing import List
from backend.game.tile import Tile, create_tile
import random


class Deck:
    """
    Manages the tile deck

    Standard Riichi Mahjong deck: 136 tiles total
    - 4 copies of each number tile (1-9 in 3 suits) = 108 tiles
    - 4 copies of each wind tile (N, E, S, W) = 16 tiles
    - 4 copies of each dragon tile (Red, Green, White) = 12 tiles
    """

    STANDARD_DECK_SIZE = 136
    DRAW_WALL_SIZE = 14
    # Dead wall for Kong compensation

    def __init__(self):
        """With type checking
        need to make dead wall?"""
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

        # make sure deck is correct length
        assert len(self.tiles) == self.STANDARD_DECK_SIZE, \
            f"Deck size mismatch: {len(self.tiles)} != {self.STANDARD_DECK_SIZE}"

    def shuffle_deck(self):
        """
        shuffle deck
        can counteract pseudo random
        with dice roll based hand formation
        """

        random.shuffle(self.tiles)

    def draw_tile(self) -> Tile:
        """
        take tile from the deck and return it

        this function will be called by hand/player
        """
        # handle empty deck
        if len(self.tiles) == 0:
            raise RuntimeError("Deck is empty!")

        # take last tile
        tile = self.tiles.pop()

        # add to used (necessary for furiten rules)
        self.used_tiles.append(tile)

        return tile

    def reset(self):
        """Reset deck to initial state"""
        self.tiles = []
        self.used_tiles = []
        self._initialize_deck()

    def __len__(self):
        return len(self.tiles)

    def __repr__(self):
        return f"Deck({len(self.tiles)} tiles remaining)"
