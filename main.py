# основной модуль

from interview import Interview
from speaker import Speaker
from interviewDataList import InterviewDataList
import ioFunc



# считывание всех интервью из файла и формирование структуры данных,
# ставящей каждому говорящему в соответствие все его интервью

data = InterviewDataList(ioFunc.read_interviews("Resources\\pushkin.txt"))

print("Количество спикеров:", len(data.speaker_list))
print("Общее количество текстов:", len(list(data.interview_list)))
print("Общее количество слов во всех текстах:",
      sum(map(lambda iv: len(iv.words_list), data.interview_list)))



# считывание списка диалектных слов из файла

dialect_words = list(ioFunc.read_dialect_words("Resources\\dialectal.txt"))

print("Количество диалектных слов в списке:", len(dialect_words))



# подсчет количества диалектных слов, употребленных говорящими в общем
# и в каждом интервью по отдельности;
# вывод общего количества диалектных слов во всех текстах

data.dialect_count(dialect_words)

print("Общее количество диалектных слов во всех текстах:",
      sum(map(lambda cont: sum(cont.dialect_list.values()), data.values())))



# запись данных в файлы

ioFunc.file_out(data, dialect_words, directory_name = "Result")

print("\nready\n")


        
