#from Game import game

def parse(user_input):

    """Parses raw user input and calls proper method in entity or room.
    Args:
        userInput (str): the raw user input"""

    user_input_arts = clean_input(user_input)
    user_input = remove_arcticles(user_input_arts)
    unknown = check_unknown_words(user_input)

    if unknown:
        print("I don't know the word: \"" + unknown + ".\"")

    else:
        verb, og_verb = find_verb(user_input)

        if verb:
            needs_direct = requires_object(verb, "direct")

            if needs_direct:
                direct = find_direct_object(user_input, og_verb)

                if direct:
                    if len(direct) > 1 and not supports_multiple_direct_objects(verb):
                        print("You can't use more than one direct object with the verb: \"" + og_verb + ".\"")

                    else:
                        needs_indirect = requires_object(verb, "indirect")

                        if needs_indirect:
                            indirect = find_indirect_object(user_input, og_verb, direct[0])

                            if len(indirect) > 1:
                                print("You can't use multiple indirect objects with the verb: \"" + og_verb + ".\"")

                            elif len(indirect) == 1:
                                execute(verb, direct, indirect)

                        else:
                            execute(verb, direct)

            else:
                execute(verb, "player")


def supports_multiple_direct_objects(verb):

    supports_list = ("take", "drop")

    if verb in supports_list:

        return True

    else:

        return False


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
    og_verb = ""
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
                    og_verb = verbs[i][j]

        return verb, og_verb

    elif verb_count == 0:

        print("There's no verb in that sentence!")
        return "", ""

    elif verb_count > 1:

        print("I don't understand that sentence!")
        return "", ""


def execute(verb, direct, indirect="", str_indirect=False):

    direct_object = game.object_from_str(direct)

    if indirect and not str_indirect:

        indirect_object = game.object_from_str(indirect)

    method = getattr(direct_object, verb)
    output = method(indirect_object)
    print(output)


def check_unknown_words(text):

    word_list = text.split(" ")
    known_list = [False for x in word_list]
    unknown_word = ""

    white_list = ("and", "to", "all", "use", "using", "with", "i")

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

    for i in range(len(word_list)-1):

        if word_list[i] + " " + word_list[i+1] in verbs or game.object_from_str(word_list[i] + " " + word_list[i+1]) or word_list[i] + " " + word_list[i+1] in white_list:

            known_list[i] = True
            known_list[i+1] = True

    for i in range(len(word_list)):

        if word_list[i] in verbs or game.object_from_str(word_list[i]) or word_list[i] in white_list:

            known_list[i] = True

    for i in range(len(word_list)):

        if not known_list[i]:

            unknown_word = word_list[i]
            break

    return unknown_word


def find_indirect_object(text, verb, direct):

    word_list = text.split()
    verb_words = verb.split()

    if len(verb_words) > 1:

        for i in range(len(word_list)):

            if word_list[i] == verb_words[0]:

                word_list[i:i+(len(verb_words)-1)] = verb
                break


    indirect_object = []

    verb_index = word_list.index(verb)

    indirect_qualifyers = ("use", "using", "with")
    qualifyer_index = None
    qualifyer_count = 0

    for i in range(len(word_list)):

        for qualifyer in indirect_qualifyers:

            if word_list[i] == qualifyer:

                qualifyer_index = i
                qualifyer_count += 1

    if qualifyer_count > 1:

        print("I don't understand that sentence!")

    if qualifyer_count <= 1:

        if qualifyer_count == 1:

            if qualifyer_index < verb_index:

                word_list = word_list[:verb_index]

            elif qualifyer_index > verb_index:

                word_list = word_list[qualifyer_index:]

            counted_list = [False for x in word_list]

            for i in range(len(word_list)-1):

                if game.object_from_str(word_list[i] + " " + word_list[i+1]) and not counted_list[i] and not counted_list[i+1]:

                    indirect_object.append(word_list[i] + " " + word_list[i+1])
                    counted_list[i] = True
                    counted_list[i+1] = True

            for i in range(len(word_list)):

                if game.object_from_str(word_list[i]) and not counted_list[i]:

                    indirect_object.append(word_list[i])
                    counted_list[i] = True

        if not indirect_object:

            user_input = input("What do you want to " + verb + " the " + direct + " with?\n>>> ")
            user_input = clean_input(user_input)
            user_input = remove_arcticles(user_input)
            unknown = check_unknown_words(user_input)

            if unknown:

                print("I don't know the word: \"" + unknown +".\"")

            else:

                input_words = user_input.split()
                counted_list = [False for x in input_words]

                for i in range(len(input_words)-1):

                    if game.object_from_str(input_words[i] + " " + input_words[i+1]) and not counted_list[i] and not counted_list[i+1]:

                        indirect_object.append(input_words[i] + " " + input_words[i+1])
                        counted_list[i] = True
                        counted_list[i+1] = True

                for i in range(len(input_words)):

                    if game.object_from_str(input_words[i]) and not counted_list[i]:

                        indirect_object.append(input_words[i])
                        counted_list[i] = True

                    elif input_words[i] == "all":

                        indirect_object.append(input_words[i])
                        counted_list[i] = True

                if not indirect_object:

                    print("What?")

    return indirect_object




