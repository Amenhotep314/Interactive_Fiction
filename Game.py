import os
import pickle
from tkinter import filedialog


DEBUG = False
# NOTE: Reference the current game state as Game.game, or use from Game import game. Do not use
# Game.Game, which points to the class and not the instance. This global is reassigned by main and
# load.
game = None


class Game:

    """A class to represent the state of the game."""

    def __init__(self):

        self.turn = 1
        self.score = 0
        self.player = player
        self.entities = entities
        self.rooms = rooms
        #self.score_events = get_score_events()




    def snap(self):

        for room in self.rooms: room.snap()
        for entity in self.entities: entity.snap()
        player.snap()


    def prioritize_entities(self):

        """Sorts the entities based on the current situation, prioritizing items in the inventory
        and current room."""

        ans = []
        for entity in self.entities:
            if entity.location == self.player:
                ans.append(entity)
                self.entities.remove(entity)
        for entity in self.entities:
            if entity.location == self.player.location:
                ans.append(entity)
                self.entities.remove(entity)
        for entity in self.entities:
            ans.append(entity)
            self.entities.remove(entity)

        self.entities = ans


    def object_from_str(self, name, inc_entities=True, inc_rooms=False, inc_player=True, is_snap=False):

        """Tries to find the object to which a given string refers.
        Args:
            name (str): The name of the target object
            inc_entities (bool): Should the function search entities? (default is True)
            inc_rooms (bool): Should the function search rooms? (default is False)
            inc_player (bool): Should the function check the player? (default is True)
            is_snap (bool): Is this function being called by a snap() function? If so, don't bother with prioritize_entities() (default is False)
        Returns:
            Entity or Room or None: The object most likely refered to by the given string, or None if this fails"""

        name = name.lower()
        if not is_snap:
            self.prioritize_entities()

        if inc_entities:
            for entity in self.entities:
                if entity.names[0].lower() == name:
                    return entity
            for entity in self.entities:
                for i in range(1, len(entity.names)):
                    if entity.names[i].lower() == name:
                        return entity

        if inc_rooms:
            for room in self.rooms:
                if room.id == name:
                    return room
            for room in self.rooms:
                if room.name == name:
                    return room

        if inc_player:
            for player_name in self.player.names:
                if player_name.lower() == name:
                    return self.player

        return None


    def turn_handler(self, increment=0):

        """Changes and/or accesses the number of the current turn.
        Args:
            increment (int): The amount by which to change the turn (default is 0)
        Returns:
            int: The current turn"""

        self.turn += increment
        return self.turn


    def score_handler(self):

        """Checks for changes in score.
        Returns:
            int: The current score"""

        for event in self.score_events:
            if getattr(event[0], event[1]) == event[2]:
                self.score += event[3]
                self.score_events.remove(event)

        return self.score


    def do_turn(self):

        """Runs all background tasks for a turn."""

        #self.score_handler()
        if self.player.strength <=0: self.player.die()
        self.player.per_turn()
        for entity in self.entities: entity.per_turn()
        for room in self.rooms: room.per_turn()
        self.turn_handler(1)


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
            other_names ([str]): Additional ways the entity may be referenced
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
            unlocks ([str]): The names of all entities which this entity can unlock. Converted from str to object after initialization by snap (default is None)"""

        self.names = name
        [self.names].append(other_names)
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

        if DEBUG:
            log("Entity initialized. Name: {name}.\tLocation: {location}".format(name=str(self), location=str(self.location)))


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
            self.location = game.object_from_str(self.location, inc_rooms=True, inc_player=True, is_snap=True)
        if self.unlocks and type(self.unlocks[0]) == str:
            self.unlocks = (game.object_from_str(entity, is_snap=True) for entity in self.unlocks)


    def contents(self):

        """Identifies entities which consider this entity their container.
        Returns:
            [Entity]: All entities which this entity contains"""

        ans = []

        for item in game.entities:
            if item.location == self:
                ans.append(item)

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

        if DEBUG:
            log("Game state update. Location of {name} is {location}".format(name=str(self), location=self.location))


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
        elif game.player.contents_size() + self.size <= game.player.capacity:
            self.location = game.player
            return "Taken."
        else:
            return "Your load is too heavy to pick up the {name}.".format(name=str(self))


    def drop(self):

        """Puts the entity in the player's current location.
        Returns:
            str: Success message"""

        self.location = game.player.location
        return "Dropped."


    def put(self, other):

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
            return "There is not enough room in the {other_name} for the {name}.".format(other_name=str(other), name=str(self))


    def open(self):

        """Opens the entity if possible.
        Returns:
            str: Success/failure message"""

        if self.open:
            return "The {name} is already open.".format(name=str(self))
        elif not self.openable:
            return "You cannot open the {name}.".format(name=str(self))
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
            return "You lock the {name}.".format(name=str(self))
        else:
            return "You cannot lock the {name} with the {other_name}.".format(name=str(self), other_name=str(locker))


    def turn_on(self):

        """Turns on the entity if possible.
        Returns:
            str: Successs/failure message"""

        if self.on:
            return "The {name} is already on.".format(name=str(self))
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
                return "You damage the {name}.".format(name=str(self))


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
            direction (str): n, e, s, w, ne, se, sw, nw, u, d, in, or out
        Returns:
            str: Failure message or empty string for success"""

        assert direction in ["n", "e", "s", "w", "ne", "se", "sw", "nw", "u", "d", "in", "out"]

        ans = self.location.move(self, direction)
        if type(ans) == str:
            return ans
        self.location = ans

        return ""


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

        Entity.__init__(self,
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



class Room:

    """A superclass implemented by all rooms in the game."""

    def __init__(self,
        name, description, id="",
        n=(None,None), e=(None,None), s=(None,None), w=(None,None), ne=(None,None), se=(None,None), sw=(None,None), nw=(None,None), u=(None,None), d=(None,None),
        light=True):

        """
        Args:
            name (str): The room's title
            description (str): A description of the room
            id (str): The room's unique identifier, if there will be multiple rooms of the same name. Otherwise set to self.name.lower() at initialization (default is "")
            n (tuple(str, str)): The name of the room to the north of this one and the name of the door in between. Converted to objects after initialization by snap (default is (None, None))
            e (tuple(str, str)): The name of the room to the east of this one and the name of the door in between. Converted to objects after initialization by snap (default is (None, None))
            s (tuple(str, str)): The name of the room to the south of this one and the name of the door in between. Converted to objects after initialization by snap (default is (None, None))
            w (tuple(str, str)): The name of the room to the west of this one and the name of the door in between. Converted to objects after initialization by snap (default is (None, None))
            ne (tuple(str, str)): The name of the room to the northeast of this one and the name of the door in between. Converted to objects after initialization by snap (default is (None, None))
            se (tuple(str, str)): The name of the room to the southeast of this one and the name of the door in between. Converted to objects after initialization by snap (default is (None, None))
            sw (tuple(str, str)): The name of the room to the southwest of this one and the name of the door in between. Converted to objects after initialization by snap (default is (None, None))
            nw (tuple(str, str)): The name of the room to the northwest of this one and the name of the door in between. Converted to objects after initialization by snap (default is (None, None))
            u (tuple(str, str)): The name of the room above this one and the name of the door in between. Converted to objects after initialization by snap (default is (None, None))
            d (tuple(str, str)): The name of the room below this one and the name of the door in between. Converted to objects after initialization by snap (default is (None, None))
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

        self.id = name.lower() if not id else id

        if DEBUG:
            log("Room initialized. Name: {name}.".format(name=self.name))


    def __str__(self):

        """Overloads the default string method.
        Returns:
            str: The room's name"""

        return self.name


    def __repr__(self):

        """Overloads the default representation method.
        Returns:
            str: The identifier of the room for internal use"""

        return self.id


    def __eq__(self, other):

        """Overloads the default comparison method.
        Args:
            other: Another object
        Returns:
            bool: Are the representations equal?"""

        return self.__repr__() == other.__repr__()


    def __hash__(self):

        """Overloads the default hash method.
        Returns:
            str: The hash code that represents the room"""

        return hash(self.__repr__())


    def snap(self):

        """Converts strings to object references when possible. Should be called on all entities at session start."""

        new_room = None
        new_door = None

        for key in self.directions:
            if self.directions[key] and type(self.directions[key][0]) == str:
                new_room = game.object_from_str(self.directions[key][0], inc_entities=False, inc_rooms=True, is_snap=True)
            if new_room:
                if self.directions[key][1] and type(self.directions[key][1]) == str:
                    new_door = game.object_from_str(self.directions[key][1], is_snap=True)
                self.directions[key] = (new_room, new_door)


    def contents(self):

        """Identifies entities which consider this room their container.
        Returns:
            tuple, Entity: All entities which this entity contains"""

        ans = ()

        for item in game.entities:
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


def main():

    """Executed from the command line and calls all other parts of the game."""

    global game
    game = Game()

    game.snap()

    if DEBUG:
        log("Session started.")

    while True:
        print("Turn: " + str(game.turn) + "\tScore" + str(game.score))
        user_input = input(">>> ")
        parse(user_input)
        game.do_turn()


def save():

    """Serializes the current game state to a file."""
    dir = os.getcwd()
    with filedialog.asksaveasfile(mode='wb', initialdir=dir, filetypes=[("Pickle files", "*.p")], defaultextension=".p") as file:
        pickle.dump(game, file)


def load():

    """Sets the current game state to the contents of a file."""
    dir = os.getcwd()
    with filedialog.askopenfile(mode='rb', initialdir=dir, filetypes=[("Pickle files", "*.p")]) as file:
        new_game = pickle.load(file)

    global game
    game = new_game


def log(event):

    """Writes the given event to log.txt, along with the date, time, and turn.
    Args:
        event (str): The text to be logged"""

    from datetime import datetime
    time = datetime.now()
    time = time.strftime("%Y/%m/%d - %H:%M:%S - Turn " + str(game.turn_handler()))

    with open("log.txt", "a") as log:
        log.write(time + ": " + str(event) + "\n")


def parse(user_input):

    """Parses raw user input and calls proper method in entity or room.
    Args:
        userInput (str): the raw user input"""

    user_input_arts = clean_input(user_input)
    user_input = remove_arcticles(user_input_arts)
    unknown = check_unknown_words(user_input)

    if unknown:
        print("I don't know the word: \"" + unknown + ".\"")

    else:
        verb, og_verb = find_verb(user_input)

        if verb:
            needs_direct = requires_object(verb, "direct")

            if needs_direct:
                direct = find_direct_object(user_input, og_verb)

                if direct:
                    if len(direct) > 1 and not supports_multiple_direct_objects(verb):
                        print("You can't use more than one direct object with the verb: \"" + og_verb + ".\"")

                    else:
                        needs_indirect = requires_object(verb, "indirect")

                        if needs_indirect:
                            indirect = find_indirect_object(user_input, og_verb, direct[0])

                            if len(indirect) > 1:
                                print("You can't use multiple indirect objects with the verb: \"" + og_verb + ".\"")

                            elif len(indirect) == 1:
                                execute(verb, direct, indirect)

                        else:
                            execute(verb, direct)

            else:
                execute(verb, ["player"])


def supports_multiple_direct_objects(verb):

    supports_list = ("take", "drop")

    if verb in supports_list:

        return True

    else:

        return False


def requires_object(verb, object_type):

    """Determines if a certain verb needs a direct or indirect object
    Args:
        verb (str): the verb in question
        objectType (str): either 'direct' or 'indirect'"""

    requires_object_list = {
        "n": (False, False),
        "s": (False, False),
        "e": (False, False),
        "w": (False, False),
        "nw": (False, False),
        "ne": (False, False),
        "sw": (False, False),
        "se": (False, False),
        "u": (False, False),
        "d": (False, False),
        "look": (False, False),
        "inventory": (False, False),
        "take": (True, False),
        "throw": (True, False),
        "open": (True, False),
        "close": (True, False),
        "read": (True, False),
        "drop": (True, False),
        "put": (True, True),
        "lock": (True, True),
        "unlock": (True, True),
        "say": (False, False),
        "turn on": (True, False),
        "turn off": (True, False),
        "hit": (True, True),
        "examine": (True, False),
        "eat": (True, False),
        "drink": (True, False)
    }

    requires = False

    if object_type == "direct":

        requires = requires_object_list[verb][0]

    elif object_type == "indirect":

        requires = requires_object_list[verb][1]

    return requires


def find_verb(text):

    """Finds the verb or verbs in a string of text.
    Args:
        text (str): the text in which to find the verb
    Returns:
        str: verb if found, empty string if not"""

    verbs = [           #Note that down below, all synonyms are switched to the first verb in the tuple.
        ["move", "go"], #This means that the first verb listed is the one that will be used.
        ["n", "north"],
        ["s", "south"],
        ["e", "east"],
        ["w", "west"],
        ["nw", "northwest"],
        ["ne", "northeast"],
        ["sw", "southwest"],
        ["se", "southeast"],
        ["u", "up"],
        ["d", "down"],
        ["look", "location", "l"],
        ["inventory"],                              #This doesn't include i because it would cause problems with the user typing I to mean themselves. There is a special case down below for if the user types only a single "i".
        ["take", "get", "pick up", "grab", "steal", "hoist"],
        ["throw", "chuck", "hurl", "pitch"],
        ["open"],
        ["close"],
        ["read"],
        ["drop", "put down"],
        ["put", "put in"],
        ["lock"],
        ["unlock"],
        ["say", "speak", "talk"],
        ["turn on", "activate", "switch on"],
        ["turn off", "deactivate", "swith off"],
        ["hit", "kill", "attack", "strike", "smite", "slash", "destroy", "chop", "slice", "punch", "slap", "kick", "assault", "smack", "break"],
        ["examine", "search", "inspect"],
        ["eat", "consume", "devour", "gobble", "munch", "gnaw on"],
        ["drink", "guzzle", "sip", "swallow", "swig", "slurp"]
    ]

    verb = ""
    og_verb = ""
    verb_count = 0
    word_list = text.split(" ")

    if text == "i":
        verb = "inventory"
        verb_count += 1

    else:

        for i in range(len(verbs)):

            for j in range(len(verbs[i])):

                for a in range(len(word_list)):

                    length = len(word_list)

                    if word_list[a] == verbs[i][j]:

                        if (word_list[a] == "down" or word_list[a] == "up") and a != 0:

                            if word_list[a-1] != "pick" and word_list[a-1] != "put":

                                verb = verbs[i][j]
                                verb_count += 1

                        elif word_list[a] == "put":

                            if a+1 != len(word_list):

                                if word_list[a+1] != "down":

                                    verb = verbs[i][j]
                                    verb_count += 1

                            else:

                                verb = verbs[i][j]
                                verb_count += 1

                        else:

                            verb = verbs[i][j]
                            verb_count += 1

                    if a+1 != len(word_list):

                        if word_list[a] + " " + word_list[a+1] == verbs[i][j]:

                            verb = word_list[a] + " " + word_list[a+1]
                            verb_count += 1

    directions = (
            "n",
            "s",
            "e",
            "w",
            "north",
            "south",
            "east",
            "west",
            "u",
            "d",
            "up",
            "down",
            "nw",
            "ne",
            "sw",
            "se",
            "northwest",
            "northeast",
            "southwest",
            "southeast"
        )

    for i in range(len(directions)):

        if verb == directions[i] and verb_count == 2:

            verb_count = 1

    if verb == "move" or verb == "go":

        response = input("Which way do you want to move?\n>>> ")
        response = response.lower()
        response = response.split()

        direction = False
        direction_index = 0

        for i in range(len(directions)):

            for j in range(len(response)):

                if response[j] == directions[i]:

                    direction = True
                    direction_index = i

        if direction == True:

            verb = directions[direction_index]

        else:
            print("That's not a direction you can go!")
            return ""

    if verb_count == 1:

        for i in range(len(verbs)):

            for j in range(len(verbs[i])):

                if verb == verbs[i][j]:

                    verb = verbs[i][0]
                    og_verb = verbs[i][j]

        return verb, og_verb

    elif verb_count == 0:

        print("There's no verb in that sentence!")
        return "", ""

    elif verb_count > 1:

        print("I don't understand that sentence!")
        return "", ""


def execute(verb, direct, indirect="", str_indirect=False):

    direct_object = [game.object_from_str(item) for item in direct]

    if indirect and not str_indirect:

        indirect_object = game.object_from_str(indirect)

    for item in direct_object:
        method = getattr(item, verb)

        if indirect:
            output = method(indirect_object)

        else:
            output = method()

        print(output)


def check_unknown_words(text):

    word_list = text.split(" ")
    known_list = [False for x in word_list]
    unknown_word = ""

    white_list = ("and", "to", "all", "use", "using", "with", "i")

    verbs = [
        "move", "go",
        "n", "north",
        "s", "south",
        "e", "east",
        "w", "west",
        "nw", "northwest",
        "ne", "northeast",
        "sw", "southwest",
        "se", "southeast",
        "u", "up",
        "d", "down",
        "look", "location", "l",
        "inventory",
        "take", "get", "pick up", "grab", "steal", "hoist",
        "throw", "chuck", "hurl", "pitch",
        "open",
        "close",
        "read",
        "drop", "put down",
        "put", "put in",
        "lock",
        "unlock",
        "say", "speak", "talk",
        "turn on", "activate", "switch on",
        "turn off", "deactivate", "swith off",
        "hit", "kill", "attack", "strike", "smite", "slash", "destroy", "chop", "slice", "punch", "slap", "kick", "assault", "smack", "break",
        "examine", "search", "inspect",
        "eat", "consume", "devour", "gobble", "munch", "gnaw on",
        "drink", "guzzle", "sip", "swallow", "swig", "slurp"
    ]

    for i in range(len(word_list)-1):

        if word_list[i] + " " + word_list[i+1] in verbs or game.object_from_str(word_list[i] + " " + word_list[i+1]) or word_list[i] + " " + word_list[i+1] in white_list:

            known_list[i] = True
            known_list[i+1] = True

    for i in range(len(word_list)):

        if word_list[i] in verbs or game.object_from_str(word_list[i]) or word_list[i] in white_list:

            known_list[i] = True

    for i in range(len(word_list)):

        if not known_list[i]:

            unknown_word = word_list[i]
            break

    return unknown_word


def find_indirect_object(text, verb, direct):

    word_list = text.split()
    verb_words = verb.split()

    if len(verb_words) > 1:

        for i in range(len(word_list)):

            if word_list[i] == verb_words[0]:

                word_list[i:i+(len(verb_words)-1)] = verb
                break


    indirect_object = []

    verb_index = word_list.index(verb)

    indirect_qualifyers = ("use", "using", "with")
    qualifyer_index = None
    qualifyer_count = 0

    for i in range(len(word_list)):

        for qualifyer in indirect_qualifyers:

            if word_list[i] == qualifyer:

                qualifyer_index = i
                qualifyer_count += 1

    if qualifyer_count > 1:

        print("I don't understand that sentence!")

    if qualifyer_count <= 1:

        if qualifyer_count == 1:

            if qualifyer_index < verb_index:

                word_list = word_list[:verb_index]

            elif qualifyer_index > verb_index:

                word_list = word_list[qualifyer_index:]

            counted_list = [False for x in word_list]

            for i in range(len(word_list)-1):

                if game.object_from_str(word_list[i] + " " + word_list[i+1]) and not counted_list[i] and not counted_list[i+1]:

                    indirect_object.append(word_list[i] + " " + word_list[i+1])
                    counted_list[i] = True
                    counted_list[i+1] = True

            for i in range(len(word_list)):

                if game.object_from_str(word_list[i]) and not counted_list[i]:

                    indirect_object.append(word_list[i])
                    counted_list[i] = True

        if not indirect_object:

            user_input = input("What do you want to " + verb + " the " + direct + " with?\n>>> ")
            user_input = clean_input(user_input)
            user_input = remove_arcticles(user_input)
            unknown = check_unknown_words(user_input)

            if unknown:

                print("I don't know the word: \"" + unknown +".\"")

            else:

                input_words = user_input.split()
                counted_list = [False for x in input_words]

                for i in range(len(input_words)-1):

                    if game.object_from_str(input_words[i] + " " + input_words[i+1]) and not counted_list[i] and not counted_list[i+1]:

                        indirect_object.append(input_words[i] + " " + input_words[i+1])
                        counted_list[i] = True
                        counted_list[i+1] = True

                for i in range(len(input_words)):

                    if game.object_from_str(input_words[i]) and not counted_list[i]:

                        indirect_object.append(input_words[i])
                        counted_list[i] = True

                    elif input_words[i] == "all":

                        indirect_object.append(input_words[i])
                        counted_list[i] = True

                if not indirect_object:

                    print("What?")

    return indirect_object


def find_direct_object(text, verb):

    word_list = text.split()
    verb_words = verb.split()

    if len(verb_words) > 1:

        for i in range(len(word_list)):

            if word_list[i] == verb_words[0]:

                word_list[i] = verb
                del word_list[i+1]
                break


    direct_object = []

    verb_index = word_list.index(verb)

    indirect_qualifyers = ("use", "using", "with")
    qualifyer_index = None
    qualifyer_count = 0

    for i in range(len(word_list)):

        for qualifyer in indirect_qualifyers:

            if word_list[i] == qualifyer:

                qualifyer_index = i
                qualifyer_count += 1

    if qualifyer_count == 1:

        if qualifyer_index < verb_index:

            word_list = word_list[verb_index:]

        elif qualifyer_index > verb_index:

            word_list = word_list[:qualifyer_index]

    if qualifyer_count > 1:

        print("I don't understand that sentence!")

    else:

        verb_index = word_list.index(verb)
        del word_list[verb_index]

        counted_list = [False for x in word_list]

        for i in range(len(word_list)-1):

            if game.object_from_str(word_list[i] + " " + word_list[i+1]) and not counted_list[i] and not counted_list[i+1]:

                direct_object.append(word_list[i] + " " + word_list[i+1])
                counted_list[i] = True
                counted_list[i+1] = True

        for i in range(len(word_list)):

            if game.object_from_str(word_list[i]) and not counted_list[i]:

                direct_object.append(word_list[i])
                counted_list[i] = True

            elif word_list[i] in ("all", "everything",):

                direct_object.append("all")
                counted_list[i] = True

        if not direct_object:

            user_input = input("What do you want to " + verb + "?\n>>> ")
            user_input = clean_input(user_input)
            user_input = remove_arcticles(user_input)
            unknown = check_unknown_words(user_input)

            if unknown:

                print("I don't know the word: \"" + unknown +".\"")

            else:

                input_words = user_input.split()
                counted_list = [False for x in input_words]

                for i in range(len(input_words)-1):

                    if game.object_from_str(input_words[i] + " " + input_words[i+1]) and not counted_list[i] and not counted_list[i+1]:

                        direct_object.append(input_words[i] + " " + input_words[i+1])
                        counted_list[i] = True
                        counted_list[i+1] = True

                for i in range(len(input_words)):

                    if game.object_from_str(input_words[i]) and not counted_list[i]:

                        direct_object.append(input_words[i])
                        counted_list[i] = True

                    elif input_words[i] == "all":

                        direct_object.append(input_words[i])
                        counted_list[i] = True

                if not direct_object:

                    print("What?")

    return direct_object


def remove_arcticles(user_input):

    """Removes common articles from a string
    Args:
        userInput (str): string from which to remove the articles
    Returns:
        str: the string without the articles"""

    article_blacklist = ("a", "an", "the", "this", "that")

    word_list = user_input.split()

    for article in article_blacklist:

        if article in word_list:

            for i in range(word_list.count(article)):

                word_list.remove(article)

    return " ".join(word_list)


def clean_input(user_input):

    """Removes puctuation and caps from string
    Args:
        userInput (str): the string to have its punctuation removed
    Returns:
        str: string without puctuation or caps"""

    punc_blacklist = (".", ",", "<", ">", "?", "/", "\\", ";", ":", "'", "[", "]", "{", "}", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "_", "+", "=", "`", "~")

    for i in range(len(punc_blacklist)):

        user_input = user_input.replace(punc_blacklist[i], "")

    user_input = user_input.lower()

    return user_input


class Player(Character):

    def __init__(self,
        name="Player", other_names=["me", "myself", "I", "self"], description="You look a bit worse than you think you do.", location="mudroom",
        size=20, strength=20, capacity=10,
        hoistable=False, destroyable=True, open=False, openable=False, lightable=False, on=False,
        unlocks=[None]):

        Character.__init__(self,
            name, other_names, description, location,
            size=size, strength=strength, capacity=capacity,
            hoistable=hoistable, destroyable=destroyable, open=open, openable=openable, lightable=lightable, on=on,
            unlocks=[None])


    def say(self, text):

        """Handles this entity being spoken to.
        Args:
            text (str): The words said to the entity
        Returns:
            str: The entity's response or a failure message"""

        return "Talking to yourself is a sign of impending madness."


    def look(self):

        """Returns the description and contents of the location of the player.
        Returns:
            str: Description of the location and a list of its contents"""

        print(type(self.location))

        name = str(self.location)
        description = self.location.examine()
        room_contents = self.location.contents()

        description = name + "\n" + description

        if room_contents:
            description += "\nHere you see:\n" + "\n".join([str(content) for content in room_contents])

        return description


    def inventory(self):

        """Returns the contents of the player's inventory.
        Returns:
            str: Description of the inventory"""

        ans = "You are carrying:\n"
        contents = self.contents()

player = Player()

entities = [
    Entity("knife", ["nasty knife"], "This is a terrific knife!", "mudroom")
]

rooms = [
    Room("Mudroom", "This room is full of shoes.")
]

if __name__ == "__main__":

    main()