"""Joint-action validation, clipping, rate limiting, and watchdog behavior."""

from dataclasses import dataclass
from time import monotonic
from typing import Optional


@dataclass
class SafetyResult:
    action: list[float]
    clipped_positions: int
    clipped_velocities: int


class JointSafetyFilter:
    def __init__(self, lower: list[float], upper: list[float], max_velocity: list[float], timeout_s: float = 0.2) -> None:
        if not (len(lower) == len(upper) == len(max_velocity)):
            raise ValueError("all joint-limit arrays must have the same dimension")
        if timeout_s <= 0:
            raise ValueError("timeout_s must be positive")
        self.lower = lower
        self.upper = upper
        self.max_velocity = max_velocity
        self.timeout_s = timeout_s
        self.last_command_time: Optional[float] = None

    def filter(self, requested: list[float], current: list[float], dt: float, now: Optional[float] = None) -> SafetyResult:
        if len(requested) != len(self.lower) or len(current) != len(self.lower):
            raise ValueError("action dimension does not match configured joints")
        if dt <= 0:
            raise ValueError("dt must be positive")
        safe = []
        clipped_positions = 0
        clipped_velocities = 0
        for request, measured, low, high, velocity in zip(requested, current, self.lower, self.upper, self.max_velocity):
            position_limited = max(low, min(high, request))
            clipped_positions += position_limited != request
            max_delta = abs(velocity) * dt
            delta = position_limited - measured
            velocity_limited = measured + max(-max_delta, min(max_delta, delta))
            clipped_velocities += velocity_limited != position_limited
            safe.append(velocity_limited)
        self.last_command_time = monotonic() if now is None else now
        return SafetyResult(safe, clipped_positions, clipped_velocities)

    def timed_out(self, now: Optional[float] = None) -> bool:
        if self.last_command_time is None:
            return True
        current_time = monotonic() if now is None else now
        return current_time - self.last_command_time > self.timeout_s
