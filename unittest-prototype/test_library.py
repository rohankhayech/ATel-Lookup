import unittest
import library


class TestLibraryMethods(unittest.TestCase):
    def test_add(self):
        self.assertEqual(library.add(2.0, 3.0), 5.0)

    def test_log(self):
        self.assertEqual(library.log(100.0, 10.0), 2.0)

    def test_log_default(self):
        self.assertEqual(library.log(32.0), 5.0)


if __name__ == '__main__':
    unittest.main()
