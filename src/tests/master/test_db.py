from unittest import TestCase
from master.db import Database

class TestDB(TestCase):

    def setUp(self) -> None:
        self.DB = Database()

    def test_db_init(self):
        pass