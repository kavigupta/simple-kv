import os
import hashlib


def key_hash(key):
    return hashlib.sha256(key.encode("utf-8")).hexdigest()


def add_key():
    entropy = os.urandom(256)
    key = hashlib.sha256(entropy).hexdigest()
    h = key_hash(key)
    print(f"Your key: {key}. Save the key since it will not be displayed again")
    with open("valid_key_hashes.txt", "a") as f:
        f.write(h + "\n")


if __name__ == "__main__":
    add_key()
