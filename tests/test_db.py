"""
These tests test the workflow of the database, creating and dropping tables and
adding various elements to the tables.

@author Kevin Wilson - khwilson@gmail.com
"""
import os
import subprocess
import tempfile
import unittest

from reading import config


class TestDatabase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.tmp_config = config.Config()
        cls.tmp_config.database.scheme = 'sqlite'
        cls.tmpfile = tempfile.mkstemp()[1]
        cls.tmpdb = tempfile.mkstemp()[1]
        cls.tmp_config.database.host = cls.tmpdb
        # raise ValueError
        with open(cls.tmpfile, 'w') as f:
            f.write(config.dump_config(config))

    @classmethod
    def tearDownClass(cls):
        # raise ValueError
        os.unlink(cls.tmpfile)
        os.unlink(cls.tmpdb)

    def test_create_tables(self):
        subprocess.Popen(['reading', 'create_tables'])
