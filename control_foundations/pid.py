"""Small PID controller used by the local control-loop exercises."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class PID:
    kp: float
    ki: float = 0.0
    kd: float = 0.0
    integral_limit: Optional[float] = None

    def __post_init__(self) -> None:
        self.integral = 0.0
        self.previous_error: Optional[float] = None

    def reset(self) -> None:
        self.integral = 0.0
        self.previous_error = None

    def update(self, target: float, measured: float, dt: float) -> float:
        if dt <= 0:
            raise ValueError("dt must be positive")

        error = target - measured
        self.integral += error * dt
        if self.integral_limit is not None:
            limit = abs(self.integral_limit)
            self.integral = max(-limit, min(limit, self.integral))

        derivative = 0.0
        if self.previous_error is not None:
            derivative = (error - self.previous_error) / dt
        self.previous_error = error

        return self.kp * error + self.ki * self.integral + self.kd * derivative
