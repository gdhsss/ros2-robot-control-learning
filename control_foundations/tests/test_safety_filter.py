import unittest

from control_foundations.safety_filter import JointSafetyFilter


class SafetyFilterTest(unittest.TestCase):
    def setUp(self) -> None:
        self.filter = JointSafetyFilter(lower=[-1.0, -1.0], upper=[1.0, 1.0], max_velocity=[0.5, 1.0], timeout_s=0.2)

    def test_clips_position_and_velocity(self) -> None:
        result = self.filter.filter([2.0, -0.5], [0.0, 0.0], dt=0.1, now=0.0)
        self.assertEqual(result.action, [0.05, -0.1])
        self.assertEqual(result.clipped_positions, 1)
        self.assertEqual(result.clipped_velocities, 2)

    def test_watchdog(self) -> None:
        self.assertTrue(self.filter.timed_out(now=0.0))
        self.filter.filter([0.0, 0.0], [0.0, 0.0], dt=0.1, now=1.0)
        self.assertFalse(self.filter.timed_out(now=1.1))
        self.assertTrue(self.filter.timed_out(now=1.3))


if __name__ == "__main__":
    unittest.main()
