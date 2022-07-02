from Entity import Entity


class Character(Entity):

    """A subclass of Entity implemented by all living things in the game."""

    def __init__(self,
        name, other_names, description, location,
        size=20, strength=20, capacity=10,
        hoistable=False, destroyable=True, open=False, openable=False, lightable=False, on=False,
        unlocks=None):

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

        Entity.__init__(self,
            name, other_names, description, location,
            size=size, strength=strength, capacity=capacity,
            hoistable=hoistable, destroyable=destroyable, open=open, openable=openable, lightable=lightable, on=on,
            unlocks=unlocks)

        
    def __str__(self):

        """Overloads the builtin string method.
        Returns:
            str: The primary name of the character"""
        
        return self.names[0].lower()
