import os
import pickle
from tkinter import filedialog
from Parser import parse

import House as Source


DEBUG = True
# NOTE: Reference the current game state as Game.game, or use from Game import game. Do not use
# Game.Game, which points to the class and not the instance. This global is reassigned by main and
# load.
game = None


class Game:

    """A class to represent the state of the game."""

    def __init__(self):

        self.turn = 1
        self.score = 0
        self.player = Source.get_player()
        self.entities = Source.get_entities()
        self.rooms = Source.get_rooms()
        self.score_events = Source.get_score_events()

        for room in self.rooms: room.snap()
        for entity in self.entities: entity.snap()


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


    def object_from_str(self, name, inc_entities=True, inc_rooms=False, inc_player=False, is_snap=False):

        """Tries to find the object to which a given string refers.
        Args:
            name (str): The name of the target object
            inc_entities (bool): Should the function search entities? (default is True)
            inc_rooms (bool): Should the function search rooms? (default is False)
            inc_player (bool): Should the function check the player? (default is False)
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

        self.score_handler()
        if self.player.strength <=0: self.player.die()
        self.player.per_turn()
        for entity in self.entities: entity.per_turn()
        for room in self.rooms: room.per_turn()
        self.turn_handler(1)


def main():

    """Executed from the command line and calls all other parts of the game."""

    global game
    game = Game()

    if DEBUG:
        log("Session started.")

    while True:
        print("Turn: " + str(game.turn) + "\tScore" + str(game.score))
        print(game.player.look())
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


if __name__ == "__main__":

    main()