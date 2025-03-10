import json
import os
import time

# File name for character data storage
CHARACTER_DATA_FILE = "character_data.json"

# Job-based stat increments per level
JOB_STAT_INCREMENTS = {
    "Warrior": {"hp": 10, "mp": 5, "physical_attack": 3, "magical_attack": 1, "defense": 2, "hit_rate": 1},
    "Mage": {"hp": 5, "mp": 10, "physical_attack": 1, "magical_attack": 3, "defense": 1, "hit_rate": 2},
    "Rogue": {"hp": 7, "mp": 7, "physical_attack": 2, "magical_attack": 2, "defense": 2, "hit_rate": 3}
}

# Generate leveling table for levels 1-40
def generate_leveling_table():
    leveling_table = {}
    base_exp = 1000
    for level in range(1, 41):
        leveling_table[level] = int(base_exp * (1.2 ** (level - 1)))
    return leveling_table

LEVELING_TABLE = generate_leveling_table()

# Data management functions
def load_character_data():
    """Load the list of characters from the JSON file."""
    if not os.path.exists(CHARACTER_DATA_FILE):
        with open(CHARACTER_DATA_FILE, "w") as f:
            json.dump([], f)
        return []
    with open(CHARACTER_DATA_FILE, "r") as f:
        content = f.read().strip()
        if not content:
            return []
        return json.loads(content)

