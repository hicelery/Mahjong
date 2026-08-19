
# hand.py
from typing import List, Dict
from backend.game.tile import Tile, Number


class Hand:
    """
    Represents a player's hand
    Typically holds 13 tiles (14 after drawing)
    """

    MAX_HAND_SIZE = 14
    NORMAL_HAND_SIZE = 13

    # init function
    def __init__(self):
        self.tiles: List[Tile] = []

    # add tile
    def add_tile(self, tile) -> Tile:

        if len(self.tiles) >= self.MAX_HAND_SIZE:
            raise RuntimeError(f"Hand already full!")
        self.append(tile)

    # remove tile
    def remove_tile(self, tile) -> Tile:
        if tile not in self.tiles:
            raise RuntimeError(f"Tile not in hand!")
        self.tiles.remove(tile)
        return tile

    # sort hand
    def sort_hand(self):
        def tile_order(tile):
            # Sort by: type (numbers < winds < dragons), then suit, then value
            type_order = {'number': 0, 'wind': 1, 'dragon': 2}
            suit_order = {'pin': 0, 'bamboo': 1,
                          'character': 2, 'wind': 3, 'dragon': 4}

            return (
                type_order.get(tile.tile_type.value, 99),
                suit_order.get(tile.suit.value, 99),
                tile.value
            )
        self.tiles.sort(key=tile_order)

    # get tile count

    def get_tile_count(self, tile: Tile) -> int:
        """Count how many of this tile type are in hand"""
        return self.tiles.count(tile)

    # check full

    def check_hand_is_full(self) -> bool:
        return len(self.tiles) == self.MAX_HAND_SIZE
