import unittest

from multiprocessing import Process
import requests
import time

from secret_test_key import test_key
from main import app


class TestKV(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = Process(target=app.run, kwargs=dict(port=8080))
        cls.server.start()
        time.sleep(0.5)

    @classmethod
    def tearDownClass(cls):
        cls.server.terminate()
        cls.server.join()

    def clear(self, key):
        requests.post(
            "http://localhost:8080/clear", params=dict(api_key=test_key, k=key)
        ).raise_for_status()

    def put(self, key, value, **kwargs):
        result = requests.post(
            "http://localhost:8080/put",
            params=dict(api_key=test_key, k=key, **kwargs),
            data=value,
        )
        result.raise_for_status()

    def get(self, key):
        return requests.get(
            "http://localhost:8080/get", params=dict(api_key=test_key, k=key)
        ).content.decode("utf-8")

    def test_put_get(self):
        self.clear("hi")
        self.put("hi", "test information and test data!")
        self.put("bye", "unrelated information")
        self.assertEqual(self.get("hi"), "test information and test data!")
        self.put("hi", "overwrite")
        self.assertEqual(self.get("hi"), "overwrite")
        self.assertEqual(self.get("bye"), "unrelated information")

    def test_put_append_get(self):
        self.clear("hi")
        self.put("hi", "test information")
        self.put("hi", " and test data!", method="append")
        self.assertEqual(self.get("hi"), "test information and test data!")
        self.put("hi", "!!", method="append")
        self.assertEqual(self.get("hi"), "test information and test data!!!")
