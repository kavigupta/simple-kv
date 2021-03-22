import os
import sys
import hashlib


def key_hash(key):
    return hashlib.sha256(key.encode("utf-8")).hexdigest()


def add_key(name):
    entropy = os.urandom(256)
    key = hashlib.sha256(entropy).hexdigest()
    h = key_hash(key)
    print(f"Your key: '{key}'. Save the key since it will not be displayed again")
    with open("valid_key_hashes.txt", "a") as f:
        f.write(f"{h}: {name}\n")


def all_hashes():
    with open("valid_key_hashes.txt") as f:
        return set(x.split(":")[0].strip() for x in f)


if __name__ == "__main__":
    add_key(sys.argv[1])