def find_direct_object(text, verb):

    word_list = text.split()
    verb_words = verb.split()

    if len(verb_words) > 1:

        for i in range(len(word_list)):

            if word_list[i] == verb_words[0]:

                word_list[i] = verb
                del word_list[i+1]
                break


    direct_object = []

    verb_index = word_list.index(verb)

    indirect_qualifyers = ("use", "using", "with")
    qualifyer_index = None
    qualifyer_count = 0

    for i in range(len(word_list)):

        for qualifyer in indirect_qualifyers:

            if word_list[i] == qualifyer:

                qualifyer_index = i
                qualifyer_count += 1

    if qualifyer_count == 1:

        if qualifyer_index < verb_index:

            word_list = word_list[verb_index:]

        elif qualifyer_index > verb_index:

            word_list = word_list[:qualifyer_index]

    if qualifyer_count > 1:

        print("I don't understand that sentence!")

    else:

        verb_index = word_list.index(verb)
        del word_list[verb_index]

        counted_list = [False for x in word_list]

        for i in range(len(word_list)-1):

            if game.object_from_str(word_list[i] + " " + word_list[i+1]) and not counted_list[i] and not counted_list[i+1]:

                direct_object.append(word_list[i] + " " + word_list[i+1])
                counted_list[i] = True
                counted_list[i+1] = True

        for i in range(len(word_list)):

            if game.object_from_str(word_list[i]) and not counted_list[i]:

                direct_object.append(word_list[i])
                counted_list[i] = True

            elif word_list[i] in ("all", "everything",):

                direct_object.append("all")
                counted_list[i] = True

        if not direct_object:

            user_input = input("What do you want to " + verb + "?\n>>> ")
            user_input = clean_input(user_input)
            user_input = remove_arcticles(user_input)
            unknown = check_unknown_words(user_input)

            if unknown:

                print("I don't know the word: \"" + unknown +".\"")

            else:

                input_words = user_input.split()
                counted_list = [False for x in input_words]

                for i in range(len(input_words)-1):

                    if game.object_from_str(input_words[i] + " " + input_words[i+1]) and not counted_list[i] and not counted_list[i+1]:

                        direct_object.append(input_words[i] + " " + input_words[i+1])
                        counted_list[i] = True
                        counted_list[i+1] = True

                for i in range(len(input_words)):

                    if game.object_from_str(input_words[i]) and not counted_list[i]:

                        direct_object.append(input_words[i])
                        counted_list[i] = True

                    elif input_words[i] == "all":

                        direct_object.append(input_words[i])
                        counted_list[i] = True

                if not direct_object:

                    print("What?")

    return direct_object


def remove_arcticles(user_input):

    """Removes common articles from a string
    Args:
        userInput (str): string from which to remove the articles
    Returns:
        str: the string without the articles"""

    article_blacklist = ("a", "an", "the", "this", "that")

    word_list = user_input.split()

    for article in article_blacklist:

        if article in word_list:

            for i in range(word_list.count(article)):

                word_list.remove(article)

    return " ".join(word_list)


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