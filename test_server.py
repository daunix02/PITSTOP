
import tempfile
import unittest
from pathlib import Path

from server import is_healthy


class HealthCheckTests(unittest.TestCase):
    def test_healthy_when_no_fault_exists(self):
        with tempfile.TemporaryDirectory() as directory:
            marker = Path(directory) / "fault"
            self.assertTrue(is_healthy(marker))

    def test_unhealthy_when_fault_exists(self):
        with tempfile.TemporaryDirectory() as directory:
            marker = Path(directory) / "fault"
            marker.touch()
            self.assertFalse(is_healthy(marker))

    def test_recovery_when_fault_is_removed(self):
        with tempfile.TemporaryDirectory() as directory:
            marker = Path(directory) / "fault"
            marker.touch()
            self.assertFalse(is_healthy(marker))
            marker.unlink()
            self.assertTrue(is_healthy(marker))


if __name__ == "__main__":
    unittest.main()
    