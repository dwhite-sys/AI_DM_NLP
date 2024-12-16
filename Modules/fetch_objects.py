def fetch_objects(list):
    grabbed_objects = []
    for object in list:
        grabbed_objects.append(object)
        if 'contains' in object.properties:
            visible = True
            if 'closed' in object.states:
                if object.states['closed'] == True:
                    visible = False
            if visible == True:
                grabbed_objects += fetch_objects(object.properties['contains'])
    
    return grabbed_objects

def fetch_parent(list, target):
    parent = None
    for object in list:
        if object == target:
            parent = list
            break
        if 'contains' in object.properties:
            visible = True
            if 'closed' in object.states:
                if object.states['closed'] == True:
                    visible = False
            if visible == True:
                parent = fetch_parent(object.properties['contains'], target)
    return parent

def get_all_objects(area, inventory):
    objects_in_area = fetch_objects(area.objects)
    objects_in_inventory = fetch_objects(inventory['items'])
    all_objects = objects_in_area + objects_in_inventory
    return all_objects