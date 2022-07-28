import Game
import Entity
import Room

def parse(user_input):

    """Parses raw user input and calls proper method in entity or room.
    Args:
        userInput (str): the raw user input"""

    user_input_arts = clean_input(user_input)
    user_input = remove_arcticles(user_input_arts)
    
    verb = find_verb(user_input)

    print(verb)

    if verb:

        needs_direct = requires_object(verb, "direct")

def requires_object(verb, object_type):

    """Determines if a certain verb needs a direct or indirect object
    Args:
        verb (str): the verb in question
        objectType (str): either 'direct' or 'indirect'"""
    
    requires_object_list = {
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
        "lock": (True, True),
        "unlock": (True, True),
        "say": (False, False),
        "turn on": (True, False),
        "turn off": (True, False),
        "hit": (True, True),
        "examine": (True, False),
        "eat": (True, False),
        "drink": (True, False)
    }

    requires = False

    if object_type == "direct":

        requires = requires_object_list[verb][0]

    elif object_type == "indirect":

        requires = requires_object_list[verb][1]
    
    return requires

    
def find_verb(text):

    """Finds the verb or verbs in a string of text.
    Args:
        text (str): the text in which to find the verb
    Returns:
        str: verb if found, empty string if not"""

    verbs = [           #Note that down below, all synonyms are switched to the first verb in the tuple.
        ["move", "go"], #This means that the first verb listed is the one that will be used.
        ["n", "north"],
        ["s", "south"],
        ["e", "east"],
        ["w", "west"],
        ["nw", "northwest"],
        ["ne", "northeast"],
        ["sw", "southwest"],
        ["se", "southeast"],
        ["u", "up"],
        ["d", "down"],
        ["look", "location", "l"],
        ["inventory"],                              #This doesn't include i because it would cause problems with the user typing I to mean themselves. There is a special case down below for if the user types only a single "i".
        ["take", "get", "pick up", "grab", "steal", "hoist"],
        ["throw", "chuck", "hurl", "pitch"],
        ["open"],
        ["close"],
        ["read"],
        ["drop", "put down"],
        ["put", "put in"],
        ["lock"],
        ["unlock"],
        ["say", "speak", "talk"],
        ["turn on", "activate", "switch on"],
        ["turn off", "deactivate", "swith off"],
        ["hit", "kill", "attack", "strike", "smite", "slash", "destroy", "chop", "slice", "punch", "slap", "kick", "assault", "smack", "break"],
        ["examine", "search", "inspect"],
        ["eat", "consume", "devour", "gobble", "munch", "gnaw on"],
        ["drink", "guzzle", "sip", "swallow", "swig", "slurp"]
    ]

    verb = ""
    verb_count = 0
    word_list = text.split(" ")

    if text == "i":
        verb = "inventory"
        verb_count += 1
    
    else:

        for i in range(len(verbs)):

            for j in range(len(verbs[i])):

                for a in range(len(word_list)):

                    length = len(word_list)

                    if word_list[a] == verbs[i][j]:

                        if (word_list[a] == "down" or word_list[a] == "up") and a != 0:

                            if word_list[a-1] != "pick" and word_list[a-1] != "put":

                                verb = verbs[i][j]
                                verb_count += 1

                        elif word_list[a] == "put":

                            if a+1 != len(word_list):

                                if word_list[a+1] != "down":

                                    verb = verbs[i][j]
                                    verb_count += 1
                            
                            else:

                                verb = verbs[i][j]
                                verb_count += 1
                        
                        else:

                            verb = verbs[i][j]
                            verb_count += 1
                    
                    if a+1 != len(word_list):

                        if word_list[a] + " " + word_list[a+1] == verbs[i][j]:

                            verb = word_list[a] + " " + word_list[a+1]
                            verb_count += 1
    
    directions = (
            "n",
            "s",
            "e",
            "w",
            "north",
            "south",
            "east",
            "west",
            "u",
            "d",
            "up",
            "down",
            "nw",
            "ne",
            "sw",
            "se",
            "northwest",
            "northeast",
            "southwest",
            "southeast"
        )

    for i in range(len(directions)):

        if verb == directions[i] and verb_count == 2:

            verb_count = 1

    if verb == "move" or verb == "go":

        response = input("Which way do you want to move?\n>>> ")
        response = response.lower()
        response = response.split()

        direction = False
        direction_index = 0

        for i in range(len(directions)):

            for j in range(len(response)):

                if response[j] == directions[i]:

                    direction = True
                    direction_index = i
        
        if direction == True:

            verb = directions[direction_index]
        
        else:
            print("That's not a direction you can go!")
            return ""
            
    if verb_count == 1:

        for i in range(len(verbs)):

            for j in range(len(verbs[i])):

                if verb == verbs[i][j]:

                    verb = verbs[i][0]
        
        return verb

    elif verb_count == 0:

        print("There's no verb in that sentence!")
        return ""
    
    elif verb_count > 1:

        print("I don't understand that sentence!")
        return ""


