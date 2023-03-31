# diacritics_restoration
A diacritics restoration python program for Czech text. Lab assingment to a NLP class at Charles University.


This program will restore diacritics of a Czech text using a mapping of words without diacritics to words with diacritics created from the most read articles in February 2023 at Czech Wikipedia and 15 Czech novels.
It follows these steps

1. Get URLs to Wikipedia articles from a wikimetrics csv file.
2. Process the Wikipedia articles and use them to create the mapping.
3. Download and process 15 Czech novels.
4. Use the mapping to restore the diacritics in the assigned text.
5. Evaluate the results using several metrics (Levenshtein, Jaro, Jaro-Winkler...)
