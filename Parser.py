import Game

def parse(userInput):

    """This is the main function for the parser.
    Pass the input from the user in as a string, and it will call the requisite method in whatever entity.
    It does not return anything, but it does write to the log and print stuff."""

    cleanText = cleanInput(userInput)

    if Game.DEBUG:
        Game.log("Parser received phrase: " + userInput + ", and cleaned it to: " + cleanText)

    
def findVerb(text):

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
        ("hit", "kill", "attack", "strike", "smite", "slash", "destroy", "chop", "slice"),
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

def move(direction):
    Game.game.player.move(direction)