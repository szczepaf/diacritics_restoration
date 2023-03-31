import re
import os
import json
import requests
import jellyfish
import prettytable


#README: https://github.com/szczepaf/diacritics_restoration/tree/main/README.md


def print_info() -> None:
    """Introduction to the experiment"""
    print("This program will restore diacritics of a Czech text using a mapping of words without diacritics to words with diacritics created from the most read articles in February 2023 at Czech Wikipedia and 15 Czech novels.", end = "\n" * 2)
    print("More information: https://github.com/szczepaf/diacritics_restoration/tree/main/README.md", end = "\n" * 3)



def remove_diacritics(word: str, diacritics: list) -> str:
    """Removes diacritics from a word."""
    word_without_diacritics = ""
    for letter in word:
            if letter in diacritics:
                letter = letter.replace(letter, "*")
            word_without_diacritics += letter
    return word_without_diacritics


def process_word(word: str, mapping: dict, diacritics: list) -> None:
    """Processes a word and adds it to the mapping."""
    word = word.lower()
    word = word.strip(".,;:!?()[]{}\"\'")
    if word == "":
        return None

    if any(char in diacritics for char in word):
        word_without_diacritics = remove_diacritics(word, diacritics)
        if word_without_diacritics in mapping:
            if word in mapping[word_without_diacritics]:
                mapping[word_without_diacritics][word] += 1
            else:
                mapping[word_without_diacritics][word] = 1
        else:
            mapping[word_without_diacritics] = dict()
            mapping[word_without_diacritics][word] = 1



def create_mapping(diacritics: list) -> dict:
    """Creates a mapping from 500 Czech most read Wiki articles and some Czech literature.
    Returns a dictionary with words without diacritics as keys. Values will also be dictionaries with words with diacritics as keys and their frequencies as values."
    """

    print("Creating a mapping from the most read articles in February 2023 at Czech Wikipedia...") 
    mapping = dict()
    mapping_size = 0
    wiki_text = ""


    

    #Download the Wikipedia 'corpus'
    url = f'https://raw.githubusercontent.com/szczepaf/diacritics_restoration/main/training_data/wiki_text.txt'
    wiki_text = requests.get(url).text
    words = wiki_text.split()
    mapping_size += len(words)

    for word in words:
                process_word(word, mapping, diacritics)

    print("Mapping size with WIKI articles: " + str(mapping_size), end = "\n" * 2)


    #Add 15 Czech novels to the mapping

    novels = ["babicka.txt", "chram_matky_bozi.txt", "lovci_mamutu.txt", "oliver_twist.txt", "postriziny.txt", "quo_vadis.txt", "velky_gatsby.txt", "zlocin_a_trest.txt", "bila_velryba.txt", "druhe_mesto.txt", "mistr_a_marketka.txt", "ostre_sledovane_vlaky.txt", "promeny.txt", "robinson_crusoe.txt", "zbabelci.txt"]
    print("Downloading 15 Czech novels and processing them...", end = "\n")
    # loop through each novel and download it
    i  = 1

    for novel in novels:
        print(f"Downloading novel {novel}...")
        url = f'https://raw.githubusercontent.com/szczepaf/diacritics_restoration/main/training_data/novels/{novel}'
        novel_text = requests.get(url).text
        novel_name = novel.strip("txt")
        print(f"Processing novel {novel_name} - {i} out of total 15...", end = "\n" * 2)
        i += 1

        words = novel_text.split()
        for word in words:
            process_word(word, mapping, diacritics)
        mapping_size += len(words)

    print(f"Mapping created, total number of words processed is: {mapping_size}")
    


    return mapping






