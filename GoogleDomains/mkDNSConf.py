import json
import sys

domain = str(sys.argv[1])

print(f"Making {domain} configuration")

username = str(input("Username: "))
password = str(input("Password: "))

d = {"domain": domain, "username": username, "password": password, "last": "0.0.0.0"}
print(json.dumps(d))
