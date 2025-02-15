import json
import os

# File name for local storage (the JSON file will contain a list of characters)
CHARACTER_DATA_FILE = "character_data.json"

# Job-based stat increments per level (base increments; refine as needed)
JOB_STAT_INCREMENTS = {
    "Warrior": {"hp": 10, "mp": 5, "physical_attack": 3, "magical_attack": 1, "defense": 2, "hit_rate": 1},
    "Mage": {"hp": 5, "mp": 10, "physical_attack": 1, "magical_attack": 3, "defense": 1, "hit_rate": 2},
    "Rogue": {"hp": 7, "mp": 7, "physical_attack": 2, "magical_attack": 2, "defense": 2, "hit_rate": 3}
}

# Generate a leveling table for levels 1-40; e.g., base exp multiplied by 1.2 per level
def generate_leveling_table():
    leveling_table = {}
    base_exp = 1000
    for level in range(1, 41):
        leveling_table[level] = int(base_exp * (1.2 ** (level - 1)))
    return leveling_table

LEVELING_TABLE = generate_leveling_table()

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

def double_confirm(prompt):
    """Prompt the user and ask for confirmation (Y/N). Returns True if confirmed."""
    while True:
        choice = input(prompt + " (Y/N): ").strip().lower()
        if choice == 'y':
            return True
        elif choice == 'n':
            return False
        else:
            print("Please enter Y or N.")

def create_new_character():
    """Create a new character with double confirmation for name and job selection.
       The user can type 'back' to cancel and return to the previous menu.
       Returns the new character's name or None if the user cancels."""
    data = load_character_data()
    print("\n--- Create New Character ---")
    
    # Prompt for character name with an option to go back.
    while True:
        name = input("Enter character name (or type 'back' to return): ").strip()
        if name.lower() == 'back':
            return None
        if any(char["name"].lower() == name.lower() for char in data):
            print("A character with that name already exists. Please choose a different name.")
        else:
            if double_confirm(f"Confirm character name '{name}'?"):
                break

    # Prompt for job selection with an option to go back.
    valid_jobs = ["Warrior", "Mage", "Rogue"]
    while True:
        job = input("Choose a job (Warrior, Mage, Rogue) (or type 'back' to return): ").strip().title()
        if job.lower() == 'back':
            return None
        if job not in valid_jobs:
            print("Invalid job choice. Please choose Warrior, Mage, or Rogue.")
        else:
            if double_confirm(f"Confirm job '{job}'?"):
                break

    # Initialize default stats
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
    print("Character created successfully!")
    return name

def choose_existing_character():
    """List existing characters and let the user choose one.
       The user can type 'back' to cancel and return to the previous menu.
       If no characters exist, display a message and return None."""
    data = load_character_data()
    if not data:
        print("No existing characters found.")
        input("Press Enter to return to the previous menu...")
        return None
    print("\n--- Choose Existing Character ---")
    for idx, char in enumerate(data, start=1):
        print(f"{idx}. Name: {char['name']}, Job: {char['job']}, Level: {char['level']}")
    while True:
        choice = input("Enter the number of the character you want to use (or type 'back' to return): ").strip()
        if choice.lower() == 'back':
            return None
        try:
            num = int(choice)
            if 1 <= num <= len(data):
                return data[num - 1]["name"]
            else:
                print("Invalid number. Please try again.")
        except ValueError:
            print("Please enter a valid number.")

def choose_or_create_character():
    """At game start, allow the user to create a new character or choose an existing one.
       Returns the active character's name.
       The user can also choose to exit the selection menu."""
    while True:
        print("\nSelect an option:")
        print("1. Create a new character")
        print("2. Choose an existing character")
        print("3. Exit")
        option = input("Enter 1, 2, or 3: ").strip()
        if option == "1":
            new_char = create_new_character()
            if new_char is not None:
                return new_char
            else:
                print("Returning to selection menu.")
        elif option == "2":
            existing_char = choose_existing_character()
            if existing_char is not None:
                return existing_char
            else:
                print("Returning to selection menu.")
        elif option == "3":
            exit("Exiting the game.")
        else:
            print("Invalid option. Please try again.")


