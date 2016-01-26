import hashlib

m=hashlib.md5()
m.update("This is an example and")

print m.digest_size