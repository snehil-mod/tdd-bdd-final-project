import sys
import unittest
from unittest.mock import patch
from importlib import reload

class TestAppInitFailure(unittest.TestCase):
    def test_init_db_failure(self):
        """It should log and exit when init_db fails"""
        with patch("service.models.init_db", side_effect=Exception("DB error")), \
             patch("service.app.logger.critical") as mock_critical, \
             patch("sys.exit") as mock_exit:
            # Reload the module to trigger app init again with patched init_db
            import service
            reload(service)  # re-runs __init__.py logic

            mock_critical.assert_called()
            args, _ = mock_critical.call_args
            self.assertEqual(args[0], "%s: Cannot continue")
            self.assertIsInstance(args[1], Exception)
            self.assertEqual(str(args[1]), "DB error")
            mock_exit.assert_called_once_with(4)