# Global variable to hold the active character's name
_active_character_name = None

def set_active_character(name):
    global _active_character_name
    _active_character_name = name

def get_active_character():
    """Return the active character object from the list (by matching the name)."""
    data = load_character_data()
    for char in data:
        if char["name"].lower() == _active_character_name.lower():
            return char
    return None

def update_active_character(updated_character):
    """Update the active character in the JSON file with the provided updated_character."""
    data = load_character_data()
    for idx, char in enumerate(data):
        if char["name"].lower() == updated_character["name"].lower():
            data[idx] = updated_character
            break
    save_character_data(data)

def update_character_name():
    """Update the active character's name with confirmation and persist the change."""
    active_char = get_active_character()
    if not active_char:
        print("No active character selected.")
        return
    current_name = active_char.get("name", "Unknown")
    print(f"Current character name: {current_name}")
    new_name = input("Enter new name for your character: ").strip()
    if double_confirm(f"Confirm change character name to '{new_name}'?"):
        # Check for duplicate names
        data = load_character_data()
        if any(char["name"].lower() == new_name.lower() for char in data):
            print("A character with that name already exists. Name change cancelled.")
            return
        active_char["name"] = new_name
        update_active_character(active_char)
        set_active_character(new_name)
        print("Character name updated successfully!")
    else:
        print("Name change cancelled.")

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
    """Add experience points to the active character.
       Future battle or quest systems will call this function."""
    active_char = get_active_character()
    if not active_char:
        print("No active character found.")
        return
    active_char["experience"] += exp_points
    update_active_character(active_char)
    print(f"Added {exp_points} experience points. Total experience: {active_char['experience']}.")

def level_up():
    """Level up the active character repeatedly if enough experience is available.
       Uses the LEVELING_TABLE for requirements and automatically increments stats."""
    active_char = get_active_character()
    if not active_char:
        print("No active character found.")
        return
    leveled = False
    while active_char["level"] < 40:
        current_level = active_char["level"]
        required_exp = LEVELING_TABLE[current_level]
        if active_char["experience"] < required_exp:
            break
        active_char["level"] += 1
        active_char["experience"] -= required_exp
        active_char["experienceToNextLevel"] = LEVELING_TABLE[active_char["level"]]
        
        increments = JOB_STAT_INCREMENTS.get(active_char["job"], 
            {"hp": 5, "mp": 5, "physical_attack": 1, "magical_attack": 1, "defense": 1, "hit_rate": 1})
        active_char["hp"] += increments["hp"]
        active_char["mp"] += increments["mp"]
        active_char["physical_attack"] += increments["physical_attack"]
        active_char["magical_attack"] += increments["magical_attack"]
        active_char["defense"] += increments["defense"]
        active_char["hit_rate"] += increments["hit_rate"]
        leveled = True
    update_active_character(active_char)
    if leveled:
        print("\nLevel up successful!")
    else:
        print("Not enough experience to level up.")
    view_character()

def character_main_menu():
    """A simple menu for character management.
       Options include viewing active character, changing name, saving character, adding experience, leveling up, and returning to game."""
    while True:
        print("\n--- Character Management Menu ---")
        print("1. View Active Character")
        print("2. Change Character Name")
        print("3. Save Character")
        print("4. Add Experience and Level Up (simulate)")
        print("5. Return to Game")
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            view_character()
        elif choice == "2":
            update_character_name()
        elif choice == "3":
            save_current_character()
        elif choice == "4":
            try:
                exp = int(input("Enter experience points to add: ").strip())
            except ValueError:
                print("Invalid number.")
                continue
            add_experience(exp)
            level_up()
        elif choice == "5":
            break
        else:
            print("Invalid option. Please try again.")

def main_menu():
    """Initialize character selection.
       Allows the user to create a new character or choose an existing one.
       Sets the active character by its name."""
    active_name = choose_or_create_character()
    set_active_character(active_name)
    print(f"Active character set to: {active_name}")

# Only call main_menu() if this module is run directly (for testing purposes)
if __name__ == "__main__":
    main_menu()
    character_main_menu()
