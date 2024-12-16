from Modules.Classes.object_class import create_object_from_types, Base_Object
from Modules.scene_parser import extract_details
from Modules.Classes.scene_class import scene

def get_objects():
    all_objects = []
    for object in area.objects:
        all_objects.append(object)
        if 'contains' in object.properties:
            visible = True
            if 'closed' in object.states:
                if object.states['closed'] == True:
                    visible = False
            if visible == True:
                for item in object.properties['contains']:
                    all_objects.append(item)
    return all_objects

area = scene(
    details={
        'name':'Front lawn',
        'desc':'In front of a house with faded white point. It\'s windows and doors are boarded up.',
        'exits':'north, south'
    },
    objects = [
        create_object_from_types(
            name = 'Mailbox',
            description = 'A mailbox with fading white paint',
            types = ['flammable', 'set piece', 'breakable', 'openable'],
            properties = {
                'contains':[create_object_from_types(
                    name = 'Letter',
                    description = 'A crumpled but easily ledgible text',
                    types = ['flammable', 'item'],
                    properties = {
                        'text':'''Welcome to AI DM!
A game of adventure, danger and low cunning. 
In it you will explore some of the most amazing territory ever seen by- deja vu.
Anywho, no computer should be without one!'''
                    },
                    interactions= {
                        'read':'player'
                    }
                )]
            }
        ),
        create_object_from_types(
            name = 'Branch',
            description = 'A small but hearty branch.',
            types=['flammable', 'breakable', 'item'],
            interactions={
                'hit':'cause break'
            }
        ),
        create_object_from_types(
            name = 'Match',
            description = 'A simple match.',
            types=['flammable', 'breakable', 'item'],
            states={'on fire':False},
            interactions={
                'ignite':'player'
            }
        )
    ]
)

print(area.details['name'])
print(area.details['desc'])

inventory = {}

# player text -> object:action:target -> game logic -> one of the functions below

def action_break(target):
    if 'break' in target.interactions:
        if 'broken' in target.states:
            if target.states['broken'] == False:
                target.states['broken'] = True
                print(f'{target.name} is now broken.')
            else:
                print(f'{target.name} is already broken.')

def action_open(target):
    if 'open' in target.interactions:
        if 'closed' in target.states:
            if target.states['closed'] == True:
                target.states['closed'] = False
                print(f'{target.name} is now open.')
                if 'contains' in target.properties:
                    print(f"It contains: ")
                    for i in target.properties['contains']:
                        print(f'   -{i.name}')
            else:
                print(f'{target.name} is already open.')

def action_close(target):
    if 'close' in target.interactions:
        if 'closed' in target.states:
            if target.states['closed'] == False:
                target.states['closed'] = True
                print(f'{target.name} is now closed.')
            else:
                print(f'{target.name} is already closed.')

def action_read(target):
    if 'text' in target.properties:
        print(f'It reads:\n "{target.properties['text']}"')

def action_ignite(target):
    if 'ignite' in target.interactions:
        if 'on fire' in target.states:
            if target.states['on fire'] == False:
                target.states['on fire'] = True
                print(f'{target.name} is now on fire.')
            else:
                print(f'{target.name} is already on fire.')

# The dictionary used to call functions/game interactions.
reactions = {
    'break':action_break,
    'open':action_open,
    'close':action_close,
    'ignite':action_ignite,
    'read':action_read
}

# A simple interaction involves an object being indirected with directly by the player (e.g., "I open the door")
def simple_interaction(command):
    action, target = command.split(':')
    for object in get_objects():
        if object.name.lower() == target:
            target = object
            for interaction in target.interactions:
                if interaction == action:
                    source = target.interactions[interaction]
                    if source == 'player':
                        reactions[interaction](target)

# A complex interaction involves one object acting on another (e.g., "I unlock the door with the key"). 
def parse_complex_command(command):
    targeter, action, target = command.split(':')
    for object in get_objects():
        if object.name.lower() == targeter:
            targeter = object
        elif object.name.lower() == target:
            target = object
    if type(target) == Base_Object and type(targeter) == Base_Object:
        execute_action(targeter, action, target)
        
def execute_action(targeter, action, target):
    if action in targeter.interactions:
        for interaction in target.interactions:
            source = target.interactions[interaction]
            if source == f'from {action}':
                reactions[interaction](target)
            else:
                for state in target.states:
                    if source == f'from {state} true':
                        if targeter.states[state] == True:
                            reactions[interaction](target)
                    if source == f'from {state} false':
                        if target.states[state] == False:
                            reactions[interaction](target)

# Determine whether an action is complex or simple.
def process_command(input:str) -> None:
    if input != 'failure':
        for command in input:
            dividers = command.count(':')
            if dividers == 2:
                 parse_complex_command(command)
            elif dividers == 1:
                simple_interaction(command)
    
def process_text(user_input:str) -> str:
    targeter, action, target = None, None, None
    for object in get_objects():
        if f'with {object.name.lower()}' in user_input or f'with the {object.name.lower()}' in user_input:
            for interaction in object.interactions:
                if interaction in user_input:
                    action = interaction
                    targeter = object
        elif object.name.lower() in user_input:
            target = object
    output = 'failure'
    if target and targeter and action:
        # An object's interaction acting on another interaction.
        output = f'{targeter.name}:{action}:{target.name.lower()}'
        return output
    elif target:
        for interaction in target.interactions:
            if interaction in user_input:
                action = interaction
        if action:
            output = f'{action}:{target.name.lower()}'
    return [output]
         
def prompt_user():
    user_input = input("> ").lower()
    command = process_text(user_input)
    #print(command) # This prints out the command list.
    process_command(command)
    prompt_user()

def main():
    print(area.details['name'])
    print(area.details['desc'])
    prompt_user()
    
main()