import Game
from Room import Room


class Entity:

    """A superclass implemented by all items in the game."""

    def __init__(self,
        name, other_names, description, location,
        size=1, strength=0, capacity=0,
        hoistable=True, destroyable=False, open=False, openable=False, lightable=False, on=False,
        unlocks=None):
        
        """
        Args:
            name (str): The primary title of the game entity
            other_names (tuple, str): Additional ways the entity may be referenced
            description (str): The detailed description of the entity
            location (str): The name of another game object which contains this entity. Converted from str to object after initialization by snap
            size (int): The amount of space taken up by the entity (default is 1)
            strength (int): Resistance of entity to destruction or entity's destructive potential (default is 0)
            capacity (int): Units of size which can be contained in the entity (default is 0)
            hoistable (bool): Can the entity be moved/picked up? (default is True)
            destroyable (bool): Can the entity be destroyed? (default is False)
            open (bool): Is the entity open? (default is False)
            openable (bool): Can the entity be opened/closed? Is it unlocked? (default is False)
            lightable (bool): Can the entity be used as a light? (default is False)
            on (bool): Is the entity on? (default is False)
            unlocks (tuple, str): The names of all entities which this entity can unlock. Converted from str to object after initialization by snap (default is None)"""

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
        self.lightable = lightable
        self.on = on
        self.unlocks = unlocks

        if Game.DEBUG:
            Game.log("Entity initialized. Name: {name}.\tLocation: {location}".format(name=str(self), location=str(self.location)))
    
    
    def __str__(self):

        """Overloads the builtin string method.
        Returns:
            str: The primary name of the entity"""
        
        return self.names[0].lower()


    def __repr__(self):

        """Overloads the builtin representation method.
        Returns:
            str: The identifier of the entity for internal use"""

        return " - ".join(self.names).lower()


    def __eq__(self, other):

        """Overloads the builtin comparison method.
        Args:
            other: Another object 
        Returns:
            bool: Are the representations equal?"""

        return self.__hash__() == other.__hash__()
    

    def __hash__(self):

        """Overloads the builtin hash method.
        Returns:
            str: The hash code that represents the entity."""

        return hash(self.__repr__())


    def snap(self):

        """Converts strings to object references when possible. Should be called on all entities at session start."""

        if type(self.location) == str:
            self.location = Game.object_from_str(self.location)
        if self.unlocks and type(self.unlocks[0]) == str:
            self.unlocks = (Game.object_from_str(entity) for entity in self.unlocks)


    def contents(self):

        """Identifies entities which consider this entity their container.
        Returns:
            tuple, Entity: All entities which this entity contains"""

        ans = ()

        for item in Game.entities:
            if item.location == self:
                ans = ans + (item,)

        return ans


    def contents_size(self):

        """Sums the size attributes of each entity which considers this entity its container.
        Returns:
            int: The size of this entity's contents"""

        ans = 0
        for item in self.contents():
            ans += item.size

        return ans


    def per_turn(self):

        """Should be called every turn on every entity. Logs state of object and may be overloaded for custom behavior."""

        if Game.DEBUG:
            Game.log("Game state update. Location of {name} is {location}".format(name=str(self), location=self.location))


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
            return "You cannot pick up the {name}.".format(name=str(self))
        elif Game.player.contents_size() + self.size <= Game.player.capacity:
            self.location = Game.player
            return "Taken."
        else:
            return "Your load is too heavy to pick up the {name}.".format(name=str(self))


    def drop(self):

        """Puts the entity in the player's current location.
        Returns:
            str: Success message"""

        self.location = Game.player.location
        return "Dropped."


    def put_in(self, other):

        """Puts the entity in the target location if possible.
        Args:
            other (Entity): The object which the entity will be put into    
        Returns:
            str: Success/failure message"""

        if not other.openable:
            return "The {other_name} is not the sort of thing you can put the {name} into.".format(other_name=str(other), name=str(self))
        elif not other.open:
            return "The {other_name} is closed.".format(other_name=str(other))
        elif other.contents_size() + self.size <= other.size:
            self.location = other
            return "The {name} is now in the {other_name}.".format(name=str(self), other_name=str(other))
        else:
            return "There is not enough room in the {other_name} for the {name}".format(other_name=str(other), name=str(self))


    def open(self):

        """Opens the entity if possible.
        Returns:
            str: Success/failure message"""

        if self.open:
            return "The {name} is already open.".format(name=str(self))
        elif not self.openable:
            return "You cannot open the {name}".format(name=str(self))
        else:
            self.open = True
            return "Opened."


    def close(self):

        """Closes the entity if possible.
        Returns:
            str: Success/failure message"""

        if not self.openable:
            return "The {name} cannot be closed.".format(name=str(self))
        elif not open:
            return "The {name} is already closed.".format(name=str(self))
        else:
            self.open = False
            return "Closed."


    def unlock(self, unlocker):

        """Allows the entity to be opened if possible.
        Args:
            unlocker (Entity): The item being used to unlock this entity    
        Returns:
            str: Success/failure message"""

        if self.openable:
            return "The {name} can already be opened."
        elif self in unlocker.unlocks:
            self.openable = True
            return "You unlock the {name}.".format(name=str(self))
        else:
            return "You cannot unlock the {name} with the {other_name}.".format(name=str(self), other_name=str(unlocker))

    
    def lock(self, locker):

        """Prevents the entity from being opened if possible.
        Args:
            locker (Entity): The item being used to lock this entity     
        Returns:
            str: Success/failure message"""

        if not self.openable:
            return "The {name} is already unopenable.".format(name=str(self))
        elif self in locker.unlocks:
            self.openable = False
            return "You lock the {name}".format(name=str(self))
        else:
            return "You cannot lock the {name} with the {other_name}".format(name=str(self), other_name=str(locker))


    def turn_on(self):

        """Turns on the entity if possible.
        Returns:
            str: Successs/failure message"""

        if self.on:
            return "The {name} is already open.".format(name=str(self))
        elif not self.lightable:
            return "The {name} cannot be turned on.".format(name=str(self))
        else:
            self.on = True
            return "It is now on."


    def turn_off(self):

        """Turns off the entity if possible.
        Returns:
            str: Successs/failure message"""

        if not self.lightable:
            return "The {name} is not a thing you can turn off.".format(name=str(self))
        elif not self.on:
            return "The {name} is already on.".format(name=str(self))
        else:
            return "It is now off."


    def hit(self, indirect_object):

        """Handles this entity being hit with another entity.
        Args:
            indirect_object (Entity): The entity being used to hit this one 
        Returns:
            str: Success/failure message"""

        if (not self.destroyable) or (indirect_object.strength <= 0):
            return "You are unable to destroy the {name} with the {other_name}.".format(name=str(self), other_name=str(indirect_object))
        else:
            self.strength -= indirect_object.strength
            if self.strength < 0:
                self.location = None
                return "With a swift blow from the {other_name}, the {name} is destroyed.".format(other_name=str(indirect_object), name=str(self))
            else:
                return "You damage the {other_name}.".format(other_name=str(indirect_object))


    def say(self, text):

        """Handles this entity being spoken to.
        Args:
            text (str): The words said to the entity    
        Returns:
            str: The entity's response or a failure message"""

        return "The {name} is unresponsive.".format(name=str(self))


    def move(self, direction):

        """Moves this entity through an exit if possible.
        Args:
            direction (str): n, e, s, w, ne, se, sw, nw, u, or d
        Returns:
            str: Failure message or empty string for success"""

        ans = self.location.move(self, direction)
        if type(ans) == str:
            return ans
        self.location = ans

        return ""

    def look(self):
        
        """Returns the description and contents of the location of the entity
        Returns:
            str: description of the location and a list of its contents"""
        
        name = self.location.__str__()
        description = self.location.examine()
        contents = self.location.contents()

        description = name + "\n" + description

        if len(contents) != 0:

            description += "\nHere you see:\n"

            for item in contents:

                description += item + "\n"
        
        return description