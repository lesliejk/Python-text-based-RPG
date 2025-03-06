---
# Character Microservice for RPGGame

This document describes how the main game (`RPGGame`) interacts with the **Character microservice**. The microservice manages character-related operations, including data retrieval, character creation, name updates, experience management, and leveling up. It uses a local JSON file (`character_data.json`) for storage and returns data to the main game in standardized Python dictionaries.

---

# File handling functions for communication

```python
def write_request(request):
    """Write a request to request.txt."""
    with open("request.txt", "w") as f:
        f.write(request)

def read_response():
    """Read the response from response.txt."""
    try:
        with open("response.txt", "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

def clear_response():
    """Remove response.txt after reading."""
    try:
        os.remove("response.txt")
    except FileNotFoundError:
        pass

def response_available():
    """Check if a response is available."""
    return os.path.exists("response.txt")

def send_request(request):
    """Send a request and wait for the response."""
    write_request(request)
    while not response_available():
        time.sleep(1)
    response = read_response()
    clear_response()
    return json.loads(response)
```    
---
## 1. Overview

The `RPGGame` module communicates with the **Character microservice** by calling its functions to perform various operations on character data. The microservice handles the following key functionalities:
- Retrieving the active character's details.
- Creating new characters with unique names.
- Updating the active character's name.
- Adding experience points to the active character.
- Leveling up the active character with updated stats and experience thresholds.

All interactions follow a consistent flow: `RPGGame` → `Character module` → `character_data.json` → `Character module` → `RPGGame`. The microservice processes the JSON data internally and returns it as Python dictionaries for easy integration into the main game.

---

## 2. Requesting Data

## Get Active Character
To retrieve the active character's details, use the `get_active_character()` function. The Character module loads the entire character list from the JSON file and filters it to return only the active character's data as a Python dictionary.

### How It Works:
1. `RPGGame` calls `get_active_character()` from the Character module.
2. The Character module calls `load_character_data()` to read `character_data.json`.
3. The JSON data (a list of characters) is parsed, and the active character is filtered out.
4. The active character's details are returned to `RPGGame` as a dictionary.

### Example:
```python
from character import get_active_character

# Request the active character
active_character = get_active_character()

if active_character:
    print("Active Character:", active_character)
else:
    print("No active character is set.")
```
## Character Creation
To create a new character, use create_new_character(name, job). This function ensures the name is unique, builds the character object, and saves it to the JSON file.

### How It Works:
RPGGame calls create_new_character(name, job).
The Character module loads existing data to check for name uniqueness.
If unique, it builds a new character object and saves it to character_data.json.
The new character’s details are returned as a dictionary.
### Example:
```python
from character import create_new_character

# Create a new character
new_character = create_new_character("Hero", "Warrior")
if new_character:
    print("New Character Created:", new_character)
else:
    print("Character creation failed (e.g., name already exists).")
```

## Update Character Name
To update the active character's name, use update_character_name(new_name). This ensures the new name is unique before updating and saving the data.

### How It Works:
RPGGame calls update_character_name(new_name).
The Character module checks for name uniqueness among existing characters.
If unique, it updates the active character’s name and saves the changes.
The updated character’s details are returned as a dictionary.

### Example:
```python
from character import update_character_name

# Update the active character's name
updated_character = update_character_name("Legend")
if updated_character:
    print("Updated Character:", updated_character)
else:
    print("Name update failed (e.g., name already exists).")
```

## Add Experience
To add experience points to the active character, use add_experience(exp_points). This updates the character's experience and saves the changes.

### How It Works:
RPGGame calls add_experience(exp_points).
The Character module updates the active character’s experience value.
The updated data is saved to character_data.json.
The updated character’s details are returned as a dictionary.
Example:
```python
from character import add_experience

# Add 100 experience points
updated_character = add_experience(100)
if updated_character:
    print("Updated Character:", updated_character)
else:
    print("Experience update failed.")
```
## Level Up
To level up the active character, use level_up(). This increments the level, updates stats based on the character’s job, and adjusts the experience threshold for the next level.

### How It Works:
RPGGame calls level_up().
The Character module retrieves the active character and increments its level.
Stats are updated iteratively based on job-specific increments, and the required experience is subtracted while updating the next level threshold (may loop if multiple levels are gained).
The updated data is saved to character_data.json.
The updated character’s details are returned as a dictionary.
### How It Works:
```python
from character import level_up

# Level up the active character
updated_character = level_up()
if updated_character:
    print("Leveled Up Character:", updated_character)
else:
    print("Level up failed.")
```
<img width="1326" alt="umlg94_2" src="https://github.com/user-attachments/assets/4e71ce37-e93d-42a1-9962-ce52fd28e2e3" />

