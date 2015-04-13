"""
These tests test the workflow of the database, creating and dropping tables and
adding various elements to the tables.

@author Kevin Wilson - khwilson@gmail.com
"""
import os
import sqlite3
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
            f.write(config.dump_config(cls.tmp_config))

    @classmethod
    def tearDownClass(cls):
        # raise ValueError
        os.unlink(cls.tmpfile)
        os.unlink(cls.tmpdb)

    def test_database(self):
        """ Try recreating the tables, adding a couple users, and then recreating tables """
        subprocess.check_call(['reading', '-c', self.tmpfile, 'create_tables'])
        subprocess.check_call(['reading', '-c', self.tmpfile, 'add_user', 'khwilson@gmail.com'])

        conn = sqlite3.connect(self.tmp_config.database.host)
        curs = conn.cursor()
        curs.execute('SELECT email, administrator FROM user')
        users = curs.fetchall()

        self.assertEqual(len(users), 1)
        user = users[0]
        self.assertEqual(user[0], 'khwilson@gmail.com')
        self.assertEqual(user[1], False)

        subprocess.check_call(['reading', '-c', self.tmpfile,
                               'add_user', '--administrator', 'khwilson@yahoo.com'])

        conn = sqlite3.connect(self.tmp_config.database.host)
        curs = conn.cursor()
        curs.execute('SELECT email, administrator FROM user')
        users = curs.fetchall()

        self.assertEqual(len(users), 2)
        users.sort()
        users = tuple((u[0], bool(u[1])) for u in users)
        self.assertEqual(users, (('khwilson@gmail.com', False), ('khwilson@yahoo.com', True)))

        subprocess.check_call(['reading', '-c', self.tmpfile, 'create_tables'])
        conn = sqlite3.connect(self.tmp_config.database.host)
        curs = conn.cursor()
        curs.execute('SELECT COUNT(*) FROM user')
        self.assertEqual(0, curs.fetchall()[0][0])
