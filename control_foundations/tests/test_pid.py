import unittest

from control_foundations.pid import PID


class PIDTest(unittest.TestCase):
    def test_proportional_response(self) -> None:
        controller = PID(kp=2.0)
        self.assertEqual(controller.update(target=1.0, measured=0.25, dt=0.1), 1.5)

    def test_rejects_invalid_dt(self) -> None:
        with self.assertRaises(ValueError):
            PID(kp=1.0).update(target=1.0, measured=0.0, dt=0.0)


if __name__ == "__main__":
    unittest.main()
