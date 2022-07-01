DEBUG = True


def main():

    """Executed from the command line and calls all other parts of the game."""
    
    if DEBUG:
        log("NEW SESSION STARTED.")


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
        log.write(time + ": " + event + "\n")


if __name__ == "__main__":
    
    turn = 0
    main()