def restore_word(word: str, mapping: dict) -> str:
    """Restores a word with diacritics from a mapping."""
    hadTripleDot = word.endswith("...")
    hadDot = (word.endswith(".") and not hadTripleDot)
    hadComma = word.endswith(",")
    hadQuestionMark = word.endswith("?")
    hadExclamationMark = word.endswith("!")
    hadColon = word.endswith(":")
    hadSquareBracketsRight = word.endswith("]")
    hadSquareBracketsLeft = word.startswith("[")
    hadRoundBracketsRight = word.endswith(")")
    hadRoundBracketsLeft = word.startswith("(")

    word_cleared = word.strip(",.!?()[]:")
    wasUpper = word_cleared[0].isupper()

    word_lower = word_cleared.lower()

    
    if word_lower in mapping:
        word_restored = max(mapping[word_lower], key=mapping[word_lower].get)
    else:
       return word

    #now restore the original form of the word
    if wasUpper:
        word_restored = word_restored.capitalize()
    #if hadTripleDot:
    #   word_restored += "..."
    if hadDot:
        word_restored += "."
    if hadComma:
        word_restored += ","
    if hadQuestionMark:
        word_restored += "?"
    if hadExclamationMark:
        word_restored += "!"
    if hadColon:
        word_restored += ":"
    #restore all brackets, square and round
    if hadSquareBracketsLeft:
        word_restored = "[" + word_restored
    if hadSquareBracketsRight:
        word_restored += "]"
    if hadRoundBracketsLeft:
        word_restored = "(" + word_restored
    if hadRoundBracketsRight:
        word_restored += ")"

    return word_restored


def restore_diacritics(text: str, mapping: dict) -> str:
    """Restores diacritics in a text.
    The function first clears the text of all non-ASCII chars, replaces them with a designated char
    and then restores diacritics in each word.
    """
    cleared_text = re.sub(r"[^\x00-\x7F][^\x00-\x7F]", "*", text)
    words = cleared_text.split()

    restored_text = ""

    for word in words:
        if "*" in word:
            restored_word = restore_word(word, mapping)
        else:
            restored_word = word
        restored_text += restored_word + " "
    return restored_text





def accuracy(gold: str, system: str) -> float:
    """Computes the accuracy of the system output.
    This evaluation function was taken from the assignment in the class Python Machine Learning for Greenhorns."""
    assert isinstance(gold, str) and isinstance(system, str), "The gold and system outputs must be strings"

    gold, system = gold.split(), system.split()
    
    #Uncomment this to see the each of the original and corrupted/restored words.
    #for i in range(min(len(gold), len(system))):
    #    print(f"{i}, {gold[i]}, {system[i]}")


   
    assert len(gold) == len(system), \
        "The gold and system outputs must have the same number of words: {} vs {}.".format(len(gold), len(system))

    words, correct = 0, 0
    for gold_token, system_token in zip(gold, system):
        words += 1
        correct += gold_token == system_token

    return correct / words


def evaluate(data_before_correction:str, data_after_correction: str, correct_data: str, correct_data2) -> None:
    """Evaluates the quality of the correction."""
    print("Running the evaluation...", end = "\n")


    lavenshtein_distance_corrupted_original = round(jellyfish.levenshtein_distance(data_before_correction, correct_data), 3)
    lavenshtein_distance_corrected_and_original = round(jellyfish.levenshtein_distance(data_after_correction, correct_data), 3)

    jaro_similarity_corrupted_original = round(jellyfish.jaro_distance(data_before_correction, correct_data), 3)
    jaro_similarity_corrected_and_original = round(jellyfish.jaro_distance(data_after_correction, correct_data), 3)

    jaro_winkler_similarity_corrupted_original  = round(jellyfish.jaro_winkler(data_before_correction, correct_data), 3)
    jaro_winkler_similarity_corrected_and_original = round(jellyfish.jaro_winkler(data_after_correction, correct_data), 3)


    #compute the accuracy using the function accuracy
    accuracy_before_correction = round(accuracy(correct_data2, data_before_correction), 3)
    accuracy_after_correction = round(accuracy(correct_data, data_after_correction), 3)


    print("Used metrics are: Lavenshtein distance, Jaro similarity, Jaro-Winkler similarity, and accuracy as the ratio of total correct words.")

    #use prettytable to display the results
    t = prettytable.PrettyTable(["Metric", "Before restoration", "After restoration"])
    t.add_row(["Levenshtein distance", lavenshtein_distance_corrupted_original, lavenshtein_distance_corrected_and_original])
    t.add_row(["Jaro similarity", jaro_similarity_corrupted_original, jaro_similarity_corrected_and_original])
    t.add_row(["Jaro-Winkler similarity", jaro_winkler_similarity_corrupted_original, jaro_winkler_similarity_corrected_and_original])
    t.add_row(["Accuracy", accuracy_before_correction, accuracy_after_correction])
    print(t)


    




