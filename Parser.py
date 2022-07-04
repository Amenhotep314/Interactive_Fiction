import Game

def parse(userInput):

    """This is the main function for the parser.
    Pass the input from the user in as a string, and it will call the requisite method in whatever entity.
    It does not return anything, but it does write to the log and print stuff."""

    cleanText = cleanInput(userInput)

    if Game.DEBUG:
    verbs = (
        ("north", "n"),
        ("south", "s"),
        ("east", "e"),
        ("west", "w"),
        ("northwest", "nw"),
        ("northeast", "ne"),
        ("southwest", "sw"),
        ("southeast", "se"),
        ("up", "u"),
        ("down", "d"),
        ("look", "location", "l"),
        ("inventory", "i"),
        ("take", "get", "pick up", "grab", "steal"),
        ("throw", "chuck", "hurl", "pitch"),
        ("open"),
        ("read"),
        ("drop"),
        ("put"),
        ("turn on", "activate", "switch on"),
        ("turn off", "deactivate", "swith off"),
        ("hit", "kill", "attack", "strike", "smite", "slash", "destroy", "chop", "slice"),
        ("examine", "search", "inspect"),
        ("eat", "consume", "devour", "gobble", "munch", "gnaw on"),
        ("drink", "guzzle", "sip", "swallow", "swig")
    )

def removeArticles(userInput):

    articleBlacklist = ("a", "an", "the", "this", "that")

    for i in range(len(articleBlacklist)):

        userInput = userInput.replace(articleBlacklist[i], "")
    
    return userInput


def cleanInput(userInput):
    
    puncBlacklist = (".", ",", "<", ">", "?", "/", "\\", ";", ":", "'", "[", "]", "{", "}", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "_", "+", "=", "`", "~")

    for i in range(len(puncBlacklist)):

        userInput = userInput.replace(puncBlacklist[i], "")

    userInput = userInput.lower()

    return userInput


def move (direction):
    Game.game.player.move(direction)