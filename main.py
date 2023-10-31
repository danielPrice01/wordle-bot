import random

global chosen_guess, num_green, num_yellow, num_gray, ge_y_ga_ltr, so_app_ltr, num_guesses, sto_cha_all, value_of_char

possible_answers = open("possible_answers", "r")
possible_guesses = open("possible_guesses", "r")
content_possible_answers = possible_answers.readlines()
content_possible_guesses = possible_guesses.readlines()
final_word = content_possible_answers[random.randint(0, len(content_possible_answers) - 1)][0:5]
chars = "abcdefghijklmnopqrstuvwxyz"
guess_or_random = input("Please input the number 1, or 2. "
                        "Would you like to:\n1: Solve today's Wordle\n2: Solve randomly generated word?\n")

og_p_answers = []
og_p_guesses = []
# Turns "possible_answers" and "possible_guesses" into two lists
for word in range(len(content_possible_answers)):
    og_p_answers.append(content_possible_answers[word].strip("\n"))
for word in range(len(content_possible_guesses)):
    og_p_guesses.append(content_possible_guesses[word].strip("\n"))

chosen_guess = ""
sto_cha_all = []

new_legal_ans = [og_p_answers]
new_legal_guess = [og_p_guesses]


def check_word():
    # Checks what letters in chosen_guess appear in actual word
    # Makes a list with the first entry of: the letter if it is right, and a space if not
    # In second entry there are the yellow letters
    # In the third entry are the gray letters
    # Additionally, create a list for green, yellow, and gray letter occurrences
    # In first entry how many letters there are, following entries in what position in the word they appear
    global num_green, num_yellow, num_gray, chosen_guess, ge_y_ga_ltr, sto_cha_all, value_of_char
    num_green = [0]
    num_yellow = [0]
    num_gray = [0]
    ge_y_ga_ltr = ["", "", ""]
    if guess_or_random == "2":
        for i in range(len(chosen_guess)):
            if chosen_guess[i] in final_word:
                if chosen_guess[i] in final_word[i]:
                    num_green[0] += 1
                    num_green.append(i)
                    ge_y_ga_ltr[0] += chosen_guess[i]
                    ge_y_ga_ltr[1] += " "
                    ge_y_ga_ltr[2] += " "
                else:
                    num_yellow[0] += 1
                    num_yellow.append(i)
                    ge_y_ga_ltr[1] += chosen_guess[i]
                    ge_y_ga_ltr[0] += " "
                    ge_y_ga_ltr[2] += " "
            if chosen_guess[i] not in final_word:
                num_gray[0] += 1
                num_gray.append(i)
                ge_y_ga_ltr[2] += chosen_guess[i]
                ge_y_ga_ltr[0] += " "
                ge_y_ga_ltr[1] += " "
    if guess_or_random == "1":
        for i in range(len(value_of_char[:4])):
            if value_of_char[i] == "g":
                num_green[0] += 1
                num_green.append(i)
                ge_y_ga_ltr[0] += chosen_guess[i]
                ge_y_ga_ltr[1] += " "
                ge_y_ga_ltr[2] += " "
            elif value_of_char[i] == "n":
                num_gray[0] += 1
                num_gray.append(i)
                ge_y_ga_ltr[2] += chosen_guess[i]
                ge_y_ga_ltr[0] += " "
                ge_y_ga_ltr[1] += " "
            elif value_of_char[i] == "y":
                num_yellow[0] += 1
                num_yellow.append(i)
                ge_y_ga_ltr[1] += chosen_guess[i]
                ge_y_ga_ltr[0] += " "
                ge_y_ga_ltr[2] += " "


def update_available_words(og_p_ans):
    # Creates a list with three entries called "legal_word"
    # Checks whether any of the listed gray letters appear in each word in the available words list
    # Checks whether green letters are listed in the same location in the available words list
    # Checks whether yellow letters are listed in the word but in a different location in available words list
    # Each time a test is passed, "y" is added to the corresponding location in "legal_word"
    # If there are no green, gray, or yellow letters, "y" is added to corresponding location in "legal_word"
    # If a word has a value of "y", "y", "y" in "legal_word", then it is considered a legal word and added to new list
    new_legal_words = []
    for i in range(len(og_p_ans)):
        legal_word = ["", "", ""]
        if num_gray[0] == 0:
            legal_word[0] = "y"
        if num_green[0] == 0:
            legal_word[1] = "y"
        if num_yellow[0] == 0:
            legal_word[2] = "y"
        for gray in range(num_gray[0]):
            if legal_word[0] != "n":
                if ge_y_ga_ltr[2][num_gray[gray + 1]] not in og_p_ans[i]:
                    legal_word[0] = "y"
                if ge_y_ga_ltr[2][num_gray[gray + 1]] in og_p_ans[i]:
                    legal_word[0] = "n"
        if legal_word[0] != "n":
            for green in range(num_green[0]):
                if legal_word[1] != "n":
                    if ge_y_ga_ltr[0][num_green[green + 1]] in og_p_ans[i][num_green[green + 1]]:
                        legal_word[1] = "y"
                    if ge_y_ga_ltr[0][num_green[green + 1]] not in og_p_ans[i][num_green[green + 1]]:
                        legal_word[1] = "n"
        if legal_word[1] != "n" and legal_word[0] != "n":
            for yellow in range(num_yellow[0]):
                if legal_word[2] != "n":
                    if ge_y_ga_ltr[1][num_yellow[yellow + 1]] in og_p_ans[i]:
                        if ge_y_ga_ltr[1][num_yellow[yellow + 1]] not in og_p_ans[i][num_yellow[yellow + 1]]:
                            legal_word[2] = "y"
                        else:
                            legal_word[2] = "n"
                    if ge_y_ga_ltr[1][num_yellow[yellow + 1]] not in og_p_ans[i]:
                        legal_word[2] = "n"
        if legal_word == ["y", "y", "y"]:
            new_legal_words.append(og_p_ans[i])
    return new_legal_words


