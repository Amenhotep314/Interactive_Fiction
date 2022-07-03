import Game

def parse(userInput):

    """This is the main function for the parser.
    Pass the input from the user in as a string, and it will call the requisite method in whatever entity.
    It does not return anything, but it does write to the log."""

    if Game.DEBUG:
        Game.log("Parser received phrase: " + userInput)


def cleanInput(userInput):
    
    puncBlacklist = [".", ",", "<", ">", "?", "/", "\\", ";", ":", "'", "[", "]", "{", "}", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "_", "+", "=", "`", "~"]

    for i in range(len(puncBlacklist)):

        userInput = userInput.replace(puncBlacklist[i], "")

    userInput = userInput.lower()

    return userInput


def move (direction):
    Game.game.player.move(direction)