import Game


class Room:

    """A superclass implemented by all rooms in the game."""

    def __init__(self,
        name, description,
        n=(None,None), e=(None,None), s=(None,None), w=(None,None), ne=(None,None), se=(None,None), sw=(None,None), nw=(None,None), u=(None,None), d=(None,None),
        light=True):

        """
        Args:
            name (str): The room's title
            description (str): A description of the room
            n (tuple, (str, str)): The name of the room to the north of this one and the name of the door in between. Converted to objects after initialization by snap (default is (None, None))
            e (tuple, (str, str)): The name of the room to the east of this one and the name of the door in between. Converted to objects after initialization by snap (default is (None, None))
            s (tuple, (str, str)): The name of the room to the south of this one and the name of the door in between. Converted to objects after initialization by snap (default is (None, None))
            w (tuple, (str, str)): The name of the room to the west of this one and the name of the door in between. Converted to objects after initialization by snap (default is (None, None))
            ne (tuple, (str, str)): The name of the room to the northeast of this one and the name of the door in between. Converted to objects after initialization by snap (default is (None, None))
            se (tuple, (str, str)): The name of the room to the southeast of this one and the name of the door in between. Converted to objects after initialization by snap (default is (None, None))
            sw (tuple, (str, str)): The name of the room to the southwest of this one and the name of the door in between. Converted to objects after initialization by snap (default is (None, None))
            nw (tuple, (str, str)): The name of the room to the northwest of this one and the name of the door in between. Converted to objects after initialization by snap (default is (None, None))
            u (tuple, (str, str)): The name of the room above this one and the name of the door in between. Converted to objects after initialization by snap (default is (None, None))
            d (tuple, (str, str)): The name of the room below this one and the name of the door in between. Converted to objects after initialization by snap (default is (None, None))
            light (bool): Is there enough light to see without a lamp? (default is True)"""

        self.name = name
        self.description = description
        self.directions = {}
        self.directions["n"] = n if n[0] else None
        self.directions["e"] = e if e[0] else None
        self.directions["s"] = s if s[0] else None
        self.directions["w"] = w if w[0] else None
        self.directions["ne"] = ne if ne[0] else None
        self.directions["se"] = se if se[0] else None
        self.directions["sw"] = sw if sw[0] else None
        self.directions["nw"] = nw if nw[0] else None
        self.directions["u"] = u if u[0] else None
        self.directions["d"] = d if d[0] else None
        self.light = light

        if Game.DEBUG:
            Game.log("Room initialized. Name: {name}.".format(name=self.name))


    def __str__(self):

        """Overloads the default string method.
        Returns:
            str: The room's name"""

        return self.name

    
    def __repr__(self):

        """Overloads the default representation method.
        Returns:
            str: The identifier of the room for internal use"""

        return str(self).lower()

    
    def __eq__(self, other):

        """Overloads the default comparison method.
        Args:
            other: Another object
        Returns:
            bool: Are the representations equal?"""

        return self.__repr__() == other.__repr__()


    def snap(self):

        """Converts strings to object references when possible. Should be called on all entities at session start."""

        for key in self.directions:
            new_room = Game.object_from_str(self.directions[key][0]) if self.directions[key] and type(self.directions[key][0]) == str else None
            if new_room:
                new_door = Game.object_from_str(self.directions[key][1]) if self.directions[key][1] and type(self.directions[key][1]) == str else None
                self.directions[key] = (new_room, new_door)


    def contents(self):

        """Identifies entities which consider this room their container.
        Returns:
            tuple, Entity: All entities which this entity contains"""

        ans = ()

        for item in Game.entities:
            if item.location == self:
                ans = ans + (item,)

        return ans


    def contents_size(self):

        """Sums the size attributes of each entity which considers this room its container.
        Returns:
            int: The size of this entity's contents"""

        ans = 0
        for item in self.contents():
            ans += item.size

        return ans


    def per_turn(self):

        """Should be called every turn on every room. May be overloaded for custom behavior."""

        pass


    def examine(self):

        """Provides details about this room.
        Returns:
            str: A room description"""

        return self.description


    def move(self, entity, direction):

        """Moves something in this room out through one of the exits if possible. Rarely call this directly, as it is wrapped by Entity.move.
        Args:
            entity (Entity): The thing trying to exit
            direction (str): n, e, s, w, ne, se, sw, nw, u, or d
        Returns:
            str or Room: Failure message or destination Room"""

        direction_data = self.directions[direction]
        if not direction_data:
            return "You can't go that way."
        elif direction_data[1] and not direction_data[1].open:
            return "Your path is blocked by the {door_name}".format(door_name=str(direction_data[1]))
        else:
            return direction_data[0]
            