import zmq                  # as communication pipe
import json
import os
import time

error_command = "Sorry I could not understand that command. Please try another command.\n"


def comm_err():
    print(error_command)


def exit_game():
    while True:
        check = input("Are you sure you want to exit the game? "
                      "Please remember to save your character manually. (Y/N) ").lower().strip()
        if check == "n":
            return
        if check == "y":
            print("Thank you for playing!")
            exit()
        else:
            comm_err()


class Help:
    def __init__(self):
        self._message = "At any time, you can use the command 'help' to show available global commands.\n"
        self._commands = {
            "help": "Show available global commands",
            "exit": "Exits the game. Your progress will not be saved",
            "character": "Manage your character (change name, view status, add experience, level up, save)"
        }

    def message(self):
        print(self._message)

    def show_commands(self):
        for option, desc in self._commands.items():
            print(f"{option}: {desc}")
        print("\n")


class StartMenu:
    def __init__(self):
        self.changelog = {
            "v1": ["Added a start menu and start options", "Added zones and traversal", "Added story text"],
            "v2": ["Added NPC support", "Added item support", "Added quest support", "Added zone images display",
                   "Added setting menu", "Added save and load feature", "Added zone themes"]
        }
        self.game_name = "Amazing Adventure Game"
        self.about = ("This game is developed by Leslie Kong as part of his Software Development Project for OSU. I "
                      "hope that you enjoy.\n")
        self.welcome = ("This text based adventure game will take you on an adventure through the "
                        "Kingdom of Riverstone. \nThere is a curse that has befallen the lands and "
                        "the King has sought any and all adventurers to lift the curse. \nAny adventurer who "
                        "finds and eliminates the curse is promised the title of Lord and equivalent lands.\n")
        self.start_instructions = "Type in any of the following commands for more information or start playing."
        self.current_version = "v2"
        self.commands = {
            "changelog": "To see features added in each version of the game",
            "about": "Learn more about the developer",
            "start": "To create your character and begin your adventure",
            "exit": "Exits the game. Your progress will not be saved"
        }
        self.help = "At any time, you can use the command 'help' to show available global commands.\n"
        self.help_commands = {
            "help": "Show available global commands",
            "exit": "Exits the game. Your progress will not be saved",
            "character": "Manage your character (view status, add experience, level up, save)",
            "settings": "Change game settings",
            "mute": "Stops playing current audio track"
        }

    def start_options(self):
        print(self.game_name)
        print(self.welcome)
        print(self.start_instructions)
        while True:
            for option, desc in self.commands.items():
                print(f"{option}: {desc}")
            print("\n")
            command = input("Please enter a command: ").lower().strip()
            if command == "exit":
                exit_game()
            elif command == "changelog":
                self.get_changelog()
            elif command == "about":
                self.get_about()
            elif command == "start":
                return
            else:
                comm_err()

    def get_about(self):
        print(self.about)

    def get_changelog(self):
        print("Your current version is", self.current_version)
        while True:
            version = input("Type in the version or 'back' (v1, v2, etc): ").lower().strip()
            if version == "back":
                return
            if version in self.changelog:
                for line in self.changelog[version]:
                    print(line)
                print("\n")
            else:
                comm_err()


