# dialectCount
The program counts dialect words used by speakers from a prepared wordlist in the interviews. The result of the program is the file Speaker_data.csv which contains information about each speaker (year of birth, amount of data by the interviewee, the number of dialect words used, the total number of words encountered in the texts of his interview and dialect ratio (ratio of the number of dialect words to the total number of words used by the speaker)) and the file Frequency_dict.csv (frequency dictionary of dialect words). The frequency dictionary contains information on the frequency of each dialect word (the total number of uses by all the speakers, the number of speakers that used a particular word, and a list of these speakers). Also, for each speaker the program creates a folder containing files with more detailed information on each speaker and the texts of each interview (including lists of dialect words used with the number of uses for each dialect word and a list of all the words used).
# Installation
The program requires Python version 3.5.1 or later.

Installing the program is done by copying the contents of the repository.

The Resources folder contains files needed to work: interview texts (pushkin.txt) and a list of dialect words (dialectal.txt). Generated files appear in the <i>Result</i> folder (needs to be created manually)

The program is launched by executing the main.py file.
