import unittest
from data.source_parser import load_source


class NvidiaTest(unittest.TestCase):
    def test_something(self):
        nvidia_parser = load_source("./sources/nvidia.yml")
        data = nvidia_parser.run()


if __name__ == '__main__':
    unittest.main()