class Game:
    def __init__(self):
        self.introduction = (
            "\nAfter a grueling week of travel, you arrive at the village on the outskirts of Riverstone Castle.\n"
            "You've heard news of a curse that had spread famine and disease across the kingdom.\n"
            "King Victor is in distress, his people are dying and if this curse is not cleansed soon \n"
            "the kingdom may be entirely wiped out. You heard his call, promising the title of Lord and land to \n"
            "any adventurer that may cure the land of the curse.\n")
        self.zones = {}
        self.quests = {}
        self.npcs = {}
        self._settings = {}
        self.menu = StartMenu()
        self.adventurer = Player()
        self._help = Help()
        self._zeromq = ZeroPipe()

    def start_menu(self):
        """
        Displays start menu
        """
        self.menu.start_options()

    def load_map_data(self, data=None):
        if data is None:
            try:
                with open('game_data.json', 'r') as infile:
                    data = json.load(infile)
            except FileNotFoundError:  # Error handling
                print(f'Could not find file game_data.json')

        print('Loading map data')
        for i in range(len(data["zone_data"])):
            zone = Zone(data["zone_data"][i])
            name = data["zone_data"][i]["zone_name"]
            self.zones[name] = zone
        print('Loading map data completed')

    def load_quest_data(self, data=None):
        if data is None:
            try:
                with open('game_data.json', 'r') as infile:
                    data = json.load(infile)
            except FileNotFoundError:  # Error handling
                print(f'Could not find file game_data.json')

        print('Loading quest data')
        for i in range(len(data["quest_data"])):
            quest = Quest(data["quest_data"][i])
            name = data["quest_data"][i]["quest_name"]
            self.quests[name] = quest
        print('Loading quest data completed')

    def load_npc_data(self, data=None):
        if data is None:
            try:
                with open('game_data.json', 'r') as infile:
                    data = json.load(infile)
            except FileNotFoundError:  # Error handling
                print(f'Could not find file game_data.json')

        print('Loading npc data')
        for i in range(len(data["npc_data"])):
            npc = NPC(data["npc_data"][i])
            name = data["npc_data"][i]["npc_name"]
            self.npcs[name] = npc
        print('Loading npc data completed')

    def load_settings(self, data=None):
        if data is None:
            try:
                with open('game_data.json', 'r') as infile:
                    data = json.load(infile)
            except FileNotFoundError:  # Error handling
                print(f'Could not find file game_data.json')

        self._settings = data["settings"]

    def load_game_data(self, data=None):
        self.load_map_data(data)
        self.load_quest_data(data)
        self.load_npc_data(data)
        self.load_settings(data)

    def zone_info(self, zone):
        print(f"\nYou enter the {zone.get_name()}.")
        if zone.get_lore():
            print(zone.get_lore())
        zone.get_directions()

    def display_image(self, byte_array):
        """
        Displays image from bytes with default image viewer
        """
        from PIL import Image  # To display images
        import io
        byte_image = io.BytesIO(byte_array)
        image = Image.open(byte_image)
        image.show()

    def play_theme(self, theme_bytes):
        """
        Plays audio file from bytes
        """
        import pygame
        import io
        pygame.mixer.init()
        pygame.mixer.stop()
        theme = io.BytesIO(theme_bytes)
        pygame.mixer.Sound(theme).play()

    def stop_sounds(self):
        """
        Stops playing current audio file
        """
        import pygame
        pygame.mixer.stop()

    def save_game(self):
        """
        Saves current game state to a save slot
        """
        slot = 0
        while not (0 < slot < 4):
            slot = int(input("\nWhich slot would you like to save to (1,2,3)? "))
        save_data = self.export_game_data()
        self._zeromq.save_game_data('save', str(slot), save_data)

    def load_from_save(self):
        """
        Loads game from save slot
        """
        slot = 0
        while not (0 < slot < 4):
            slot = int(input("\nWhich save slot would you like to load (1,2,3)? "))
        data = self._zeromq.load_game_data('load', str(slot))
        self.load_game_data(data)
        print(f'Successfully loaded save file {slot}')

    def export_game_data(self):
        """
        Parses objects out to dictionaries to store in json
        """
        data = {"zone_data": self.export_map_data(), "quest_data": self.export_quest_data(),
                "npc_data": self.export_npc_data(), "settings": self.export_settings()}
        return data

    def export_npc_data(self):
        npc_data = []
        for npc in self.npcs.values():
            data = {"object_num": npc._object_num, "npc_name": npc._npc_name, "hostile": npc._hostile,
                    "stats": npc._stats, "alive": npc._alive, "reputation": npc._reputation, "dialogue": npc._dialogue}
            npc_data.append(data)

        return npc_data

    def export_quest_data(self):
        quest_data = []
        for quest in self.quests.values():
            data = {"object_num": quest._object_num, "quest_name": quest._quest_name, "quest_progress": quest._progress,
                    "quest_complete": quest._complete, "quest_text": quest._quest_text}
            quest_data.append(data)

        return quest_data

    def export_settings(self):
        return self._settings

    def export_map_data(self):
        zone_data = []
        for zone in self.zones.values():
            data = {"object_num": zone._object_num, "zone_name": zone._zone_name, "zone_lore": zone._lore,
                    "north": zone.directions["north"], "south": zone.directions["south"],
                    "east": zone.directions["east"], "west": zone.directions["west"], "npcs": zone._npcs,
                    "items": zone._items, "theme": zone._theme}
            zone_data.append(data)

        return zone_data

    def game_menu(self):
        """
        Acts as default menu after starting the adventure
        :return:
        """
        while True:
            self._help.message()
            zone = self.zones[self.adventurer.location]
            self.zone_info(zone)
            if self._settings["image_display"]:
                self.display_image(self._zeromq.get_image('zone', zone.get_name()))
            if self._settings["theme_sounds"] and zone._theme:
                self.play_theme(self._zeromq.get_theme(zone._theme))

            command = input("\nWhat would you like to do? ").lower().strip()
            print("\n")
            if command == "exit":
                exit_game()
            elif command == "help":
                self._help.show_commands()
            elif command == "character":
                manage_character()
            elif command == "settings":
                self.settings_menu()
            elif command == "save":
                self.save_game()
            elif command == "load":
                self.load_from_save()
            elif command == "mute":
                self.stop_sounds()
            elif command in zone.directions:
                if zone.directions[command] is None:
                    print("You cannot go that way.")
                else:
                    self.adventurer.move(zone.directions[command])
            else:
                comm_err()

    def settings_menu(self):
        """
        Menu to change settings
        """
        while True:
            for i, setting in enumerate(self._settings, 1):
                print(f"{i}. {setting}")

            selection = input("\nEnter the setting you would like to change or 'back': ").lower().strip()
            selection = "_".join(selection.split())
            if selection == "back":
                return
            if selection in self._settings:
                if self._settings[selection]:
                    print(f'{selection} is currently toggled on. Do you want to toggle this setting off? ', end="")
                else:
                    print(f'{selection} is currently toggled off. Do you want to toggle this setting on? ', end="")
                confirmation = input()
                if confirmation == "y":
                    self.toggle_setting(selection)
                    continue
                if confirmation == "n":
                    continue
                else:
                    comm_err()
            else:
                print("Sorry, I could not find that setting")

    def toggle_setting(self, setting):
        """
        Toggles a setting on/off
        """
        if self._settings[setting]:
            self._settings[setting] = False
            print(f'{setting} has been toggled off.')
        else:
            self._settings[setting] = True
            print(f'{setting} has been toggled on.')


