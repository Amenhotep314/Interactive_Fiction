DEBUG = True
turn = 0

def main():

    """Executed from the command line and calls all other parts of the game."""
    
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

    mailbox = Entity(
        "Small Mailbox",
        ("mailbox", "box",),
        "",
        west_of_house,
        capacity=1,
        hoistable=False,
        openable=True
    )

    leaflet = Entity(
        "Leaflet",
        (),
        "The leaflet says, \"WELCOME TO ZORK!\n\nZORK is a game of adventure, danger, and low cunning. In it you will explore some of the most amazing territory ever seen by mortals. No computer should be without one!\"",
        mailbox,
    )

    # End tests

    while True:
        turn_handler(1)
        # Background tasks
        # Display update
        # User input
        # Parse
        # Turn tasks
        break


def turn_handler(increment=0):
    
    """Changes and/or accesses the number of the current turn.
    Args:
        increment (int): The amount by which to change the turn (default is 0)
    Returns:
        int: The current turn"""
    
    global turn
    turn += increment
    return turn


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