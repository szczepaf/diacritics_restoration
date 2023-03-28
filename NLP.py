import wikipedia
import time
import pandas as pd
import re
import os
import json



#This will be a program for the restoration of czech diacritics.
#In the first step, a corpus will be created from the Czech Wikipedia.
#A dictionary with words with removed diacritics as keys and most frequent corresponding words with diacritics as values will be created.
#The program will then be able to restore diacritics in a text.



def load_URLs(path:str) -> list:

    """Loads URLs from a file with csv data about top wiki articles and returns a list containing them."""
    print("Loading URLs from a csv wikismetrics file...")

    #the csv files has columns article, rank, timestamp, etc.
    #We only need the first column.
    df = pd.read_csv(path)
    URLs = df["article"].tolist()
    time.sleep(0.5)
    print("URLs loaded.", end = "\n" * 3)
    return URLs



def remove_diacritics(word: str, diacritics: list) -> str:
    """Removes diacritics from a word."""
    word_without_diacritics = ""
    for letter in word:
            if letter in diacritics:
                letter = letter.replace(letter, "*")
            word_without_diacritics += letter
    return word_without_diacritics


def process_word(word: str, corpus: dict, diacritics: list) -> None:
    """Processes a word and adds it to the corpus."""
    word = word.lower()
    word = word.strip(".,;:!?()[]{}\"\'")
    if word == "":
        return None

    if any(char in diacritics for char in word):
        word_without_diacritics = remove_diacritics(word, diacritics)
        if word_without_diacritics in corpus:
            if word in corpus[word_without_diacritics]:
                corpus[word_without_diacritics][word] += 1
            else:
                corpus[word_without_diacritics][word] = 1
        else:
            corpus[word_without_diacritics] = dict()
            corpus[word_without_diacritics][word] = 1



def create_corpus(URLs: list, diacritics: list) -> dict:
    """Creates a corpus from a list of URLs.
    Returns a dictionary with words without diacritics as keys. Values will also be dictionaries with words with diacritics as keys and their frequencies as values."
    """
    wikipedia.set_lang("cz")

    print("Creating a corpus from the most read articles in February 2023 at Czech Wikipedia...") 
    corpus = dict()
    URLs = URLs[:500] #500 articles could be enough for testing
    corpus_size = 0
    url_count = 1

    for URL in URLs:
        try:
            print(f"Processing page {url_count} out of total {len(URLs)}: " + URL)
            url_count += 1

            page = wikipedia.page(URL)
            content = page.content
            words = content.split()
            for word in words:
                process_word(word, corpus, diacritics)
            corpus_size += len(words)


        #except wiki disambiguation error - pick first option
        except wikipedia.exceptions.DisambiguationError as e:
            print("Disambiguation error: " + URL)
            page = wikipedia.page(e.options[0])
            print("Picked first option: " + e.options[0])
            content = page.content
            words = content.split()
            for word in words:
                process_word(word, corpus, diacritics)
            corpus_size += len(words)
            


        except wikipedia.exceptions.PageError as e:
            print("Invalid URL: " + URL)

    print("Corpus size with WIKI articles: " + str(corpus_size))

    #now process 15 Czech novels     
    #iterate over all files in the folder "novels"
    i  = 1
    for filename in os.listdir("novels"):
        novel_name = filename.strip("txt")
        print(f"Processing novel {novel_name} - {i} out of total 15...")
        i += 1
        with open("novels/" + filename, "r", encoding="utf-8") as f:
            #content = f.read()
            #words = content.split()
            #for word in words:
            #change the code so we dont load the whole file into memory
            #but instead process the file line by line
            for line in f:
                line = line.strip()
                words = line.split()
                for word in words:
                    process_word(word, corpus, diacritics)
            corpus_size += len(words)

    print(f"Corpus created, total number of words in processed articles is: {corpus_size}")
    return corpus






def restore_word(word: str, corpus: dict) -> str:
    wasUpper = word[0].isupper()
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

    word_cleared = word_lower.strip(",.!?()[]")
    word_lower = word.lower()

    
    if word_cleared in corpus:
        word_restored = max(corpus[word_cleared], key=corpus[word_cleared].get)
    else:
       return word

    #now restore the original form of the word
    if wasUpper:
        word_restored = word_restored.capitalize()
    if hadTripleDot:
        word_restored += "..."
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
        word_restored += "[" + word_restored
    if hadSquareBracketsRight:
        word_restored += "]"
    if hadRoundBracketsLeft:
        word_restored = "(" + word_restored
    if hadRoundBracketsRight:
        word_restored += ")"

    return word_restored


def restore_diacritics(text: str, corpus: dict) -> str:
    ##Replace non ascii letters with stars - replace two nonasci letters with one star using regex
    cleared_text = re.sub(r"[^\x00-\x7F][^\x00-\x7F]", "*", text)
    words = cleared_text.split()

    restored_text = ""

    for word in words:
        if "*" in word:
            restored_word = restore_word(word, corpus)
        else:
            restored_word = word
        restored_text += restored_word + " "
    return restored_text



URLs = load_URLs("top_articles.csv")
diacritics = ["á", "é", "ě", "í", "ó", "ú", "ů", "ý", "č", "ď", "ň", "ř", "š", "ť", "ž"]

#check if the current folder contains the json with the corpus called "corpus.json". 
#If yes, load it. If not, create it.

if os.path.exists("corpus.json"):
    with open("corpus.json", "r", encoding="utf-8") as f:
        corpus = json.load(f)
    print("Corpus loaded from disk.")
else:
    corpus = create_corpus(URLs, diacritics)
    with open("corpus.json", "w", encoding="utf-8") as f:
        json.dump(corpus, f, indent=2)
    print("Corpus saved to disk.")


#open the file dev.txt and read it
with open("eval.txt", "r", encoding="utf-8") as f:
    text = f.read()


print(restore_diacritics(text, corpus))