def execute(verb, direct, indirect="", str_indirect=False):
    
    direct_object = Game.game.object_from_str(direct)

    if indirect and not str_indirect:

        indirect_object = Game.game.object_from_str(indirect)

    method = getattr(direct_object, verb)
    output = method(indirect_object)
    print(output)


def check_unknown_words(text):

    word_list = text.split(" ")
    unknown_word = ""

    verbs = [
        "move", "go",
        "n", "north",
        "s", "south",
        "e", "east",
        "w", "west",
        "nw", "northwest",
        "ne", "northeast",
        "sw", "southwest",
        "se", "southeast",
        "u", "up",
        "d", "down",
        "look", "location", "l",
        "inventory",
        "take", "get", "pick up", "grab", "steal", "hoist",
        "throw", "chuck", "hurl", "pitch",
        "open",
        "close",
        "read",
        "drop", "put down",
        "put", "put in",
        "lock",
        "unlock",
        "say", "speak", "talk",
        "turn on", "activate", "switch on",
        "turn off", "deactivate", "swith off",
        "hit", "kill", "attack", "strike", "smite", "slash", "destroy", "chop", "slice", "punch", "slap", "kick", "assault", "smack", "break",
        "examine", "search", "inspect",
        "eat", "consume", "devour", "gobble", "munch", "gnaw on",
        "drink", "guzzle", "sip", "swallow", "swig", "slurp"
    ]

    for word in word_list:

        if word not in verbs and not Game.object_from_str(word):

            unknown_word = word
            break
    
    return unknown_word


def find_direct_object(text, verb):

    word_list = text.split(" ")

    direct_object = ""

    for i in range(len(word_list)):

        if word_list[i] in verbs:

            known_list[i] = True
        
        elif Game.object_from_str(word_list[i]):

            known_list[i] = True

        else:

            unknown_word = word_list[i]
            break
    
    return unknown_word

def remove_arcticles(user_input):

    """Removes common articles from a string
    Args:
        userInput (str): string from which to remove the articles
    Returns:
        str: the string without the articles"""

    article_blacklist = ("a", "an", "the", "this", "that")

    for i in range(len(article_blacklist)):

        user_input = user_input.replace(article_blacklist[i]+" ", "")
        user_input = user_input.replace(" "+article_blacklist[i], "")
    
    return user_input

def clean_input(user_input):

    """Removes puctuation and caps from string
    Args:
        userInput (str): the string to have its punctuation removed
    Returns:
        str: string without puctuation or caps"""
    
    punc_blacklist = (".", ",", "<", ">", "?", "/", "\\", ";", ":", "'", "[", "]", "{", "}", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "_", "+", "=", "`", "~")

    for i in range(len(punc_blacklist)):

        user_input = user_input.replace(punc_blacklist[i], "")

    user_input = user_input.lower()

    return user_input

def move(direction):
    Game.game.player.move(direction)