class Zone:
    def __init__(self, data):
        self._object_num = data["object_num"]
        self._zone_name = data["zone_name"]
        self._lore = data["zone_lore"]
        self.directions = {"north": data["north"],
                           "south": data["south"],
                           "east": data["east"],
                           "west": data["west"]}
        self._npcs = data["npcs"]
        self._items = data["items"]
        self._theme = data["theme"]

    def get_npcs(self):
        return self._npcs

    def get_items(self):
        return self._items

    def get_directions(self):
        for key, val in self.directions.items():
            if val is not None:
                print(f'{key}: {val}')

    def get_lore(self):
        return self._lore

    def get_name(self):
        return self._zone_name


class Player:
    def __init__(self):
        self.name = "Player"
        self.score = 0
        self.location = "Town"

    def change_name(self, name):
        self.name = name

    def move(self, zone_name):
        self.location = zone_name

    def change_score(self, points):
        self.score += points


class Quest:
    def __init__(self, data):
        self._object_num = data["object_num"]
        self._quest_name = data["quest_name"]
        self._progress = data["quest_progress"]
        self._complete = data["quest_complete"]
        self._quest_text = data["quest_text"]


class NPC:
    def __init__(self, data):
        self._object_num = data["object_num"]
        self._npc_name = data["npc_name"]
        self._hostile = data["hostile"]
        self._stats = data["stats"]
        self._alive = data["alive"]
        self._reputation = data["reputation"]
        self._dialogue = data["dialogue"]


