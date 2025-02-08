# Text Based Adventure Game
# Programmed and Developed by Leslie Kong

import time

# -------------------------------------------------START MENU--------------------------------------------------------- #
game_name = "Amazing Adventure Game"
game_subtext = "Programmed by Leslie Kong\n"
about_game = "This game is developed by Leslie Kong as part of his Software Development Project for OSU. I hope that you enjoy.\n"
welcome_message = ("This text based adventure game will take you on an adventure through the Kingdom of Riverstone."
                   "\nThere is a curse that has befallen the lands and the King has sought any and all adventurers to lift curse. "
                   "\nAny adventurer who finds and eliminates the curse is promised the title of Lord and equivalent lands.\n")
start_instructions = ("Type in any of the following commands for more information or start playing.")
error_command = "Sorry I could not understand that command. Please try another command.\n"

start_commands = {
    "changelog":"To see features added in each version of the game",
    "about":"Learn move about the developer",
    "start":"To create your character and begin your adventure",
    "exit": "Exits the game. Your progress will not be saved"
}

current_ver = "v1"

changelog = {
    "v1": ["Added a start menu and start options","Added zones and traversal", "Added story text"],
}

help_info = "At any time, you can use the command 'help' to show available global commands.\n"

help_commands = {
    "help":"Show available global commands",
    "exit": "Exits the game. Your progress will not be saved",
    "changename": "Changes your name"
}


game_intro = ("\nAfter a grueling week of travel, you arrive at the village on the outskirts of Riverstone Castle.\n"
              "You've heard news of a curse that had spread famine and disease across the kingdom.\n"
              "King Victor is in distress, his people are dying and if this curse is not cleansed soon \n"
              "the kingdom may be entirely wiped out. You heard his call, promising the title of Lord and land to \n"
              "any adventurer that may cure the land of the curse.\n")

# ---------------------------------------------------GAME DATA------------------------------------------------------- #

username = None

# All the map zones and descriptions of the zone
zones = {
    "Mountain Peak":"The top is frigid and windy. You discover a statue of female, standing prideful with the sun"
                    "glistening upon it. There is a family praying in front of the statue, with a small basket of "
                    "offerings placed at its feet.",
    "Path to Mountain Peak":"There are still signs of recent tracks to the peak. You wonder what is at the top",
    "Abandoned Village":"The village looks to be abandoned years ago. When King Victor declared his lordship over these"
                        "lands, many of the smaller villages were abandoned for promise of their own farmland on more "
                        "fertile pastures.",
    "Mountain Pass":"The pass is narrow and not well maintained. Still you persevere through",
    "Base of Mountain":"You reach the base of the mountain. There are signs of frequent travel. It is surprising that"
                       "the townsfolk would journey up the mountain in their weakened states.",
    "Town":"You are immediately hit with a stench of death and decay. There is no joy or hope left in this town."
           "You realize you must find a way to lift the curse before it's too late.",
    "West Swamp":"",
    "Cave Entrance":"You come across an unassuming cave entrance. Perhaps there is a clue here.",
    "Eastern Forest":"Much of this forest has been deforested to make room for farmland.",
    "East Swamp":"",
    "Deep Water":"The water is too deep to wade through. You will need a boat to cross",
    "Small Island":"The island has no signs of recent activity. There is not much here.",
    "Cavern":"The cavern is too dark to see very far, but you know it is vast from the echos. You were told that it"
             "is easy to get lost in here so you make sure you path carefully.",
    "Cave River":"There is a river flowing deeper into the cave. The water is warm to the touch. You think about taking"
                 "a dip, but the water is too deep and flowing too fast so you reconsider.",
    "Witch's Shack":"The witch invites you in. The smell is immediately intense, a mix of medicinal, rot, but also "
                    "floral aromas. You get slightly woozy just by being in the room.",
    "Wolf's Den":"You carefully enter the Wolf's Den. There is a stench of decaying meat. There are 2 wolves sleeping at"
                 "the back of the den. You should leave before they wake.",
    "Witch's Cellar":"It would be a mistake to enter while the witch is here. You should find a better time.",
    "Western Forest":"The forest if dense. You see part of the forest where they have harvest for wood, but it seems"
                     "there is little to no harvesting happening now",
    "Road to Riverstone":"The road has not been maintained in months.",
    "Guard Tower":"As you approach the guard tower, you notice that there are no guards currently posted",
    "Castle Gates":"As you draw closer, you notice a large crowd in front of the gates. There is a line of guards in"
                   "front of the gates blocking the crowd from entering the castle.",
    "Riverstone":"You won't be able to get past the crowd. You should find another way."
}

