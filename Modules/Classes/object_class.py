# Name (str)
# Description (str)
# Type (str)
# Properties
    # Property Name (str): Value (size, bool, etc) (str)
# States:
    # State name (on fire, broken, etc) (str): Active (bool)
# Interactions:
    # Interaction name (hit, pick up, etc) (str), Target type (flammable, player, etc) (str)

class Base_Object:
    def __init__(self, name:str, description:str, properties:dict={}, states:dict={}, interactions:dict={}) -> object:
        '''
        Example:
        Name: Branch
        Description: A small but hearty branch. 
        Properties:
            Size: 'short'
            Weight: 'light'
            Anchored: False
        States:
            on fire: no
            broken: no
        Actions on other objects (action, target):
            hit -> any
        To change states, an interaction must make sense.
        '''

        self.name = name
        self.description = description
        self.properties = properties
        self.states = states
        self.interactions = interactions

# Types stores arguments

type_templates = {
    'flammable':{'properties':{'flammable':True}, 'states':{'on fire':False},'interactions':{'ignite':['when on fire true']}},
    'item':{'interactions':{'pick up':['player'], 'drop':['player']}},
    'set piece':{'properties':{'movable':False}},
    'breakable':{'properties':{'breakable':True}, 'states':{'broken':False}, 'interactions':{'break':['because hit']}},
    'container':{'properties':{'container':True}, 'interactions':['open']},
    'openable':{'states':{'closed':True}, 'interactions':{'open':['player'], 'close':['player']}},
    'enterable':{'properties':{'leads to':'location'},'interactions':{'enter':['go to front lawn']}},
}

def create_object_from_types(name:str, description:str, types:list=[], properties:dict={}, states:dict={}, interactions:dict={}):

    # Create a blank version of each property if there isn't one passed as an argument.
    properties = {} if not properties else properties
    states = {} if not states else states
    interactions = {} if not interactions else interactions

    for i in types:
        if i in list(type_templates):
            if 'properties' in type_templates[i]:
                properties = {**type_templates[i]['properties'], **properties}
            if 'states' in type_templates[i]:
                states = {**type_templates[i]['states'], **states}
            if 'interactions' in type_templates[i]:
                interactions = {**type_templates[i]['interactions'], **interactions}
    item = Base_Object(name, description, properties, states, interactions)
    return item

# Test item for debugging
# branch = create_object_from_types('Branch', 'A small but hearty branch.', ['flammable', 'item'] ,interactions={'hit':'any'})
# print(branch.interactions)