class ZeroPipe:
    """
    Initializes connection for microservice communication
    """
    def __init__(self):
        self.context = zmq.Context()                        # Sets up the environment so that we are able to begin
        self.socket = self.context.socket(zmq.REQ)          # Request socket type
        self.socket.connect("tcp://localhost:5555")
        self.save_socket = self.context.socket(zmq.REQ)
        self.save_socket.connect("tcp://localhost:5556")
        self.sound_socket = self.context.socket(zmq.REQ)
        self.sound_socket.connect("tcp://localhost:5557")

    def get_theme(self, theme):
        import base64
        request = {"theme": theme}
        self.sound_socket.send_json(request)
        byte_sound = self.sound_socket.recv()
        byte_array = bytearray(base64.b64decode(byte_sound))
        return byte_array

    def save_game_data(self, request, slot, data):
        self.save_socket.send_json({"request": request, "slot": slot, "data": data})
        response = self.save_socket.recv()
        if response:
            print(f'Successfully saved to slot {slot}')

    def load_game_data(self, request, slot):
        self.save_socket.send_json({"request": request, "slot": slot})
        load_data = self.save_socket.recv_json()
        return load_data

    def get_image(self, obj_type, name):
        import base64
        request = {"type": obj_type, "name": name}
        self.socket.send_json(request)
        byte_image = self.socket.recv()
        byte_array = bytearray(base64.b64decode(byte_image))
        return byte_array

    def end_connection(self):
        """
        Terminates the connection
        """
        self.context.destroy()
        self.socket.close()

# -------------------------------------------------CHARACTER--------------------------------------------------------- #

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

def initialize_character():
    """Prompt the user to create a new character or choose an existing one."""
    character_list = send_request("get_character_list")
    if character_list:
        print("Existing characters:")
        for idx, name in enumerate(character_list, start=1):
            print(f"{idx}. {name}")
        while True:
            choice = input("Enter the number of the character to use, or 'new' to create a new character: ").strip()
            if choice.lower() == "new":
                while True:
                    name = input("Enter character name: ").strip()
                    job = input("Choose a job (Warrior, Mage, Rogue): ").strip().title()
                    if job not in ["Warrior", "Mage", "Rogue"]:
                        print("Invalid job.")
                        continue
                    result = send_request(f"create_new_character name={name} job={job}")
                    if result["status"] == "success":
                        print("Character created successfully!")
                        send_request(f"set_active_character name={name}")
                        break
                    else:
                        print(result["message"])
                break
            else:
                try:
                    num = int(choice)
                    if 1 <= num <= len(character_list):
                        selected_name = character_list[num - 1]
                        send_request(f"set_active_character name={selected_name}")
                        break
                    else:
                        print("Invalid number.")
                except ValueError:
                    print("Invalid input.")
    else:
        print("No existing characters. Please create a new character.")
        while True:
            name = input("Enter character name: ").strip()
            job = input("Choose a job (Warrior, Mage, Rogue): ").strip().title()
            if job not in ["Warrior", "Mage", "Rogue"]:
                print("Invalid job.")
                continue
            result = send_request(f"create_new_character name={name} job={job}")
            if result["status"] == "success":
                print("Character created successfully!")
                send_request(f"set_active_character name={name}")
                break
            else:
                print(result["message"])

def manage_character():
    """Manage the active character via the microservice."""
    while True:
        print("\n--- Character Management Menu ---")
        print("1. View Active Character")
        print("2. Change Character Name")
        print("3. Add Experience")
        print("4. Level Up")
        print("5. Return to Game")
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            character_data = send_request("get_active_character")
            if "status" in character_data and character_data["status"] == "error":
                print(character_data["message"])
            else:
                print("\n--- Active Character Status ---")
                for key, value in character_data.items():
                    print(f"{key}: {value}")
        elif choice == "2":
            new_name = input("Enter new name for your character: ").strip()
            result = send_request(f"update_character_name new_name={new_name}")
            if result["status"] == "success":
                print("Character name updated successfully!")
            else:
                print(result["message"])
        elif choice == "3":
            try:
                exp = int(input("Enter experience points to add: ").strip())
                result = send_request(f"add_experience exp_points={exp}")
                if result["status"] == "success":
                    print(f"Added {exp} experience points.")
                else:
                    print(result["message"])
            except ValueError:
                print("Invalid number.")
        elif choice == "4":
            result = send_request("level_up")
            if result["status"] == "success":
                print("Level up successful!")
                print("Updated character:")
                for key, value in result["character"].items():
                    print(f"{key}: {value}")
            else:
                print(result["message"])
        elif choice == "5":
            break
        else:
            print("Invalid option.")

def change_name():
    """Change the active character's name."""
    new_name = input("Enter new name for your character: ").strip()
    result = send_request(f"update_character_name new_name={new_name}")
    if result["status"] == "success":
        print("Character name updated successfully!")
    else:
        print(result["message"])


if __name__ == "__main__":
    adventure = Game()
    adventure.start_menu()
    adventure.load_game_data()
    initialize_character()
    adventure.game_menu()
