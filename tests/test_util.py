import hashlib
import multiprocessing
import unittest
from time import sleep

def test_func(fun,y):
    fun(y)

def test_func2(x):
    print(x)

class TestUtilMethods(unittest.TestCase):

    def test_str_hash(self):
        inputs = "你好"
        result = int(hashlib.sha1(inputs.encode("utf-8")).hexdigest(), 16) % (10 ** 8)
        print(result)
        self.assertEqual(13397538, result)

    def test_process(self):
        multiprocessing.Process(target=test_func, args=(test_func2, 3)).start()


if __name__ == '__main__':
    unittest.main()
