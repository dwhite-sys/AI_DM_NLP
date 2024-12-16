# Information (dict)
    # Name (str)
    # Description (str)
    # Exits (list)
# States (dict)
    # Event name (str)
        # Trigger (str)
        # Consequences (str)
        # Active (bool)
# Objects (list of object instances)

class scene:
    def __init__(self, details:dict, objects:list=[], events:dict={}):
        
        self.details = details
        self.objects = objects
        self.events = events