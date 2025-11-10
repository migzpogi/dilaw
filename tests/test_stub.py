import unittest

from WebApp import stub_test


class StubTests(unittest.TestCase):

    def test_webapp(self):
        self.assertTrue(stub_test())


if __name__ == '__main__':
    unittest.main()
