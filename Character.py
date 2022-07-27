from Game import game
from Entity import Entity


class Character(Entity):

    """A subclass of Entity implemented by all living things in the game."""

    def __init__(self,
        name, other_names, description, location,
        size=20, strength=20, capacity=10,
        hoistable=False, destroyable=True, open=False, openable=False, lightable=False, on=False,
        unlocks=[None]):

        """
        Args:
            name (str): The primary title of the game character
            other_names (tuple, str): Additional ways the character may be referenced
            description (str): The detailed description of the character
            location (str): The name of another game object which contains this character. Converted from str to object after initialization by snap
            size (int): The amount of space taken up by the character (default is 20)
            strength (int): Resistance of character to destruction (default is 20)
            capacity (int): Units of size which can be contained in the character (default is 10)
            hoistable (bool): Can the character be moved/picked up? (default is False)
            destroyable (bool): Can the character be destroyed? (default is True)
            open (bool): Is the character open? (default is False)
            openable (bool): Can the character be opened/closed? Is it unlocked? (default is False)
            lightable (bool): Can the character be used as a light? (default is False)
            on (bool): Is the character on? (default is False)
            unlocks (tuple, str): The names of all entities which this character can unlock. Converted from str to object after initialization by snap (default is None)"""

        super.__init__(self,
            name, other_names, description, location,
            size=size, strength=strength, capacity=capacity,
            hoistable=hoistable, destroyable=destroyable, open=open, openable=openable, lightable=lightable, on=on,
            unlocks=unlocks)


    def __str__(self):

        """Overloads the builtin string method.
        Returns:
            str: The primary name of the entity"""

        return self.names[0]


    def take(self):

        """Puts the character in the player's inventory if possible.
        Returns:
            str: Success/failure message"""

        if not self.hoistable:
            return "You cannot pick up {name}.".format(name=str(self))
        elif game.player.contents_size() + self.size <= game.player.capacity:
            self.location = game.player
            return "Taken."
        else:
            return "Your load is too heavy to pick up {name}.".format(name=str(self))


    def put(self, other):

        """Puts the character in the target location if possible.
        Args:
            other (Entity): The object which the character will be put into
        Returns:
            str: Success/failure message"""

        if not other.openable:
            return "The {other_name} is not the sort of thing you can put {name} into.".format(other_name=str(other), name=str(self))
        elif not other.open:
            return "The {other_name} is closed.".format(other_name=str(other))
        elif other.contents_size() + self.size <= other.size:
            self.location = other
            return "{name} is now in the {other_name}.".format(name=str(self), other_name=str(other))
        else:
            return "There is not enough room in the {other_name} for {name}.".format(other_name=str(other), name=str(self))


    def open(self):

        """Opens the character if possible.
        Returns:
            str: Success/failure message"""

        if self.open:
            return "{name} is already open.".format(name=str(self))
        elif not self.openable:
            return "You cannot open {name}.".format(name=str(self))
        else:
            self.open = True
            return "Opened."


    def close(self):

        """Closes the character if possible.
        Returns:
            str: Success/failure message"""

        if not self.openable:
            return "{name} cannot be closed.".format(name=str(self))
        elif not open:
            return "{name} is already closed.".format(name=str(self))
        else:
            self.open = False
            return "Closed."


    def unlock(self, unlocker):

        """Allows the character to be opened if possible.
        Args:
            unlocker (Entity): The item being used to unlock this character
        Returns:
            str: Success/failure message"""

        if self.openable:
            return "{name} can already be opened."
        elif self in unlocker.unlocks:
            self.openable = True
            return "You unlock {name}.".format(name=str(self))
        else:
            return "You cannot unlock {name} with the {other_name}.".format(name=str(self), other_name=str(unlocker))


    def lock(self, locker):

        """Prevents the character from being opened if possible.
        Args:
            locker (Entity): The item being used to lock this character
        Returns:
            str: Success/failure message"""

        if not self.openable:
            return "{name} is already unopenable.".format(name=str(self))
        elif self in locker.unlocks:
            self.openable = False
            return "You lock {name}.".format(name=str(self))
        else:
            return "You cannot lock the {name} with the {other_name}".format(name=str(self), other_name=str(locker))


    def turn_on(self):

        """Turns on the character if possible.
        Returns:
            str: Successs/failure message"""

        if self.on:
            return "{name} is already on.".format(name=str(self))
        elif not self.lightable:
            return "{name} cannot be turned on.".format(name=str(self))
        else:
            self.on = True
            return "On."


    def turn_off(self):

        """Turns off the character if possible.
        Returns:
            str: Successs/failure message"""

        if not self.lightable:
            return "{name} is not a thing you can turn off.".format(name=str(self))
        elif not self.on:
            return "{name} is already on.".format(name=str(self))
        else:
            return "Off."


    def hit(self, indirect_object):

        """Handles this character being hit with another entity.
        Args:
            indirect_object (Entity): The entity being used to hit this one
        Returns:
            str: Success/failure message"""

        if (not self.destroyable) or (indirect_object.strength <= 0):
            return "You are unable to kill {name} with the {other_name}.".format(name=str(self), other_name=str(indirect_object))
        else:
            self.strength -= indirect_object.strength
            if self.strength < 0:
                self.location = None
                return "With a swift blow from the {other_name}, {name} is slain.".format(other_name=str(indirect_object), name=str(self))
            else:
                return "You strike {name}.".format(name=str(self))


    def say(self, text):

        """Handles this character being spoken to.
        Args:
            text (str): The words said to the character
        Returns:
            str: The entity's response or a failure message"""

        return "\"Hello!\" says {name}.".format(name=str(self))
