#--------------------------------------------------------------------------------------------------------------
#   Dependencies
#--------------------------------------------------------------------------------------------------------------

#------------------
#-   Libraries    -
#------------------

import queue

#------------------
#-   Modules      -
#------------------

from Modules.simplify import clear
from Modules.process_commands import process_commands
from Modules.process_text import process_text
from Modules.Classes.location_class import location
from Data.Scenes.house import area as house
from Data.Scenes.front_lawn import area as front_lawn

#! TODO: Test synonyms using the function dictionary
#! TODO: Make things like "small bag" work. Objects can only be one word currently.
#! TODO: Some kind of "Deposit" command
#! TODO: Lastly, add normalization using an LLM. This might fix "small bag" not working on its own.


#---------------------------------------------------------------------------------------
#-   Process explanation                                                               -
#---------------------------------------------------------------------------------------
# Process: main - user input                                                           -
#           -> process_text - list of converted "instrument:action:target" commands    -
#                       -> process_command - processes each command                    -
#                                      -> actions - executes the commands              -
#---------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------
#   Initializations
#--------------------------------------------------------------------------------------------------------------

notifications = queue.Queue()

inventory = {
    'items':[],
    'equipped':None
}

#--------------------------------------------------------------------------------------------------------------
#   Functions
#--------------------------------------------------------------------------------------------------------------

current_location = location('front lawn',{
    'front lawn':front_lawn,
    'house':house
})

#--------------------------------------------------------------------------------------------------------------
#   Functions
#--------------------------------------------------------------------------------------------------------------

#------------------
#-  Notifications -
#------------------
def display_notifs():
    while not notifications.empty():
        print(notifications.get())

#------------------
#-   Game Loop    -
#------------------
def prompt_user():
    # Grab user input
    user_input = input("> ").lower()

    # Process user input into commands, then into actions
    command_list = process_text(user_input)
    process_commands(command_list, current_location, inventory, notifications)
    # print(command_list) # Debug the commands

    # Read off notifications
    display_notifs()

    # Repeat process
    print()
    prompt_user()

#--------------------------------------------------------------------------------------------------------------
#   Initialization
#--------------------------------------------------------------------------------------------------------------
def main():
    clear()
    print(current_location.area.details['name'])
    print(current_location.area.details['desc'])
    print('Contains: ')
    print(*(f' - {i.name}' for i in current_location.area.objects), sep='\n')
    print()
    prompt_user()
    
main()