import math
from typing import List, Tuple

class BoundaryLogic:
    def __init__(self, boundary_points: List[Tuple[float, float]], brick_size: Tuple[float, float]):
        """
        Handles edges and corners for brick placement.

        :param boundary_points: List of (x, y) tuples defining the boundary.
        :param brick_size: (length, width) of a standard brick.
        """
        self.boundary_points = boundary_points
        self.brick_length, self.brick_width = brick_size

    def snap_to_grid(self, x: float, y: float) -> Tuple[float, float]:
        """
        Snap a given (x, y) position to the nearest valid grid point.
        """
        snapped_x = round(x / self.brick_length) * self.brick_length
        snapped_y = round(y / self.brick_width) * self.brick_width
        return snapped_x, snapped_y

    def is_on_edge(self, x: float, y: float) -> bool:
        """
        Check if the given (x, y) coordinate is along the edge.
        """
        min_x = min(px for px, _ in self.boundary_points)
        max_x = max(px for px, _ in self.boundary_points)
        min_y = min(py for _, py in self.boundary_points)
        max_y = max(py for _, py in self.boundary_points)

        return x == min_x or x == max_x or y == min_y or y == max_y

    def is_corner(self, x: float, y: float) -> bool:
        """
        Determine if a given (x, y) coordinate is a corner.
        """
        min_x = min(px for px, _ in self.boundary_points)
        max_x = max(px for px, _ in self.boundary_points)
        min_y = min(py for _, py in self.boundary_points)
        max_y = max(py for _, py in self.boundary_points)

        return (x == min_x and y == min_y) or (x == max_x and y == min_y) or \
               (x == min_x and y == max_y) or (x == max_x and y == max_y)

    def staggered_offset(self, row: int) -> float:
        """
        Returns the horizontal offset for a given row to achieve staggered Flemish bond.
        - Even rows: No offset
        - Odd rows: Half-brick offset
        """
        return (self.brick_length / 2) if row % 2 == 1 else 0
