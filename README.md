# Communication Contract

This document describes how the main game (RPGGame) interacts with the Character microservice. In our architecture, the main game calls functions from the Character module to request data. The Character module then retrieves the data from a local JSON file (`character_data.json`) and returns it to the main game.

---

## 1. Requesting Data

In the main game (RPGGame), you call the functions from the Character module to **request** data. For example, to obtain the active character's details, you would call the `get_active_character()` function.

### How It Works:
1. **RPGGame** calls `get_active_character()` from the Character module.
2. **Character Microservice** calls `load_character_data()` to read the local JSON file.
3. The JSON data (a list of characters) is parsed and the active character (a Python dictionary) is returned from Character back to RPGGame.

### Example Request Call (in RPGGame):

```python
from character import get_active_character

# RPGGame requests the active character data from the Character module.
active_character = get_active_character()

if active_character:
    print("Active Character:", active_character)
else:
    print("No active character is set.")
```

## 2. Receiving Data

Once the main game has requested data, it receives the active character’s information as a Python dictionary. 

### How It Works:
1. The Character module processes the data fetched from the local JSON file.
2. It returns a structured Python dictionary containing character details (e.g., name, level, job, and stats).
3. The main game receives this dictionary and can then use it as needed.

### Example Request Call (in RPGGame):
```python
from character import get_active_character

# RPGGame receives the character data after Character module retrieves it.
character_data = get_active_character()

if character_data:
    name = character_data.get("name")
    level = character_data.get("level")
    job = character_data.get("job")
    print(f"Character Name: {name}")
    print(f"Level: {level}")
    print(f"Job: {job}")
else:
    print("No active character data available.")
```
### Note
1. The Character module internally accesses character_data.json to retrieve the data.
2. The data flows from RPGGame → Character module → Local JSON file → Character module → RPGGame.
3. The Character module does all the work of fetching and parsing the local JSON data.
4. The data is returned in a standardized format (a Python dictionary) so that RPGGame can easily integrate it.

![UML Sequence Diagram](/umlg94.png)