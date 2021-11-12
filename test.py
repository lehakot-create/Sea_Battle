import unittest
# from ship import Ship
from ship import Dot
from ship import Ship


class MyTestCase(unittest.TestCase):
    # @classmethod
    # def setUpClass(cls):
    #     cls.ship = Ship()
    #
    # def test_ship_location(self):
    #     self.ship.ship_location()
    #     table = self.ship.get_table()
    #     for row in range(len(table)-1):
    #         # print(table[row])
    #         for column in range(len(table[row])-1):
    #             if table[row][column] == '■':
    #                 if table[row + 1][column] == '■' and table[row][column + 1] == '■':
    #                     # print(table[row][column], table[row][column + 1])
    #                     # print(table[row + 1][column], table[row + 1][column + 1])
    #                     raise AssertionError

    # def test_dot(self):
    #     self.dot = Dot(1, 2)
    #     self.dot2 = Dot(1, 2)
    #     self.dot3 = Dot(2, 3)
    #     self.assertEqual(self.dot, (1, 2))
    #     self.assertNotEqual(self.dot, self.dot3)

    def test_ship(self):
        self.cases = [
            [[1, Dot(1, 1), 0], Dot(1, 1)],
            [[1, (1, 1), 1], [(1, 1)]],
            [[2, (1, 1), 0], [(1, 1), (1, 2)]],
            [[2, (1, 1), 1], [(1, 1), (2, 1)]]

        ]
        for el in self.cases:
            with self.subTest(x=el):

                self.ship = Ship(*el[0])
                answer = self.ship.dots
                self.assertEqual(answer, el[1])


if __name__ == '__main__':
    unittest.main()
