#!/usr/bin/python3
import hashlib

set_value = "123456sdefe"
# h = hashlib.md5()
# h.update(set_value.encode())
h = hashlib.md5(set_value.encode())
password = h.hexdigest()
print(password)

checked_against = "1a23456sdefe"
# h = hashlib.md5()
# h.update(checked_against.encode())
b = hashlib.md5(checked_against.encode())
chk_pwd = b.hexdigest()
print(chk_pwd)

print(password == chk_pwd)
