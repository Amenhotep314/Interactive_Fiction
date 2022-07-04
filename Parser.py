import Game

def parse(userInput):

    """Parses raw user input and calls proper method in entity or room.
    Args:
        userInput (str): the raw user input"""

    cleanText = cleanInput(userInput)

    if Game.DEBUG:
        Game.log("Parser received phrase: " + userInput + ", and cleaned it to: " + cleanText)

def requiresObject(verb, objectType):
    
    requisiteObjectList = {
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
        "turn on": (True, False),
        "turn off": (True, False),
        "hit": (True, True),
        "examine": (True, False),
        "eat": (True, False),
        "drink": (True, False)
    }

    requires = False

    if objectType == "direct":

        requires = requisiteObjectList[verb][0]

    elif objectType == "indirect":

        requires = requisiteObjectList[verb][1]
    
    return requires

    
def findVerb(text):

    """Finds the verb or verbs in a string of text.
    Args:
        text (str): the text in which to find the verb
    Returns:
        str: verb if found, empty string if not"""

    verbs = (           #Note that down below, all synonyms are switched to the first verb in the tuple.
        ("n", "north"), #This means that the first verb listed is the one that will be used.
        ("s", "south"),
        ("e", "east"),
        ("w", "west"),
        ("nw", "northwest"),
        ("ne", "northeast"),
        ("sw", "southwest"),
        ("se", "southeast"),
        ("u", "up"),
        ("d", "down"),
        ("look", "location", "l"),
        ("inventory"),                              #This doesn't include i because it would cause problems with the user typing I to mean themselves. There is a special case down below for if the user types only a single "i".
        ("take", "get", "pick up", "grab", "steal", "hoist",),
        ("throw", "chuck", "hurl", "pitch"),
        ("open"),
        ("close"),
        ("read"),
        ("drop"),
        ("put"),
        ("turn on", "activate", "switch on"),
        ("turn off", "deactivate", "swith off"),
        ("hit", "kill", "attack", "strike", "smite", "slash", "destroy", "chop", "slice", "punch", "slap", "kick", "assault"),
        ("examine", "search", "inspect"),
        ("eat", "consume", "devour", "gobble", "munch", "gnaw on"),
        ("drink", "guzzle", "sip", "swallow", "swig", "slurp")
    )

    verb = ""
    verbCount = 0
    wordList = text.split(" ")

    if text == "i":
        verb = "inventory"
    
    else:

        for i in range(len(verbs)):

            for j in range(len(verbs[i])):

                for a in range(len(wordList)):

                    length = len(wordList)

                    if wordList[a] == verbs[i][j]:

                        verb = verbs[i][j]
                        verbCount += 1
                    
                    if a+1 != len(wordList):

                        if wordList[a] + " " + wordList[a+1] == verbs[i][j]:

                            verb = wordList[a] + " " + wordList[a+1]
                            verbCount += 1
    
    if verbCount == 1:

        for i in range(len(verbs)):

            for j in range(len(verbs[i])):

                if verb == verbs[i][j]:

                    verb = verbs[i][0]
        
        return verb

    elif verbCount == 0:

        print("There's no verb in that sentence!")
        return ""
    
    elif verbCount > 1:

        print("I don't understand that sentence!")
        return ""
        

def removeArticles(userInput):

    """Removes common articles from a string
    Args:
        userInput (str): string from which to remove the articles
    Returns:
        str: the string without the articles"""

    articleBlacklist = ("a", "an", "the", "this", "that")

    for i in range(len(articleBlacklist)):

        userInput = userInput.replace(articleBlacklist[i], "")
    
    return userInput

def cleanInput(userInput):

    """Removes puctuation and caps from string
    Args:
        userInput (str): the string to have its punctuation removed
    Returns:
        str: string without puctuation or caps"""
    
    puncBlacklist = (".", ",", "<", ">", "?", "/", "\\", ";", ":", "'", "[", "]", "{", "}", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "_", "+", "=", "`", "~")

    for i in range(len(puncBlacklist)):

        userInput = userInput.replace(puncBlacklist[i], "")

    userInput = userInput.lower()

    return userInput

def move(direction):
    Game.game.player.move(direction)