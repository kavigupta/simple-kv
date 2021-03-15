import os
import shelve
from google.cloud import storage

from keys import key_hash


def store(key):
    with open("valid_key_hashes.txt") as f:
        hashes = [x.strip() for x in set(f)]
    h = key_hash(key)
    if h not in hashes:
        return None

    # Enable Cloud Storage
    client = storage.Client()
    # Reference an existing bucket.
    return client.get_bucket(h)
