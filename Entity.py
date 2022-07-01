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

        if Game.DEBUG:
            Game.log("Entity initialized. Name: {name}.\tLocation: {location}".format(name=name, location=location))
    
    
    def __str__(self):

        """Overloads the builtin string method.
        
        Returns:
            str: The primary name of the entity"""
        
        return self.names[0]


    def __eq__(self, other):

        """Overloads the builtin comparison method.

        Args:
            other (Entity): Another entity
        
        Returns:
            bool: Are the primary names equal?"""

        return self.__str__() == other.__str__()


    def per_turn(self):

        """Should be called every turn on every entity. Logs state of object and may be overloaded for custom behavior."""

        if Game.DEBUG:
            Game.log("Game state update. Location of {name} is {location}".format(name=self.names[0], location=self.location))


    def examine(self):

        """Gives further details about the entity when the player requests them.
        
        Returns:
            str: Description of entity"""

        return self.description


    def take(self):

        """Puts the entity in the player's inventory if possible.
        
        Returns:
            str: Success/failure message"""

        if not self.hoistable:
            return "You cannot pick up the {name}.".format(name=self.names[0])
        elif Game.inventory_size() + self.size <= Game.player.capacity:
            self.location = Game.player
            return "Taken."
        else:
            return "Your load is too heavy to pick up the {name}.".format(name=self.names[0])


    def drop(self):

        """Puts the entity in the player's current location.
        
        Returns:
            str: Success message"""

        self.location = Game.player.location
        return "Dropped."


    def open(self):

        """Opens the entity if possible.
        
        Returns:
            str: Success/failure message"""

        if self.open:
            return "The {name} is already open.".format(name=self.names[0])
        elif not self.openable:
            return "You cannot open the {name}".format(name=self.names[0])
        else:
            self.open = True
            return "Opened."


    def close(self):

        """Closes the entity if possible.
        
        Returns:
            str: Success/failure message"""

        if not self.openable:
            return "The {name} cannot be closed.".format(name=self.names[0])
        elif not open:
            return "The {name} is already closed.".format(name=self.names[0])
        else:
            self.open = False
            return "Closed."