def main():

    diacritics = ["á", "é", "ě", "í", "ó", "ú", "ů", "ý", "č", "ď", "ň", "ř", "š", "ť", "ž"]

    print_info()


    #If mapping already exists, load it from disk, otherwise create it
    if os.path.exists("mapping.json"):

        with open("mapping.json", "r", encoding="utf-8") as f:
            mapping = json.load(f)

        print("The experiment has been run before. Training data has already been downloaded and mapping created...", end = "\n" * 3)
        print("mapping loaded from disk.")
    else:
        print("Experiment is running for the first time on this machine. The training data will be downloaded and mapping created...", end = "\n" * 3)
        
        mapping = create_mapping(diacritics)
        
        with open("mapping.json", "w", encoding="utf-8") as f:
            json.dump(mapping, f, indent=2)
        print("mapping saved to disk.", end = "\n" * 2)

    #Get the dev and eval data from the class website
    print("Gathering dev data...")
    dev_data = requests.get("https://ufal.mff.cuni.cz/~zabokrtsky/courses/npfl124/data/diacritics-dtest.txt").text
    eval_data = requests.get("https://ufal.mff.cuni.cz/~zabokrtsky/courses/npfl124/data/diacritics-etest.txt").text


    #restore diacritics
    print("Restoring diacritics for dev data...")
    dev_data_restored = (restore_diacritics(dev_data, mapping))


    #read the correct (original, non-corrupted) dev data from the file dev_data_correct
    with open("dev_data_correct.txt", "r", encoding="utf-8") as f:
        dev_data_correct = f.read()

    #read the correct (original, non-corrupted) dev data from the file dev_data_correct
    #version 2 for eval and dev data:
    #This is because the lengths are differing by 2 when comparing the corrupted and original data.
    #The cause is due to the fact that some non-ASCII characters coming in the corrupted files are interpreted as a whitespace.
    #We need to manualy change about 10 characters in the files so the accuracy comparison word by word is possible.
    #This does not affect the results in any measurable way.

    with open("dev_data_correct2.txt", "r", encoding="utf-8") as f:
        dev_data_correct2 = f.read()


    #Repeat the process with Evaluation data
    print("Gathering eval data...")
    print("Restoring diacritics for eval data...")

    eval_data_restored = (restore_diacritics(eval_data, mapping))

    with open("eval_correct.txt", "r", encoding="utf-8") as f:
        eval_correct = f.read()

    with open("eval_correct2.txt", "r", encoding="utf-8") as f:
        eval_correct2 = f.read()

    print("EVALUATING DEV DATA", end = "\n" * 2)
    evaluate(dev_data, dev_data_restored, dev_data_correct, dev_data_correct2)
    print("\n" * 3)

    print("EVALUATING EVAL DATA", end = "\n" * 2)
    evaluate(eval_data, eval_data_restored, eval_correct2, eval_correct)
    print("\n" * 3)



    #write the resulting corrected data to a file results.txt
    with open("resultsDev.txt", "w", encoding="utf-8") as f:
        f.write(dev_data_restored)

    with open("resultsEval.txt", "w", encoding="utf-8") as f:
        f.write(eval_data_restored)


if __name__ == "__main__":
    main()


