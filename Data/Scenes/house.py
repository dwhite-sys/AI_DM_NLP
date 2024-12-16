from Modules.Classes.object_class import create_object_from_types
from Modules.Classes.scene_class import scene

area = scene(
    details={
        'name':'Interior of House',
        'desc':'A dark and gloomy interior of a house.',
        'exits':'north, south'
    },
    objects = [
        create_object_from_types(
            name = 'Window',
            description = 'A shattered window.',
            types=['breakable', 'openable', 'enterable'],
            properties = {
                'leads to':'front lawn',
            },
            states={
                'broken':True,
            },
            interactions={
                'enter':['player'],
            }
        ),
        create_object_from_types(
            name = 'Pouch',
            description = 'A small but slighly heavy bag',
            types = ['flammable', 'openable', 'item'],
            properties = {
                'contains':[create_object_from_types(
                    name = 'Coin',
                    description = 'Probably valuable',
                    types = ['item'],
                )]
            }
        ),
    ]
)