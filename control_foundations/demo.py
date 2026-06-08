"""Run a tiny policy-to-controller loop locally without ROS2."""

from .safety_filter import JointSafetyFilter
from .trajectory import interpolate


def main() -> None:
    current = [0.0, 0.0, 0.0]
    requested = [1.4, -0.8, 0.5]
    action_chunk = interpolate(current, requested, steps=5)
    safety = JointSafetyFilter(lower=[-1.0, -1.0, -1.0], upper=[1.0, 1.0, 1.0], max_velocity=[1.5, 1.5, 1.5])
    print("step | requested                 | safe action               | clipped")
    for step, action in enumerate(action_chunk, start=1):
        result = safety.filter(action, current, dt=0.1, now=step * 0.1)
        current = result.action
        clipped = result.clipped_positions + result.clipped_velocities
        print(f"{step:>4} | {str(action):<25} | {str(result.action):<25} | {clipped}")
    print(f"watchdog timed out at t=1.0s: {safety.timed_out(now=1.0)}")


if __name__ == "__main__":
    main()
