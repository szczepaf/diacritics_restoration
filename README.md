# diacritics_restoration
A diacritics restoration python program for Czech text. Lab assingment to a NLP class at Charles University.


This program will restore diacritics of a Czech text using a mapping of words without diacritics to words with diacritics created from the most read articles in February 2023 at Czech Wikipedia and 15 Czech novels.
It follows these steps

1. Download the data from Wikipedia
2. Process 500 Wikipedia articles and use them to create the mapping.
3. Download and process 15 Czech novels.
4. Use the mapping to restore the diacritics in the assigned text (Czech articles from a scientific website).
5. Evaluate the results using several metrics (Levenshtein, Jaro, Jaro-Winkler...)
6. Clear training data


The results are following:
Used metrics are: Lavenshtein distance, Jaro similarity, Jaro-Winkler similarity, and accuracy as the ratio of total correct words.



---

**BEFORE AND AFTER RESTORATION METRICS - DEV DATA**

| Metric | Before restoration | After restoration |
| --- | --- | --- |
| Levenshtein distance | 3546 | 434 |
| Jaro similarity | 0.755 | 0.848 |
| Jaro-Winkler similarity | 0.853 | 0.909 |
| Accuracy | 0.484 | 0.884 |

**EVAL DATA METRICS**

| Metric | Before restoration | After restoration |
| --- | --- | --- |
| Levenshtein distance | 13195 | 2167 |
| Jaro similarity | 0.739 | 0.826 |
| Jaro-Winkler similarity | 0.844 | 0.895 |
| Accuracy | 0.501 | 0.868 |

---



More information: https://ufal.mff.cuni.cz/courses/npfl124#assignments
