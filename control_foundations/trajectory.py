"""Trajectory helpers for action-chunk execution."""


def interpolate(start: list[float], target: list[float], steps: int) -> list[list[float]]:
    if len(start) != len(target):
        raise ValueError("start and target must have the same dimension")
    if steps <= 0:
        raise ValueError("steps must be positive")

    result = []
    for step in range(1, steps + 1):
        alpha = step / steps
        result.append([a + alpha * (b - a) for a, b in zip(start, target)])
    return result