def save_character_data(data):
    """Save the list of characters to the JSON file."""
    with open(CHARACTER_DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def update_active_character(updated_character):
    """Update the active character in the JSON file."""
    data = load_character_data()
    for idx, char in enumerate(data):
        if char["name"].lower() == updated_character["name"].lower():
            data[idx] = updated_character
            break
    save_character_data(data)

# Global variable for active character
_active_character_name = None

def set_active_character(name):
    """Set the active character by name."""
    global _active_character_name
    _active_character_name = name

def get_active_character():
    """Return the active character object."""
    data = load_character_data()
    for char in data:
        if char["name"].lower() == _active_character_name.lower():
            return char
    return None

# Microservice operations (non-interactive)
def create_new_character(name, job):
    """Create a new character if name is unique and job is valid."""
    data = load_character_data()
    if any(char["name"].lower() == name.lower() for char in data):
        return {"status": "error", "message": "Name already exists"}
    if job not in ["Warrior", "Mage", "Rogue"]:
        return {"status": "error", "message": "Invalid job"}
    character = {
        "name": name,
        "job": job,
        "level": 1,
        "experience": 0,
        "experienceToNextLevel": LEVELING_TABLE[1],
        "hp": 100,
        "mp": 50,
        "physical_attack": 10,
        "magical_attack": 5,
        "defense": 5,
        "hit_rate": 5
    }
    data.append(character)
    save_character_data(data)
    return {"status": "success", "character": character}

# def update_character_name(new_name):
#     """Update the active character's name if unique."""
#     active_char = get_active_character()
#     if not active_char:
# <<<<<<< HEAD
#         return {"status": "error", "message": "No active character"}
#     data = load_character_data()
#     if any(char["name"].lower() == new_name.lower() for char in data if char["name"].lower() != active_char["name"].lower()):
#         return {"status": "error", "message": "Name already exists"}
#     active_char["name"] = new_name
#     update_active_character(active_char)
#     set_active_character(new_name)
#     return {"status": "success", "character": active_char}
# =======
#         print("No active character selected.")
#         return
#     current_name = active_char.get("name", "Unknown")
#     print(f"Current character name: {current_name}")
#     new_name = input("Enter new name for your character: ").strip()
#     if double_confirm(f"Confirm change character name to '{new_name}'?"):
#         # Check for duplicate names
#         data = load_character_data()
#         if any(char["name"].lower() == new_name.lower() for char in data):
#             print("A character with that name already exists. Name change cancelled.")
#             return
#         active_char["name"] = new_name
#         for character in data:
#             if character["name"] == current_name:
#                 character["name"] = new_name
#         save_character_data(data)
#         set_active_character(new_name)
#         print("Character name updated successfully!")
#     else:
#         print("Name change cancelled.")

def view_character():
    """Display the active character's status."""
    active_char = get_active_character()
    if active_char:
        print("\n--- Active Character Status ---")
        for key, value in active_char.items():
            print(f"{key}: {value}")
    else:
        print("No active character selected.")

def save_current_character():
    """Explicitly save the current active character (if there are unsaved changes in memory)."""
    active_char = get_active_character()
    if active_char:
        update_active_character(active_char)
        print("Character saved successfully!")
    else:
        print("No active character to save.")

def add_experience(exp_points):
    """Add experience to the active character."""
    active_char = get_active_character()
    if not active_char:
        return {"status": "error", "message": "No active character"}
    active_char["experience"] += exp_points
    update_active_character(active_char)
    return {"status": "success", "character": active_char}

def level_up():
    """Level up the active character if enough experience is available."""
    active_char = get_active_character()
    if not active_char:
        return {"status": "error", "message": "No active character"}
    leveled = False
    while active_char["level"] < 40:
        current_level = active_char["level"]
        required_exp = LEVELING_TABLE[current_level]
        if active_char["experience"] < required_exp:
            break
        active_char["level"] += 1
        active_char["experience"] -= required_exp
        active_char["experienceToNextLevel"] = LEVELING_TABLE[active_char["level"]]
        increments = JOB_STAT_INCREMENTS.get(active_char["job"], {"hp": 5, "mp": 5, "physical_attack": 1, "magical_attack": 1, "defense": 1, "hit_rate": 1})
        active_char["hp"] += increments["hp"]
        active_char["mp"] += increments["mp"]
        active_char["physical_attack"] += increments["physical_attack"]
        active_char["magical_attack"] += increments["magical_attack"]
        active_char["defense"] += increments["defense"]
        active_char["hit_rate"] += increments["hit_rate"]
        leveled = True
    update_active_character(active_char)
    if leveled:
        return {"status": "success", "character": active_char}
    else:
        return {"status": "error", "message": "Not enough experience"}

# File handling functions for communication
def write_response(response):
    """Write the response to response.txt."""
    with open("response.txt", "w") as f:
        f.write(response)

def read_request():
    """Read the request from request.txt."""
    try:
        with open("request.txt", "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

def clear_request():
    """Remove request.txt after processing."""
    try:
        os.remove("request.txt")
    except FileNotFoundError:
        pass

def request_available():
    """Check if a request is available."""
    return os.path.exists("request.txt")

def parse_request(request):
    """Parse the request string into command and parameters."""
    parts = request.split()
    command = parts[0]
    params = {}
    for part in parts[1:]:
        if "=" in part:
            key, value = part.split("=", 1)
            params[key] = value
    return command, params

# Main microservice loop
if __name__ == "__main__":
    print("Character Microservice is running. Waiting for requests...")
    while True:
        if request_available():
            request = read_request()
            clear_request()
            command, params = parse_request(request)
            if command == "get_character_list":
                data = load_character_data()
                names = [char["name"] for char in data]
                response = json.dumps(names)
            elif command == "create_new_character":
                name = params.get("name")
                job = params.get("job")
                result = create_new_character(name, job)
                response = json.dumps(result)
            elif command == "set_active_character":
                name = params.get("name")
                data = load_character_data()
                if any(char["name"].lower() == name.lower() for char in data):
                    set_active_character(name)
                    response = json.dumps({"status": "success"})
                else:
                    response = json.dumps({"status": "error", "message": "Character not found"})
            elif command == "get_active_character":
                character = get_active_character()
                if character:
                    response = json.dumps(character)
                else:
                    response = json.dumps({"status": "error", "message": "No active character"})
            # elif command == "update_character_name":
            #     new_name = params.get("new_name")
            #     # result = update_character_name(new_name)
            #     response = json.dumps(result)
            elif command == "add_experience":
                exp_points = int(params.get("exp_points", 0))
                result = add_experience(exp_points)
                response = json.dumps(result)
            elif command == "level_up":
                result = level_up()
                response = json.dumps(result)
            else:
                response = json.dumps({"status": "error", "message": "Unknown command"})
            write_response(response)
        time.sleep(1)  # Prevent excessive CPU usage