class Area:

    types = ['grass', 'street', 'garbage_dump']

    def __init__(self, type):
        self.type = type
        if type == 'grass':
            self.image = "grass_url"
        elif type == 'street':
            self.image = "street_url"
        elif type == 'garbage_dump':
            self.image = "garbage_dump_url"