def guess_word():
    def rank_words_to_guess():
        global ge_y_ga_ltr, num_green, num_gray, num_yellow
        # Creates a dictionary of every letter in the alphabet, and the value of 0
        appearance_letters = {}
        for char in range(len(chars)):
            appearance_letters.update({str(chars[char]): 0})
        # Checks each word in "newly_available_words" corresponding to "possible_answers" file
        # Adds to "appearance_letters" dict how many words have each letter in the alphabet
        # If a letter appears in multiple times in one word, it will be added to the dict
        check_word()
        sto_cha_all.append(ge_y_ga_ltr)
        new_legal_words = update_available_words(new_legal_ans[-1])
        new_legal_ans.append(new_legal_words)
        for i in range(len(new_legal_words)):
            for letter in range(len(chars)):
                if chars[letter] in new_legal_words[i]:
                    appearance_letters[chars[letter]] += 1
                if new_legal_words[i].count(chars[letter]) > 1:
                    recurring_letter = chars[letter] * new_legal_words[i].count(chars[letter])
                    if recurring_letter in appearance_letters:
                        appearance_letters[recurring_letter] += 1
                    if recurring_letter not in appearance_letters:
                        appearance_letters.update({recurring_letter: 1})

        # Sorts the appearance_letters dict, based on how many words each entry appears in
        global so_app_ltr
        so_app_ltr = dict(sorted(appearance_letters.items(), key=lambda x: x[1]))

        # Checks each word in "newly_available_words" corresponding to the "possible_guesses" file
        # Goes through each character in each possible guess, and adds to the "points_per_word" dict
        # The dict has the word, followed by how many points the word is valued at
        # Points are decided based on the letters in the word
        # Letters are ranked based on how many words they appear in
        # Program then chooses the word with the most points, assigning it to "word_to_guess"
        points_per_word = {}
        check_word()
        new_legal_words = update_available_words(new_legal_guess[-1])
        new_legal_guess.append(new_legal_words)
        for ans in range(len(new_legal_words)):
            current_points = 0
            for loc in range(len(new_legal_words[ans])):
                number_appears = new_legal_words[ans].count(new_legal_words[ans][loc])
                repeat = str(new_legal_words[ans][loc] * new_legal_words[ans].count(new_legal_words[ans][loc]))
                if number_appears == 1:
                    current_points += list((so_app_ltr.keys())).index(str(new_legal_words[ans][loc]))
                if number_appears > 1:
                    current_points += list((so_app_ltr.keys())).index(str(new_legal_words[ans][loc])) / number_appears
                    if repeat in so_app_ltr:
                        current_points += list((so_app_ltr.keys())).index(repeat) / number_appears
                    if repeat not in so_app_ltr:
                        current_points += 0
            points_per_word.update({new_legal_words[ans]: current_points})
        sorted_p_p_w = list(sorted(points_per_word.items(), key=lambda x: x[1]))
        word_to_guess = sorted_p_p_w[-1][0]
        return word_to_guess

    global chosen_guess, num_guesses, value_of_char
    num_guesses = 0

    def make_a_guess():
        global chosen_guess, num_guesses, sto_cha_all
        num_guesses += 1
        chosen_guess = rank_words_to_guess()
        print(f"Guess {num_guesses}: {chosen_guess}")

    if guess_or_random == "2":
        while chosen_guess != final_word:
            make_a_guess()
            if num_guesses == 6:
                break
        if chosen_guess == final_word:
            print(f"The correct word has been guessed, after {num_guesses} words. The word is {chosen_guess}")
    if guess_or_random == "1":
        value_of_char = ""
        ge_y_ga_ltr = ["", "", ""]
        num_green = [0]
        num_yellow = [0]
        num_gray = [0]
        make_a_guess()
        while value_of_char[:4] != "ggggg":
            value_of_char = input("Write 'g' if the letter is green, 'n' if it is gray, and 'y' if it is yellow\n")
            check_word()
            make_a_guess()
            if num_guesses == 6:
                break
        if value_of_char[:4] != "ggggg":
            print(f"The correct word has been guessed, after {num_guesses} words. The word is {chosen_guess}")


guess_word()
