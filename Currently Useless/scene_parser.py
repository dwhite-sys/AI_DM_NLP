# Detail a specific object.
def grab_object_details(object, info, depth=''):
    info += f'\n{depth}      -' + object.name
    # List object states
    info += f'\n{depth}         Current state:'
    for state in object.states.keys():
        # Bools become yes and no so the AI can understand it better
        condition = str(object.states[state]) if object.states[state] != True and object.states[state] != False else "yes" if object.states[state] != False else "no"
        info += f'\n{depth}            -' + state + ": " + condition
    if not object.states.keys():
        # If there isn't any states, say so.
        info += f'\n{depth}            (None)'
    info += f'\n{depth}         Properties:'

    # List properties
    for property in object.properties.keys():
        # Contains and text have to be handled seperately. Contains is a list of its own and its contents being visible are dependent on whether it's open. Text has special instructions.
        if property != 'contains' and property != 'text':
            info += f'\n{depth}            -' + property
        elif property == 'contains':
            if not 'closed' in object.states:
                # Add everything it contains to the output.
                info += f'\n{depth}         Contains:'
                for item in object.properties[property]:
                    info = grab_object_details(item, info, '      ')
            else:
                if object.states['closed'] == False:  
                    # If it isn't closed, add the items it contains
                    info += f'\n{depth}         Contains:' 
                    for item in object.properties[property]:
                        info = grab_object_details(item, info, '      ')
                else:
                    # If it's closed, say its contents are hidden.
                    info += f'\n{depth}         Contains:' 
                    info += f'\n{depth}            (contents hidden - closed)'
        elif property == 'text':
            info += f'\n{depth}            -text: (read in entirely when prompted)"{object.properties['text']}"'
    # If there isn't any properties, say so.
    if not object.properties.keys():
        info += f'\n{depth}            (None)'
            
    # List interactions
    info += f'\n{depth}         Interactions: (to the AI: to facilitate one of the listed,  respond with "You attempt to [action] the [object]. /interact" (with correct grammar)'
    if not object.interactions.keys():
        info += f'\n{depth}            (None)'
    for interaction in object.interactions.keys():
        info += f'\n{depth}            -' + interaction + " (" + str(object.interactions[interaction]) + ")"
    return info

# Start detail extraction
def extract_details(area):
    info = ''
    info += f'''Scene: {area.details['name']} 
    Details:
        -Description: {area.details['desc']}

    Objects:'''
    for object in area.objects:
        info = grab_object_details(object, info, )
    return info
