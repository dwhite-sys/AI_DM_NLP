from Modules.Classes.object_class import create_object_from_types
from Modules.Classes.scene_class import scene

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
In it you will explore some of the most amaz- deja vu...
Anywho, no computer should be without a copy!'''
                    },
                    interactions= {
                        'read':['player']
                    }
                )]
            }
        ),
        create_object_from_types(
            name = 'Branch',
            description = 'A small but hearty branch.',
            types=['flammable', 'breakable', 'item'],
            interactions={
                'hit':['cause break']
            }
        ),
        create_object_from_types(
            name = 'Match',
            description = 'A simple match.',
            types=['flammable', 'breakable', 'item'],
            states={'on fire':False},
            interactions={
                'ignite':['player']
            }
        ),
        create_object_from_types(
            name = 'Window',
            description = 'A shattered window.',
            properties = {
                'leads to':'house',
            },
            types=['breakable', 'openable', 'enterable'],
            states={
                'broken':True,
                'leads to ':'house'},
            interactions={
                'enter':['player'],
            }
        ),
    ]
)