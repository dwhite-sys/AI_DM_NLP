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
import threading
from Modules.simplify import wait
from Modules.fetch_objects import fetch_objects, fetch_parent

#--------------------------------------------------------------------------------------------------------------
#   Individual actions
#--------------------------------------------------------------------------------------------------------------

# Actions
def action_enter(target, location, inventory, notifications):
    if 'enter' in target.interactions:
        if 'leads to' in target.properties:
            if target.properties['leads to'] in location.areas:
                location.change_area(target.properties['leads to'])
                print(f'Entered "{location.area.details['name']}".')

def action_break(target, location, inventory, notifications):

    if 'break' in target.interactions:
        if 'broken' in target.states:
            if target.states['broken'] == False:
                target.states['broken'] = True
                print(f'{target.name} is now broken.')
            else:
                print(f'{target.name} is already broken.')

def action_open(target, location, inventory, notifications):
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

def action_close(target, location, inventory, notifications):
    if 'close' in target.interactions:
        if 'closed' in target.states:
            if target.states['closed'] == False:
                target.states['closed'] = True
                print(f'{target.name} is now closed.')
            else:
                print(f'{target.name} is already closed.')

def action_read(target, location, inventory, notifications):
    if 'text' in target.properties:
        print(f'It reads:\n "{target.properties['text']}"')
    else:
        print(f'You can\'t read {target}.')

def action_ignite(target, location, inventory, notifications):
    if 'ignite' in target.interactions:
        if 'on fire' in target.states:
            if target.states['on fire'] == False:
                target.states['on fire'] = True
                print(f'{target.name} is now on fire.')
                def burn_to_ash(item_list):
                    if target.interactions['ignite'] != 'player':
                        wait(60)
                        destroy_object(target, item_list)
                        notifications.put(f"{target.name} burned to ash.")
                if target in location.area.objects:
                    thread = threading.Thread(target=burn_to_ash, args=(location.area.objects,))
                    thread.start()
                elif target in inventory['items']:
                    thread = threading.Thread(target=burn_to_ash, args=(inventory['items'],))
                    thread.start()
            else:
                print(f'{target.name} is already on fire.')

#--------------------------------------------------------------------------------------------------------------
#   Inventory interactions
#--------------------------------------------------------------------------------------------------------------

def action_pick_up(target, location, inventory, notifications):
    if target not in inventory['items'] and target in fetch_objects(location.area.objects):
        move_object(target, location.area.objects, inventory['items'])
        print(f"Picked up {target.name}")

def action_drop(target, location, inventory, notifications):
    if target not in location.area.objects and target in inventory['items']:
        move_object(target, inventory['items'], location.area.objects)
        print(f"Dropped {target.name}")

#--------------------------------------------------------------------------------------------------------------
#   Destroy/move items
#--------------------------------------------------------------------------------------------------------------

def destroy_object(object, current_list:list):
    current_list.remove(object)

def move_object(object, current_list:list, new_list:list):
    new_list.append(object)
    fetch_parent(current_list, object).remove(object)

#--------------------------------------------------------------------------------------------------------------
#   Dictionary for calling actions
#--------------------------------------------------------------------------------------------------------------

# The dictionary used to call functions/game interactions.
actions = {
    'break':action_break,
    'open':action_open,
    'close':action_close,
    'ignite':action_ignite,
    'read':action_read,
    'pick up':action_pick_up,
    'drop':action_drop,
    'enter':action_enter,
}

#--------------------------------------------------------------------------------------------------------------
#   Dictionary for calling actions
#--------------------------------------------------------------------------------------------------------------