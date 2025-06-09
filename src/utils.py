from dataclasses import dataclass

from config_reader import CELL_SIZE


@dataclass(frozen=True, slots=True)
class Display:
    x: int
    y: int
    fps: int


@dataclass(frozen=True, slots=True)
class NoOutOfBoundsChecks:
    """
    Container for results of out-of-bounds checks.
    """
    x_pos: bool
    x_neg: bool
    y_pos: bool
    y_neg: bool

    def generally(self) -> bool:
        return self.x_pos and self.x_neg and self.y_pos and self.y_neg


class PartialOutOfBoundsChecks(NoOutOfBoundsChecks):
    """
    Container for results of "partial out-of-bounds" checks.
    """
    def generally(self) -> bool:
        return self.x_pos or self.x_neg or self.y_pos or self.y_neg


class NoOutOfBoundsChecker:
    def __init__(self, display: Display):
        self.display = display

    def check_movement(self, x: int, y: int) -> NoOutOfBoundsChecks:
        return NoOutOfBoundsChecks(
            x < self.display.x - CELL_SIZE, x > -1,
            y < self.display.y - CELL_SIZE, y > -1
        )
    

class PartialOutOfBoundsChecker:
    def __init__(self, display: Display):
        self.display = display

    def check_movement(self, x: int, y: int) -> PartialOutOfBoundsChecks:
        return PartialOutOfBoundsChecks(
            x > self.display.x + CELL_SIZE, x < -1,
            y > self.display.y + CELL_SIZE, y < -1
        )
    