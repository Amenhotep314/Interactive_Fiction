import House


DEBUG = True

class Game:

    """A class to represent the state of the game."""

    def __init__(self):
        
        self.turn = 0
        self.score = 0
        self.player = House.get_player()
        self.entities = House.get_entities()
        self.rooms = House.get_rooms()
        self.score_events = House.get_score_events()

        for key in self.rooms:
            self.rooms[key].snap()
        for key in self.entities:
            self.entities[key].snap()


    def prioritize_entities(self):

        """Sorts the entities based on the current situation, prioritizing items in the inventory
        and current room."""

        ans = ()
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


    def object_from_str(self, name, require_entity=False):

        """Tries to find the object to which a given string refers.
        Args:
            name (str): The name of the target object
            require_entity (bool): Should the function search exclusively for an Entity, not a Room? (default is False)
        Returns:
            Entity or Room or None: The object most likely refered to by the given string, or None if this fails"""

        name = name.lower()

        for key in self.entities:
            if name == key.lower():
                return self.entities[key]
        for key in self.entities:
            if name in (other_name.lower() for other_name in self.entities[key].names):
                return self.entities[key]   
        if name in (other_name.lower() for other_name in self.player.names):
            return self.player
        
        if require_entity:
            return None

        for key in self.rooms:
            if name == self.rooms[key].lower():
                return self.rooms[key]
        
        return None   
        


def main():

    """Executed from the command line and calls all other parts of the game."""

    game = Game()
    
    if DEBUG:
        log("Session started.")
    
    # Import all entities and rooms
    # Snap all entities and rooms

    # Start tests
    from Entity import Entity
    from Room import Room

    west_of_house = Room(
        "West of House",
        "You are standing in an open field west of a white house, with a boarded front door.",
    )

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
    time = time.strftime("%Y/%m/%d - %H:%M:%S - Turn " + str(turn))

    with open("log.txt", "a") as log:
        log.write(time + ": " + str(event) + "\n")


if __name__ == "__main__":
    
    main()