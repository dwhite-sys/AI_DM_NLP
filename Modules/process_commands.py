#--------------------------------------------------------------------------------------------------------------
#   Dependencies
#--------------------------------------------------------------------------------------------------------------

#------------------
#-   Libraries    -
#------------------

#     (None)

#------------------
#-   Modules      -
#------------------

from Modules.Classes.object_class import Base_Object
from Modules.execute_actions import actions
from Modules.fetch_objects import get_all_objects

#-------------------------------------------------------------------------------------------------------------------------
#-   Process explanation                                                                                                 -
#-------------------------------------------------------------------------------------------------------------------------
# commands - converted command list                                                                                      -
#     -> process command - passes to either simple command (no instrument) or complex command (w/ an instrument)         -
#             -> simple command                                                                                          -
#                -> split into action and target                                                                         -
#                   -> look through all the objects                                                                      -
#                      -> match to target                                                                                -
#                         -> look through all the interactions                                                           -
#                            -> look through all its interactions                                                        -
#                               -> if a match is found, check if its source is the player                                -
#                                   -> look through interaction causes                                                   -
#                                       -> if a match is found, execute action using actions module                      -
#                                                                                                                        -
#             -> complex command                                                                                         -
#                -> split in to instrument, action, and target strings                                                   -
#                   -> look through all the objects                                                                      -
#                      -> match to instrument and target                                                                 -
#                         -> make sure they've both been matched by checking if they're both objects instead of strings  -
#                            -> execute action function listed below                                                     -
#                                                                                                                        -
#             -> execute action                                                                                          -
#               -> check for matching action in instrument action                                                          -
#                  -> search through target interactions                                                                 -
#                     -> find matching "from" cause                                                                      -
#                        -> execute action using actions module if found                                                 -
#                           -> if not, find matching "from" state                                                        -
#                              -> execute action using actions module if found                                           -
#-------------------------------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------------------
#   Execute Simple Actions (action + target)
#--------------------------------------------------------------------------------------------------------------

# A simple interaction involves an object being indirected with directly by the player (e.g., "I open the door")
def simple_command(command, location, inventory, notifications):
    action, target = command.split(':')
    for object in get_all_objects(location.area, inventory):
        if object.name.lower() == target:
            target = object
            interactions = target.interactions
            if action in interactions:
                for cause in interactions[action]:
                    if cause == 'player':
                        actions[action](target, location, inventory, notifications)

#--------------------------------------------------------------------------------------------------------------
#   Grab the objects for Complex Actions (instrument + action + target)
#--------------------------------------------------------------------------------------------------------------

def complex_command(command, location, inventory, notifications):
    instrument, action, target = command.split(':')
    for object in get_all_objects(location.area, inventory):
        if object.name.lower() == instrument:
            instrument = object
        elif object.name.lower() == target:
            target = object
    if type(target) == Base_Object and type(instrument) == Base_Object:
        execute_action(instrument, action, target, location, inventory, notifications)
    else:
        print('did nothing')

#--------------------------------------------------------------------------------------------------------------
#   Execute Action for Complex Actions
#--------------------------------------------------------------------------------------------------------------
        
def execute_action(instrument, action, target, location, inventory, notifications):
    did_action = False
    instrument_interactions = instrument.interactions
    if action in instrument_interactions:
        target_interactions = target.interactions
        for interaction in target_interactions:
            for cause in target_interactions[interaction]:
                if f'cause {interaction}' in instrument_interactions[action]:
                    if cause == f'because {action}':
                        actions[interaction](target, location, inventory, notifications)
                else:
                    for state in instrument.states:
                        if cause == f'when {state} true':
                            if instrument.states[state] == True:
                                actions[interaction](target, location, inventory, notifications)
                        if cause == f'when {state} false':
                            if target.states[state] == False:
                                actions[interaction](target, location, inventory, notifications)


#--------------------------------------------------------------------------------------------------------------
#   Catagorize Commands into Simple or Complex
#--------------------------------------------------------------------------------------------------------------
# Determine whether an action is complex or simple.
def process_commands(input:str, location, inventory, notifications) -> None:
    if input != 'failure':
        for command in input:
            dividers = command.count(':')
            if dividers == 2:
                 complex_command(command, location, inventory, notifications)
            elif dividers == 1:
                simple_command(command, location, inventory, notifications)

#--------------------------------------------------------------------------------------------------------------
#   End of Command Interpreter
#--------------------------------------------------------------------------------------------------------------