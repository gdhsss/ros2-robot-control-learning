import unittest

from control_foundations.trajectory import interpolate


class TrajectoryTest(unittest.TestCase):
    def test_interpolation_reaches_target(self) -> None:
        result = interpolate([0.0, 0.0], [1.0, -1.0], steps=4)
        self.assertEqual(result[-1], [1.0, -1.0])
        self.assertEqual(result[0], [0.25, -0.25])


if __name__ == "__main__":
    unittest.main()
