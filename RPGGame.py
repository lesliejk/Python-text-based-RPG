# RPGGame.py

import time
import character  # Import the character microservice module

# -------------------------------------------------START MENU--------------------------------------------------------- #
game_name = "Amazing Adventure Game"
game_subtext = "Programmed by Leslie Kong\n"
about_game = ("This game is developed by Leslie Kong as part of his Software Development Project for OSU. "
              "I hope that you enjoy.\n")
welcome_message = ("This text based adventure game will take you on an adventure through the Kingdom of Riverstone."
                   "\nThere is a curse that has befallen the lands and the King has sought any and all adventurers to lift the curse. "
                   "\nAny adventurer who finds and eliminates the curse is promised the title of Lord and equivalent lands.\n")
start_instructions = "Type in any of the following commands for more information or start playing."
error_command = "Sorry I could not understand that command. Please try another command.\n"

start_commands = {
    "changelog": "To see features added in each version of the game",
    "about": "Learn more about the developer",
    "start": "To create your character and begin your adventure",
    "exit": "Exits the game. Your progress will not be saved"
}

current_ver = "v2"

changelog = {
    "v1": ["Added a start menu and start options", "Added zones and traversal", "Added story text"],
    "v2": ["Added NPC support", "Added item support", "Added quest support"]
}

help_info = "At any time, you can use the command 'help' to show available global commands.\n"

help_commands = {
    "help": "Show available global commands",
    "exit": "Exits the game. Your progress will not be saved",
    "changename": "Change your character's name",
    "manage": "Manage your character (view status, add experience, level up, save)"
}

game_intro = ("\nAfter a grueling week of travel, you arrive at the village on the outskirts of Riverstone Castle.\n"
              "You've heard news of a curse that had spread famine and disease across the kingdom.\n"
              "King Victor is in distress, his people are dying and if this curse is not cleansed soon \n"
              "the kingdom may be entirely wiped out. You heard his call, promising the title of Lord and land to \n"
              "any adventurer that may cure the land of the curse.\n")

# ---------------------------------------------------GAME DATA------------------------------------------------------- #

username = None

quests = [
    {"quest_val": 0, "name": "Curse of Riverstone", "progress_val": 0, "complete": False, "quest_text": ["placeholder1", "placeholder2", "placeholder3"]},
    {"quest_val": 1, "name": "Find the Beggar's lost cat", "progress_val": 0, "complete": False, "quest_text": ["placeholder1", "placeholder2", "placeholder3"]},
    {"quest_val": 2, "name": "Help the family give their son a burial", "progress_val": 0, "complete": False, "quest_text": ["placeholder1", "placeholder2", "placeholder3"]},
]

npcs = [
    {"name": "Beggar", "npc_val": 0, "quest_val": 1, "dialogue": ["dplaceholder1", "dplaceholder2", "dplaceholder3"]},
    {"name": "Town Guard", "npc_val": 1, "quest_val": 0, "dialogue": ["dplaceholder1", "dplaceholder2", "dplaceholder3"]},
    {"name": "Crying Mother", "npc_val": 2, "quest_val": 2, "dialogue": ["dplaceholder1", "dplaceholder2", "dplaceholder3"]}
]

