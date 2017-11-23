import os
import unittest

import logging
from configparser import MissingSectionHeaderError

from logmodule import UdpHandlerError
from logmodule import get_logger


class TestGetLogger(unittest.TestCase):
    def test_valid_conf_path_input(self):
        """Test get_logger with valid input"""

        logger = get_logger("config-valid.conf")

        self.assertTrue(isinstance(logger, logging.Logger))

    def test_invalid_conf_path_raises_error(self):
        with self.assertRaises(UdpHandlerError):
            get_logger("invalid.conf")

    def test_valid_conf_env_var_path_input(self):
        os.environ["LOGSTASH_CONFIG"] = "config-valid.conf"
        get_logger()

    def test_no_conf_raises_error(self):
        with self.assertRaises(UdpHandlerError):
            get_logger()

    def test_invalid_conf_file_invalid_handler_raises_error(self):
        with self.assertRaises(ImportError):
            get_logger("config-invalid-handler-name.conf")

    def test_invalid_conf_file_malformed_file_raises_error(self):
        with self.assertRaises(MissingSectionHeaderError):
            get_logger("config-invalid-malformed.conf")
