import os
from itertools import count

from keys import key_hash, all_hashes

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("secret.json")
default_app = firebase_admin.initialize_app(
    cred, {"databaseURL": "https://mineral-subject-307700-default-rtdb.firebaseio.com/"}
)


class Store:
    def __init__(self, reference):
        self.reference = reference

    def get(self, key):
        reference = self.reference.child(key)
        length = reference.child("length").get()
        if length is None:
            return None
        result = []
        for i in range(length):
            value = reference.child(str(i)).get()
            result.append(value)
        return "".join(result)

    def clear(self, key):
        reference = self.reference.child(key)
        reference.delete()

    def put(self, key, value):
        reference = self.reference.child(key)
        reference.delete()
        reference.child("length").set(1)
        reference.child("0").set(value)

    def append(self, key, value):
        reference = self.reference.child(key)
        length = reference.child("length").get() or 0
        reference.child("length").set(length + 1)
        reference.child(str(length)).set(value)


def store(key):
    h = key_hash(key)
    if h not in all_hashes():
        return None
    return Store(db.reference("/").child(h))
