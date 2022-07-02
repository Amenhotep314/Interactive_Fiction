DEBUG = True
turn = 0

def main():

    """Executed from the command line and calls all other parts of the game."""
    
    if DEBUG:
        log("Session started.")
    
    # Import all entities and rooms
    # Snap all entities and rooms

    from Entity import Entity
    test = Entity(
        "Brass Lantern",
        ("lantern", "lamp", "light"),
        "The brass lantern is highly hoistable.",
        "Attic"
    )

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