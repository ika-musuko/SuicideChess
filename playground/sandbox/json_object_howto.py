# json seralization support howto
import json

class User(object):
    def __init__(self, name, password):
        self.name = name
        self.password = password
alice = User('Alice A. Adams', 'secret')

def jdefault(o):
    if isinstance(o, set):
        return list(o)
    return o.__dict__
    
print(json.dumps(alice, default=jdefault))
# outputs: {"password": "secret", "name": "Alice A. Adams"}