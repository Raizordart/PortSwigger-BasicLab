<<<<<<< HEAD
import hashlib
import base64

with open("password.txt", "r") as f:
    data = f.read().split()

with open("rainbow_table.txt", "w") as f:
    for dat in data:
        pwd_hash = hashlib.md5(dat.encode()).digest().hex()
        cookie_candidate = base64.b64encode(f"carlos:{pwd_hash}".encode())
=======
import hashlib
import base64

with open("password.txt", "r") as f:
    data = f.read().split()

with open("rainbow_table.txt", "w") as f:
    for dat in data:
        pwd_hash = hashlib.md5(dat.encode()).digest().hex()
        cookie_candidate = base64.b64encode(f"carlos:{pwd_hash}".encode())
>>>>>>> ae5bd4f (init commit)
        f.write(f"{cookie_candidate.decode()}\n") 