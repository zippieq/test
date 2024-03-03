import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    print("Loading word list from file...")
    wordlist = open("words.txt").read().split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist

    print(line)


def choose_word(wordlist):
    return random.choice(wordlist)


def get_len_word(secretword):
    unique_letters_secret_word = set(secret_word)
    len_secret_word = len(unique_letters_secret_word)
    return len_secret_word
# -----------------------------------


wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''

    secret_word_list = []
    for letter in secret_word:
        secret_word_list.append(letter)

    common_letters = []
    for letter in secret_word:
        if letter in letters_guessed:
            common_letters.append(letter)

    if sorted(common_letters) == sorted(secret_word_list):
        return True
    else:
        return False


def get_guessed_word(secret_word, letters_guessed):
    word = ''
    for letter in secret_word:
        if letter in letters_guessed:
            word += letter
        else:
            word += '_ '
    return word


def get_available_letters(letters_guessed):

    alphabet = string.ascii_lowercase
    available_letters = ''

    for letter in alphabet:
        if letter not in letters_guessed:
            available_letters += letter
    return available_letters


def hangman(secret_word):
    letters_guessed = []
    letters_guessed_clone = []
    len_secret_word = len(secret_word)
    loop = 0
    num_guesses_remaining = 6
    warnings = 3
    print("Welcome to the game Hangman!")
    print("I am thinking of a word that is {} letters long.".format(len_secret_word))
    print("Accummulating three warnings will lose you a guess.\n")
    print("-------------------------------------------")

    while num_guesses_remaining > 0:
        letter = guess_something(secret_word, letters_guessed, letters_guessed_clone, loop, num_guesses_remaining, warnings)
        if not str.isalpha(letter):
            handle_not_vowel_letter(secret_word, letters_guessed, num_guesses_remaining, warnings)
        if warnings < 0:
            num_guesses_remaining -= 1
            print("You have no warnings left. Sorry, you will lose a guess.")
        if is_word_guessed(secret_word, letters_guessed):
            print("\nCongratulations! You guessed my word.")
            print("Your total score: {}".format(
                num_guesses_remaining * get_len_word(secret_word)))
            break
        loop += 1
        print("-------------------------------------------")
    else:
        print("You ran out of guesses. The word is {}.".format(secret_word))

def handle_not_vowel_letter(secret_word, letters_guessed, num_guesses_remaining, warnings):
    if warnings > 0:
        warnings -= 1
        print("Invalid input. Please enter letters only.", end=" ")
        if warnings == 1 or warnings == 0:
            print("You now have {} warning left: ".format(warnings))
        else:
            print("You now have {} warnings left: ".format(warnings))
        print("Word to guess:", get_guessed_word(
                    secret_word, letters_guessed))
    else:
        num_guesses_remaining -= 1
        print("You have no warnings left. Sorry, you will lose a guess.")

def guess_something(secret_word, letters_guessed, letters_guessed_clone, loop, num_guesses_remaining, warnings):
    print("Secret word:", secret_word)
    print("You have {} guess(es) left. Good luck!".format(
                num_guesses_remaining))
    print("Available letters:", get_available_letters(letters_guessed))
    letter = str(input("Guess a letter: ")).lower()
    print()
    if str.isalpha(letter):
        if len(letter) > 1:
            print("Please enter one letter at a time.")
        if len(letter) == 1:
            letters_guessed.append(letter)
            if letter in secret_word:
                correct_letter(secret_word, letters_guessed, letters_guessed_clone, loop, num_guesses_remaining, warnings, letter)
            else:
                wrong_letter(secret_word, letters_guessed, num_guesses_remaining, letter)                        
    return letter
# -----------------------------------
def hangman_with_hints(secret_word):
    letters_guessed = []
    letters_guessed_clone = []
    len_secret_word = len(secret_word)
    exemption = "*"
    loop = 0
    num_guesses_remaining = 6
    warnings = 3
    print("Welcome to the game Hangman!")
    print("The word is {} letters long.".format(len_secret_word))
    print("Accummulating three warnings will lose you a guess.\n")
    print("-------------------------------------------")

    while num_guesses_remaining > 0:
        if num_guesses_remaining > 1:
            print("You have {} guesses left. Good luck!".format(
                num_guesses_remaining))
        else:
            print("You have {} guess left. Good luck!".format(
                num_guesses_remaining))
        print("Available letters:", get_available_letters(letters_guessed))
        letter = str(input("Guess a letter: ")).lower()
        if letter == "*":
            show_possible_matches(get_guessed_word(
                secret_word, letters_guessed))
        print()
        if str.isalpha(letter):
            if len(letter) > 1:
                print("Please enter one letter at a time.")
            if len(letter) == 1:
                letters_guessed.append(letter)
                if letter in secret_word:
                    correct_letter(secret_word, letters_guessed, letters_guessed_clone, loop, num_guesses_remaining, warnings, letter)
                else:
                    wrong_letter(secret_word, letters_guessed, num_guesses_remaining, letter)
        if not str.isalpha(letter) and letter != exemption:
            if warnings > 0:
                warnings -= 1
                print("Invalid input. Please enter letters only.", end=" ")
                if warnings == 1 or warnings == 0:
                    print("You now have {} warning left: ".format(warnings))
                else:
                    print("You now have {} warnings left: ".format(warnings))
                print("Word to guess:", get_guessed_word(
                    secret_word, letters_guessed))
            else:
                num_guesses_remaining -= 1
                print("You have no warnings left. Sorry, you will lose a guess.")
        if warnings < 0:
            num_guesses_remaining -= 1
            print("You have no warnings left. Sorry, you will lose a guess.")
        if is_word_guessed(secret_word, letters_guessed):
            print("\nCongrats! You guessed my word.")
            print("Your total score: {}".format(
                num_guesses_remaining * get_len_word(secret_word)))
            break
        loop += 1
        print("-------------------------------------------")
    else:
        print("Sorry you ran out of guesses. The word is {}.".format(secret_word))

def wrong_letter(secret_word, letters_guessed, num_guesses_remaining, letter):
    print("Sorry, that letter is not in my word: ",
                          get_guessed_word(secret_word, letters_guessed))
    if letter in "aeiou":
        num_guesses_remaining -= 2
        print("You entered a vowel letter, that will cost you 2 guesses.")
    else:
        num_guesses_remaining -= 1
        print("You entered a consonant letter, you will lose a guess.")

def correct_letter(secret_word, letters_guessed, letters_guessed_clone, loop, num_guesses_remaining, warnings, letter):
    if loop == 0:
        print("Good guess:", get_guessed_word(
                            secret_word, letters_guessed))
    if loop >= 1:
        letters_guessed_clone.append(
                            letters_guessed[len(letters_guessed) - 2])
        if letter in letters_guessed_clone:
            if warnings > 0:
                warnings -= 1
                print("You have already guessed that letter.", end=" ")
                if warnings == 1 or warnings == 0:
                    print("You now have {} warning left: ".format(warnings))
                else:
                    print("You now have {} warnings left: ".format(warnings))
                print("Word to guess:", get_guessed_word(
                                    secret_word, letters_guessed))
            else:
                num_guesses_remaining -= 1
                print("You have no warnings left. Sorry, you will lose a guess.")
        else:
            print("Good guess:", get_guessed_word(
                                secret_word, letters_guessed))

if __name__ == "__main__":
    #secret_word = choose_word(wordlist)
    # hangman(secret_word)

    ###############

    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)