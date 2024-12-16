scene_reference = '(scene object)'
class location:
    def __init__(self, starting_location:str='starting scene', areas:dict={'scene':scene_reference}):
        self.area = areas[starting_location]
        self.areas = areas

    def change_area(self, area:str):
        self.area = self.areas[area]
        print(self.area.details['name'])
        print(self.area.details['desc'])
        print('Contains: ')
        print(*(f' - {i.name}' for i in self.area.objects), sep='\n')