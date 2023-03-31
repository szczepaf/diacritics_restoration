# diacritics_restoration
A diacritics restoration python program for Czech text. Lab assingment to a NLP class at Charles University.


This program will restore diacritics of a Czech text using a mapping of words without diacritics to words with diacritics created from the most read articles in February 2023 at Czech Wikipedia and 15 Czech novels.
It follows these steps

1. Download the data from Wikipedia
2. Process 500 Wikipedia articles and use them to create the mapping.
3. Download and process 15 Czech novels.
4. Use the mapping to restore the diacritics in the assigned text.
5. Evaluate the results using several metrics (Levenshtein, Jaro, Jaro-Winkler...)
6. Clear training data