zones = {
    "Mountain Peak": "The top is frigid and windy. You discover a statue of a female, standing pridefully with the sun glistening upon it.",
    "Path to Mountain Peak": "There are still signs of recent tracks to the peak. You wonder what is at the top.",
    "Abandoned Village": "The village appears to be abandoned for years. Many smaller villages were abandoned when King Victor declared his lordship.",
    "Mountain Pass": "The pass is narrow and not well maintained. Still, you persevere through.",
    "Base of Mountain": "You reach the base of the mountain. Signs of frequent travel are visible.",
    "Town": "You are immediately hit with a stench of death and decay. There is no joy or hope left in this town.",
    "West Swamp": "",
    "Cave Entrance": "You come across an unassuming cave entrance. Perhaps there is a clue here.",
    "Eastern Forest": "Much of this forest has been deforested to make room for farmland.",
    "East Swamp": "",
    "Deep Water": "The water is too deep to wade through. You will need a boat to cross.",
    "Small Island": "The island has no signs of recent activity. There is not much here.",
    "Cavern": "The cavern is too dark to see very far, but you know it is vast from the echoes.",
    "Cave River": "There is a river flowing deeper into the cave. The water is warm to the touch.",
    "Witch's Shack": "The witch invites you in. The smell is intense, a mix of medicinal, rot, and floral aromas.",
    "Wolf's Den": "You carefully enter the Wolf's Den. There is a stench of decaying meat.",
    "Witch's Cellar": "It would be a mistake to enter while the witch is here.",
    "Western Forest": "The forest is dense. You see an area where wood is harvested.",
    "Road to Riverstone": "The road has not been maintained in months.",
    "Guard Tower": "As you approach the guard tower, you notice there are no guards posted.",
    "Castle Gates": "A large crowd stands in front of the gates, blocked by a line of guards.",
    "Riverstone": "You won't be able to get past the crowd. You should find another way."
}

directions = {
    "Mountain Peak": {"north": None, "east": None, "south": "Path to Mountain Peak", "west": None},
    "Path to Mountain Peak": {"north": "Mountain Peak", "east": None, "south": "Abandoned Village", "west": None},
    "Abandoned Village": {"north": "Path to Mountain Peak", "east": "Cave Entrance", "south": "Mountain Pass", "west": None},
    "Mountain Pass": {"north": "Abandoned Village", "east": None, "south": "Base of Mountain", "west": None},
    "Base of Mountain": {"north": "Mountain Pass", "east": None, "south": "Town", "west": None},
    "Town": {"north": "Mountain Pass", "east": "Eastern Forest", "south": "West Swamp", "west": "Western Forest"},
    "West Swamp": {"north": "Town", "east": "East Swamp", "south": None, "west": "Road to Riverstone"},
    "Cave Entrance": {"north": None, "east": "Cavern", "south": None, "west": "Abandoned Village"},
    "Eastern Forest": {"north": None, "east": None, "south": "East Swamp", "west": "Town"},
    "East Swamp": {"north": "Eastern Forest", "east": "Witch's Shack", "south": "Deep Water", "west": "West Swamp"},
    "Deep Water": {"north": "East Swamp", "east": None, "south": "Small Island", "west": None},
    "Small Island": {"north": "Deep Water", "east": None, "south": None, "west": None},
    "Cavern": {"north": "Cave Entrance", "east": None, "south": "Cave River", "west": "Wolf's Den"},
    "Cave River": {"north": "Cavern", "east": None, "south": None, "west": None},
    "Witch's Shack": {"north": None, "east": "Witch's Cellar", "south": None, "west": "East Swamp"},
    "Wolf's Den": {"north": None, "east": None, "south": None, "west": "Cavern"},
    "Witch's Cellar": {"north": None, "east": None, "south": None, "west": "Witch's Shack"},
    "Western Forest": {"north": None, "east": "Town", "south": "Road to Riverstone", "west": None},
    "Road to Riverstone": {"north": "Western Forest", "east": "West Swamp", "south": None, "west": "Guard Tower"},
    "Guard Tower": {"north": None, "east": "Road to Riverstone", "south": None, "west": "Castle Gates"},
    "Castle Gates": {"north": None, "east": "Guard Tower", "south": None, "west": "Riverstone"},
    "Riverstone": {"north": None, "east": "Castle Gates", "south": None, "west": None}
}

other_options = {  
    "Mountain Peak": [[npcs[2]], [], []],
    "Path to Mountain Peak": [[], [], []],
    "Abandoned Village": [[], [], []],
    "Mountain Pass": [[], ["item1", "item2"], []],
    "Base of Mountain": [[], ["item1", "item2"], []],
    "Town": [[npcs[0], npcs[1], npcs[2]], [], []],
    "West Swamp": [[], [], []],
    "Cave Entrance": [[], [], []],
    "Eastern Forest": [[], [], []],
    "East Swamp": [[], [], []],
    "Deep Water": [[], [], []],
    "Small Island": [[], [], []],
    "Cavern": [[], [], []],
    "Cave River": [[], [], []],
    "Witch's Shack": [[], [], []],
    "Wolf's Den": [[], [], []],
    "Witch's Cellar": [[], [], []],
    "Western Forest": [[], [], []],
    "Road to Riverstone": [[], [], []],
    "Guard Tower": [[], [], []],
    "Castle Gates": [[], [], []],
    "Riverstone": [[], [], []]
}

