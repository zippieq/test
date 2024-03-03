import random
import string

WORDLIST_FILENAME = "words.txt"

def load_words():
    with open(WORDLIST_FILENAME, 'r') as file:
        words = file.readlines()
        word_list = [word.strip().lower() for word in words]
        return word_list

def choose_word(word_list):
    return random.choice(word_list)

def is_word_guessed(secret_word, letters_guessed):
    return set(secret_word) == set(letters_guessed)

def get_guessed_word(secret_word, letters_guessed):
    return ''.join([letter if letter in letters_guessed else '_ ' for letter in secret_word])

def get_available_letters(letters_guessed):
    alphabet = string.ascii_lowercase
    return ''.join([letter for letter in alphabet if letter not in letters_guessed])

def is_valid_guess(letter):
    return len(letter) == 1 and letter.isalpha()

def hangman(secret_word):
    num_guesses_remaining = 6
    warnings = 3
    letters_guessed = []

    print("Welcome to the game Hangman!")
    print(f"I am thinking of a word that is {len(secret_word)} letters long.")
    print("Accumulating three warnings will lose you a guess.")
    print("-------------------------------------------")

    while num_guesses_remaining > 0:
        print(f"You have {num_guesses_remaining} guesses left.")
        print(f"Available letters: {get_available_letters(letters_guessed)}")
        letter = input("Guess a letter: ").lower()

        if is_valid_guess(letter):
            if letter in letters_guessed:
                if warnings > 0:
                    warnings -= 1
                    print(f"You've already guessed that letter. You have {warnings} warnings left.")
                else:
                    num_guesses_remaining -= 1
                    print("You have no warnings left. Sorry, you will lose a guess.")
            else:
                letters_guessed.append(letter)
                if letter in secret_word:
                    print(f"Good guess: {get_guessed_word(secret_word, letters_guessed)}")
                else:
                    print(f"Sorry, that letter is not in my word: {get_guessed_word(secret_word, letters_guessed)}")
                    if letter in "aeiou":
                        num_guesses_remaining -= 2
                        print("You entered a vowel letter, that will cost you 2 guesses.")
                    else:
                        num_guesses_remaining -= 1
                        print("You entered a consonant letter, you will lose a guess.")
        else:
            if warnings > 0:
                warnings -= 1
                print(f"Invalid input. Please enter letters only. You have {warnings} warnings left.")
            else:
                num_guesses_remaining -= 1
                print("You have no warnings left. Sorry, you will lose a guess.")

        if is_word_guessed(secret_word, letters_guessed):
            print(f"\nCongratulations! You guessed my word: {secret_word}")
            print(f"Your total score: {num_guesses_remaining * len(set(secret_word))}")
            break

        print("-------------------------------------------")

    else:
        print(f"Sorry, you ran out of guesses. The word was: {secret_word}")