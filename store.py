import os
import shelve

from keys import key_hash


def store(key):
    with open("valid_key_hashes.txt") as f:
        hashes = [x.strip() for x in set(f)]
    h = key_hash(key)
    if h not in hashes:
        return None
    try:
        os.makedirs("data")
    except:
        pass
    return shelve.open(os.path.join("data", h), "c")