# Zone connections for traversal
directions = {
    "Mountain Peak":{"north":None,"east":None,"south":"Path to Mountain Peak","west":None},
    "Path to Mountain Peak":{"north":"Mountain Peak","east":None,"south":"Abandoned Village","west":None},
    "Abandoned Village":{"north":"Path to Mountain Peak","east":"Cave Entrance","south":"Mountain Pass","west":None},
    "Mountain Pass":{"north":"Abandoned Village","east":None,"south":"Base of Mountain","west":None},
    "Base of Mountain":{"north":"Mountain Pass","east":None,"south":"Town","west":None},
    "Town":{"north":"Mountain Pass","east":"Eastern Forest","south":"West Swamp","west":"Western Forest"},
    "West Swamp":{"north":"Town","east":"East Swamp","south":None,"west":"Road to Riverstone"},
    "Cave Entrance":{"north":None,"east":"Cavern","south":None,"west":"Abandoned Village"},
    "Eastern Forest":{"north":None,"east":None,"south":"East Swamp","west":"Town"},
    "East Swamp":{"north":"Eastern Forest","east":"Witch's Shack","south":"Deep Water","west":"West Swamp"},
    "Deep Water":{"north":"East Swamp","east":None,"south":"Small Island","west":None},
    "Small Island":{"north":"Deep Water","east":None,"south":None,"west":None},
    "Cavern":{"north":"Cave Entrance","east":None,"south":"Cave River","west":"Wolf's Den"},
    "Cave River":{"north":"Cavern","east":None,"south":None,"west":None},
    "Witch's Shack":{"north":None,"east":"Witch's Cellar","south":None,"west":"East Swamp"},
    "Wolf's Den":{"north":None,"east":None,"south":None,"west":"Cavern"},
    "Witch's Cellar":{"north":None,"east":None,"south":None,"west":"Witch's Shack"},
    "Western Forest":{"north":None,"east":"Town","south":"Road to Riverstone","west":None},
    "Road to Riverstone":{"north":"Western Forest","east":"West Swamp","south":None,"west":"Guard Tower"},
    "Guard Tower":{"north":None,"east":"Road to Riverstone","south":None,"west":"Castle Gates"},
    "Castle Gates":{"north":None,"east":"Guard Tower","south":None,"west":"Riverstone"},
    "Riverstone":{"north":None,"east":"Castle Gates","south":None,"west":None}
}


# ------------------------------------------------START FUNCTIONS----------------------------------------------------- #
def exit_game():
    while True:
        check = input("Are you sure you want to exit the game? Your progress will not be saved. (Y/N) ")
        if check.lower() == "n":
            return
        if check.lower() == "y":
            print("Thank you for playing! Game will exit in 3 seconds.")
            time.sleep(3)
            exit()
        else:
            print("Sorry I could not understand that command. Please try another command.")


def change_log():
    """
    Returns change log by version
    """
    print("Your current version is v1")
    while True:
        version = input("Type in the version you would like to see or 'back' to go back (v1, v2, etc): ")
        if version == "back":
            return
        if version in changelog:
            for i in range(len(changelog[version])):
                print(changelog[version][i])
            print("\n")
        else:
            comm_err()


def about():
    print(about_game)

def comm_err():
    print(error_command)
def start_menu():
    """
    Acts as a start menu for the game
    """
    print(game_name)
    print(welcome_message)
    print(start_instructions)
    for option in start_commands:
        print(option,":", start_commands[option])
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



# ------------------------------------------------GAME FUNCTIONS----------------------------------------------------- #

def change_name():
    """
    Changes the name of the adventurer
    """
    global username
    while True:
        if username:
            pre_username = input("What would you like to change your name to? ")
        else:
            pre_username = input("What is your name adventurer? ")
        confirm = input(f"Change your name to {pre_username}? (Y/N) ")
        if confirm == 'y':
            username = pre_username
            return
        elif confirm == 'n':
            continue
        else:
            comm_err()

def help():
    for option in help_commands:
        print(option,":", help_commands[option])
    print("\n")

def introduction():
    change_name()
    print(game_intro)
    print(help_info)

def start_game():
    """
    Starts the character in the town and allows user to traverse the map
    """
    location = "Town"
    while True:
        print(f"You enter the {location}.")
        print(zones[location])
        for option in directions[location]:
            if directions[location][option] is not None:
                print(option, ":", directions[location][option])
        command = input("What would you like to do? ")
        print("\n")
        if command.lower() == "exit":
            exit_game()
        elif command.lower() == "changename":
            change_name()
        elif command.lower() == "help":
            help()
        elif command.lower() in directions[location]:
            if directions[location][command] is None:
                print("You cannot go that way.")
            else:
                location = directions[location][command]
        else:
            comm_err()

start_menu()
introduction()
start_game()