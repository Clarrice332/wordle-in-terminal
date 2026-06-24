import random
from collections import Counter

MAX_GUESS_ATTEMPTS = 6
MAX_NUMBER_OF_LETTERS = 5
GREEN = "\033[42;30m"
YELLOW = "\033[43;30m"
GRAY = "\033[100;30m"
RESET = "\033[0m"

def get_secret_list():
    try:
        with open("secret words.txt", "r") as f:
            word_list = [line.strip().lower() for line in f.read().splitlines()]
        
        return word_list
    except FileNotFoundError:
        print("Error: file not found")
        
        return []
    
def get_valid_list():
    try:
        with open("valid words.txt", "r") as f:
            word_list = [line.strip().lower() for line in f.read().splitlines()]
        
        return word_list
    except FileNotFoundError:
        print("Error: file not found")
        
        return []
    
def get_secret_word(all_secrets):
    
    return random.choice(all_secrets)

def get_guess(all_valid):
    while True:
        guess = input("Guess: ")
        clean_guess = guess.strip().lower()

        if clean_guess not in all_valid or len(clean_guess) != 5:
            print("Not a valid guess.")
        else:
            break
    
    return clean_guess

def check_guess(secret_word, user_guess):
    color_letters = [0, 0, 0, 0, 0] # Create a list to hold our results (0=Gray, 1=Yellow, 2=Green)
    letter_storage = Counter(secret_word)

    for i in range(MAX_NUMBER_OF_LETTERS):
        if user_guess[i] == secret_word[i]:
            color_letters[i] = 2
            letter_storage[user_guess[i]] -= 1

    for i in range(MAX_NUMBER_OF_LETTERS):
        if color_letters[i] == 0:
            if user_guess[i] in secret_word and letter_storage[user_guess[i]] > 0:
                color_letters[i] = 1
                letter_storage[user_guess[i]] -= 1

    return color_letters

def print_colored_result(color_letters, user_guess):
    colored_result = ""
    
    for i in range(MAX_NUMBER_OF_LETTERS):
        letter = user_guess[i].upper()
        color = color_letters[i]

        if color == 2:
            colored_result += f"{GREEN} {letter} {RESET}"
        elif color == 1:
            colored_result += f"{YELLOW} {letter} {RESET}"
        else:
            colored_result += f"{GRAY} {letter} {RESET}"

    return colored_result
            
def game(all_valid, all_secrets):
    secret_word = get_secret_word(all_secrets)
    
    for attempt in range(MAX_GUESS_ATTEMPTS):
        user_guess = get_guess(all_valid)
        color_letters = check_guess(secret_word, user_guess)
        result = print_colored_result(color_letters, user_guess)
        if user_guess == secret_word:
            print(result)
            break
        else:
            print(result)

        if attempt == 5 and user_guess != secret_word:
            print("You didn't get the word.")
            
            for i in range(len(secret_word)):
                if i == 4:
                    print(f"{GREEN} {secret_word[i].upper()} {RESET}")
                else:
                    print(f"{GREEN} {secret_word[i].upper()} {RESET}", end="")
def main():
    all_valid = get_valid_list()
    all_secrets = get_secret_list()

    while True:
        choice = input("Press enter to play, q to quit: ")

        if choice == 'q':
            break

        game(all_valid, all_secrets)

main()