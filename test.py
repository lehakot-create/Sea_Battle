import unittest
from ship import Ship


class MyTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ship = Ship()

    def test_ship_location(self):
        self.ship.ship_location()
        table = self.ship.get_table()
        for row in range(len(table)-1):
            print(table[row])
            for column in range(len(table[row])-1):
                if table[row][column] == '■':
                    if table[row + 1][column] == '■' and table[row][column + 1] == '■':
                        print(table[row][column], table[row][column + 1])
                        print(table[row + 1][column], table[row + 1][column + 1])
                        raise AssertionError


if __name__ == '__main__':
    unittest.main()
