import hashlib
import unittest
from time import sleep


class TestUtilMethods(unittest.TestCase):

    def test_str_hash(self):
        inputs = "你好"
        result = int(hashlib.sha1(inputs.encode("utf-8")).hexdigest(), 16) % (10 ** 8)
        print(result)
        self.assertEqual(13397538, result)


if __name__ == '__main__':
    unittest.main()