# ------------------------------------------------START FUNCTIONS----------------------------------------------------- #
def exit_game():
    while True:
        check = input("Are you sure you want to exit the game? Please remember to save your character manually. (Y/N) ")
        if check.lower() == "n":
            return
        if check.lower() == "y":
            print("Thank you for playing! Game will exit in 3 seconds.")
            time.sleep(3)
            exit()
        else:
            print("Sorry I could not understand that command. Please try another command.")

def change_log():
    print("Your current version is", current_ver)
    while True:
        version = input("Type in the version you would like to see or 'back' to go back (v1, v2, etc): ")
        if version == "back":
            return
        if version in changelog:
            for line in changelog[version]:
                print(line)
            print("\n")
        else:
            print(error_command)

def about():
    print(about_game)

def comm_err():
    print(error_command)

def start_menu():
    print(game_name)
    print(welcome_message)
    print(start_instructions)
    for option, desc in start_commands.items():
        print(f"{option}: {desc}")
    print("\n")
    while True:
        command = input("Please enter a command: ")
        if command.lower() == "exit":
            exit_game()
        elif command.lower() == "changelog":
            change_log()
        elif command.lower() == "about":
            about()
        elif command.lower() == "start":
            return
        else:
            comm_err()

# ------------------------------------------------Character Management Integration----------------------------------------------------- #
def initialize_character():
    """
    Replaces the old username creation.
    When starting the game, prompt the user to either create a new character or choose an existing one.
    """
    character.main_menu()  # Calls the character module's main_menu for selection/creation

def manage_character():
    """
    Calls the character management menu from character.py.
    """
    print("\n=== Character Management ===")
    character.character_main_menu()

# ------------------------------------------------GAME FUNCTIONS----------------------------------------------------- #
def change_name():
    """
    Changes the character's name using the character module's update function.
    """
    character.update_character_name()

def help():
    for option, desc in help_commands.items():
        print(f"{option}: {desc}")
    print("\n")

def introduction():
    print(game_intro)
    print(help_info)

def start_game():
    """
    Starts the character in the town and allows user to traverse the map.
    """
    location = "Town"
    while True:
        print(f"\nYou enter the {location}.")
        print(zones[location])
        for option in directions[location]:
            if directions[location][option] is not None:
                print(option, ":", directions[location][option])
        if other_options[location][0]:  # Prints names of all the NPCs in the zone
            print("npc :", ", ".join([other_options[location][0][i]['name'] for i in range(len(other_options[location][0]))]))
        if other_options[location][1]:  # Prints names of all the items in the zone
            print("items :", ", ".join([other_options[location][1][i] for i in range(len(other_options[location][1]))]))
        print("\nAdditional option: type 'character' to manage your character.")
        command = input("\nWhat would you like to do? ")
        print("\n")
        if command.lower() == "exit":
            exit_game()
        elif command.lower() == "changename":
            change_name()
        elif command.lower() == "character":
            manage_character()
        elif command.lower() == "help":
            help()
        elif command.lower() in directions[location]:
            if directions[location][command] is None:
                print("You cannot go that way.")
            else:
                location = directions[location][command]
        elif any(other_options[location][0][i]['name'].lower() == command.lower() for i in range(len(other_options[location][0]))):
            talk(command.lower())
        else:
            comm_err()

def talk(npc_name):
    print(f'You talk with the {npc_name}')

# ------------------------------------------------MAIN EXECUTION----------------------------------------------------- #
start_menu()
initialize_character()  # Prompt to create or choose a character
introduction()
start_game()
