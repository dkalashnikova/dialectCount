# модуль, содержащий определение класса InterviewDataList,
# описывающего структуру данных для хранения интервью,
# поставленных в соответствие говорящим,
# и словарей диалектных слов, встретившихся в речи говорящих

from interview import Interview
from speaker import Speaker
from collections import namedtuple




# определение класса InterviewDataList (для удобства унаследован от
# встроенного класса словаря (dict))

class InterviewDataList(dict):

    # именованный кортеж, описывающий содержимое ячейки значения
    # определяемой структуры данных (ключом будет являться именованный кортеж,
    # описывающий говорящего (Speaker))
    
    SpeakerContent = namedtuple("SpeakerContent",
                                ["interview_list", "dialect_list"])



    # инициализирующий метод класса
    
    def __init__(self, interview_list = []):
        super(InterviewDataList, self).__init__()
        for iv in interview_list:
            self.add_interview(iv)
        


    # метод для добавления интервью в ячейку структуры данных,
    # соответствующей говорящему, давшему это интервью (при этом,
    # если для каких-то интервью уже произведен подсчет диалектных слов,
    # то происходит дополнение словаря диалектных слов соответствующего говорящего)

    def add_interview(self, interview):
        if interview.speaker in self:
            speaker_cont = self[interview.speaker]
            speaker_cont.interview_list.append(interview)

            for word in interview.dialect_list:
                if word in speaker_cont.dialect_list:
                    speaker_cont.dialect_list[word] += \
                                            interview.dialect_list[word]
                else:
                    speaker_cont.dialect_list[word] = \
                                            interview.dialect_list[word]

        else:
            self[interview.speaker] = \
                self.SpeakerContent([interview],
                                    interview.dialect_list.copy())




    # свойство для получения всех интервью, содержащихся в структуре данных

    @property
    def interview_list(self):
        for speaker_cont in self.values():
            for interview in speaker_cont.interview_list:
                yield interview


    # свойство для получения всех говорящих, содержащихся в структуре данных
    
    @property
    def speaker_list(self):
        return list(self.keys())




    # метод для формирования словарей встретившихся диалектных слов
    # для всех интервью и говорящих, содержащихся в структуре данных
    # (назначение аргумента recount такое же, как и для метода
    # dialect_count класса Interview)

    def dialect_count(self, dialect_words_list, recount = True,
                      speakers = None):
        
        if speakers == None:
            speakers = self.keys()


        N = 0
        
        for speaker in speakers:

            if recount:
                self[speaker].dialect_list.clear()


            for iv in self[speaker].interview_list:

                iv.dialect_count(dialect_words_list, recount)

                
                for word in iv.dialect_list:
                    
                    if word in self[speaker].dialect_list:
                        self[speaker].dialect_list[word] += iv.dialect_list[word]
                    else:
                        self[speaker].dialect_list[word] = iv.dialect_list[word]


                N += 1
                print("Обработано интервью: ", N)





