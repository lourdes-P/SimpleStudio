import eel
import json
import logic.interpreter.lexicalanalizer.token
from logic.interpreter.lexicalanalizer.reserved_word_manager.reserved_word_map import ReservedWordMap

reserved_words = ReservedWordMap()

eel.init("./src/gui")

# functions between the init and start
def read_data():
    with open("data.json", "r") as file:
        content = json.loads(file.read())
    return content

def write_data(content):
    with open("data.json","w") as file:
        file.write(json.dumps(content))
    return content

@eel.expose
# this decorator will expose this function to the gui javascript file
# this means we will be able to call this function from javascript
def create_token(title):
    global token_count

    new_token = {
        "id": token_count + 1,
        "title": title
    }

    content = read_data()
    content['tokens'].append(new_token)

    write_data(content)
    token_count += 1

    return new_token

@eel.expose
def list_tokens():
    return read_data()

@eel.expose
def delete_token(id):
    global token_count
    content = read_data()
    content['tokens'].remove(content.loc[(content['tokens'].id == id)] )

    write_data(content)
    token_count -= 1

import os
if not os.path.exists("data.json"):
    file= open("data.json", "w")
    file.write(json.dumps({"tokens": []}))
    file.close()
else:
    content = read_data()
    token_count = len(content['tokens'])

eel.start("index.html")
