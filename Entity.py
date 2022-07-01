import Game


class Entity:

    """A generic interface implemented by all items in the game."""

    def __init__(self, name, other_names, description, location, size=1, strength=0, capacity=0, hoistable=True, destroyable=False, open=False, openable=False):
        
        """Args:
            name (str): The primary title of the game entity
            other_names (tuple, str): Additional ways the entity may be referenced
            description (str): The detailed description of the entity
            location (Room/Entity): Another object in the game which contains this instance
            size (int): The amount of space taken up by the entity (default is 1)
            strength (int): Resistance of entity to destruction or entity's destructive potential (default is 0)
            capacity (int): Units of size which can be contained in the entity (default is 0)
            hoistable (bool): Can the entity be moved/picked up? (default is False)
            destroyable (bool): Can the entity be destroyed? (default is False)
            open (bool): Is the entity open? (default is False)
            openable (bool): Can the entity be opened? Is it unlocked? (default is False)"""

        self.names = (name,) + other_names
        self.description = description
        self.location = location
        self.size = size
        self.hoistable = hoistable
        self.destroyable = destroyable
        self.strength = strength
        self.capacity = capacity
        self.open = open
        self.openable = openable
        print()

        if Game.DEBUG:
            Game.log("Entity initialized. Name: {name}.\tLocation: {location}".format(name=name, location=location))
    
    
    def __str__(self):

        """Overloads the builtin string method.
        
        Returns:
            str: The primary name of the entity"""
        
        return self.names[0]


    def __eq__(self, other):

        """Overloads the builtin comparison method.
        
        Returns:
            bool: Are the primary names equal?"""

        return self.__str__() == other.__str__()

