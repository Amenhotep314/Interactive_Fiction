from Entity import Entity
from Character import Character
from Room import Room

# CHARACTER DEFINITIONS
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

        name = str(self.location)
        description = self.location.examine()
        room_contents = self.location.contents()

        description = name + "\n" + description

        if room_contents:
            description += "\nHere you see:\n" + "\n".join(room_contents)

        return description


    def inventory(self):

        """Returns the contents of the player's inventory.
        Returns:
            str: Description of the inventory"""

        ans = "You are carrying:\n"
        contents = self.contents()


