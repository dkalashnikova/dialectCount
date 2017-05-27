# модуль, содержащий функции чтения и записи в файлы

from speaker import Speaker
from interview import Interview



# функция для чтения файла, содержащего список диалектных слов

def read_dialect_words(filename):
    with open(filename, "rt", encoding = "utf8") as fin:
        for line in fin:
            word = line.strip(' \n')
            if word != '':
                yield word





# функция для считывания интервью из файла;
# последовательно для каждого интервью возвращает кортеж,
# содержащий текст интервью и именованный кортеж, описывающий говорящего

def read_interviews(filename):

    import re
    
    # регулярное выражение, служащее для определения года рождения говорящего
    # из его обозначения

    p_age = re.compile(r"(?:\D(\d{4,4})(?:(?:\b)|(?:\D+\d{0,3})))$",
                       re.IGNORECASE)


    # вспомогательная функция, принимающая строковое обозначение говорящего
    # и возвращающая кортеж из обозначения говорящего и года его рождения,
    # если он указан в обозначении; если год не указан, вторым элементом
    # возвращаемого кортежа является None
    
    def speaker_parse(speaker):
        m = p_age.findall(speaker)
        str_age = m[0] if m else None
        name = speaker
        return (name, int(str_age) if str_age else None)



    with open(filename, "rt", encoding = "utf8") as fin:

        text = ""
        speaker = None

        N = 0
        
        for line in fin:

            N += 1
            string = line.strip(' ')

            
            if (string == '\n'):
                continue

            elif string.startswith("FILE"):
                if (speaker != None) and text != "":
                    yield Interview(text, Speaker(*speaker_parse(speaker)))
                    text = ""
                    speaker = None

            elif string.startswith("SPEAKER"):
                if speaker != None:
                    yield Interview(text, Speaker(*speaker_parse(speaker)))
                    text = ""
                    speaker = None
                speaker = string.partition("SPEAKER:")[2].strip(' \n')
                    
            else:
                text += string


        else:
            if text != "":
                yield Interview(text, Speaker(*speaker_parse(speaker)))
                





# функция, осуществляющая завершающую обработку полученных данных
# и запись обработанных данных в файлы

def file_out(data, dialect_words_list, directory_name = "Result"):

    import os
    import csv
    

    # формирование списка словарей, содержащего данные обработки
    # для каждого спикера, для последующей записи в csv файл,
    # содержащий информацию по всем говорящим
    
    sp_data = [{"code name": sp.name,
                "возраст": str(sp.age),
                "количество текстов": str(len(data[sp].interview_list)),
                "количество диалектных слов": str(sum(
                    data[sp].dialect_list.values())),
                "общее количество слов": str(sum(
                    map(lambda iv: len(iv.words_list),
                        data[sp].interview_list))),
                "коэффициент диалектности": str(sum(
                    data[sp].dialect_list.values()) / sum(
                        map(lambda iv: len(iv.words_list),
                            data[sp].interview_list)))
                }
               for sp in data]

    with open(directory_name + "\\Speaker_data.csv", "wt") as fout:
        cout = csv.DictWriter(fout,
                              fieldnames = ["code name",
                                            "возраст",
                                            "количество текстов",
                                            "количество диалектных слов",
                                            "общее количество слов",
                                            "коэффициент диалектности"],
                              dialect = "excel",
                              delimiter = ';')
        cout.writeheader()
        cout.writerows(sp_data)




    from collections import defaultdict
    from itertools import chain

    # формирование частотного словаря диалектных слов
    
    freq_dict = defaultdict(lambda: [0, []])

    for w_fr_sp in chain(*tuple(map(lambda it: map(lambda i: (i, it[0].name),
                                                   it[1].dialect_list.items()),
                                    data.items()))):
        freq_dict[w_fr_sp[0][0]][0] += w_fr_sp[0][1]
        if w_fr_sp[1] not in freq_dict[w_fr_sp[0][0]][1]:
            freq_dict[w_fr_sp[0][0]][1].append(w_fr_sp[1])

    for word in dialect_words_list:
        freq_dict[word][0] += 0
        
    
    # преобразование частотного словаря в список словарей для записи
    # частотонго словаря в csv файл
    
    freq_dict_csv = [{"слово": word,
                      "количество употреблений": freq_dict[word][0],
                      "количество спикеров, употребляющих слово":
                          len(freq_dict[word][1]),
                      "спикеры": ' | '.join(freq_dict[word][1])
                      }
                     for word in sorted(list(freq_dict.keys()))]


    with open(directory_name + "\\Frequency_dict.csv", "wt") as fout:
        cout = csv.DictWriter(fout,
                              fieldnames = ["слово",
                                            "количество употреблений",
                                            "количество спикеров, употребляющих слово",
                                            "спикеры"],
                              dialect = "excel",
                              delimiter = ';')
        cout.writeheader()
        cout.writerows(freq_dict_csv)
        



    # создание папки для каждого говорящего и запись общего файла говорящего,
    # содержащего обобщенную информацию о нем и файлы для каждого его интервью
    
    for speaker in data:
    
        dir_name = \
                 directory_name + "\\" + \
                 ((str(speaker.age) + '__') if speaker.age else '') + \
                 speaker.name
        os.mkdir(dir_name)
        

        text_num = 0
        for iv in data[speaker].interview_list:

            text_num += 1
            with open(dir_name + "\\text_" + str(text_num) + r".txt", "wt",
                      encoding = "utf8") as fout:

                fout.write("Количество диалектных слов:\n" +
                           str(sum(iv.dialect_list.values())) + '\n' +
                           "\nОбщее количество слов:\n" +
                           str(len(iv.words_list)) + '\n\n' +
                           "\n--------------------------------------\n" +
                           "\nСписок диалектных слов:\n\n" +
                           '\n'.join(list(map(lambda dw: dw + ":  " +
                                              str(iv.dialect_list[dw]),
                                              iv.dialect_list))) +
                           '\n\n' +
                           "\n--------------------------------------\n" +
                           "\nОбщий список слов (с повторами):\n\n" +
                           '\n'.join(iv.words_list) + '\n\n' +
                           "\n--------------------------------------\n" +
                           "\nТекст #" + str(text_num) + ":\n\n" +
                           iv.text + '\n')


                           
        with open(dir_name + "\\Speaker_info" + r".txt", "wt",
                  encoding = "utf8") as fout:

            fout.write("Год рождения:\n" + str(speaker.age) + '\n' +
                       "\nCode name:\n" + speaker.name + '\n\n' +
                       "\n--------------------------------------\n" +
                       "\nКоличество диалектных слов:\n" +
                       str(sum(data[speaker].dialect_list.values())) +
                       "\n\nОбщее количество слов:\n" +
                       str(sum(map(lambda iv: len(iv.words_list),
                               data[speaker].interview_list))) + '\n\n' +
                       "\n--------------------------------------\n" +
                       "\nСписок диалектных слов:\n\n" +
                       '\n'.join(list(map(lambda dw: dw + ":  " +
                                          str(data[speaker].dialect_list[dw]),
                                          data[speaker].dialect_list))) +
                       '\n\n' +
                       "\n--------------------------------------\n" +
                       "\nОбщий список слов (с повторами):\n\n" +
                       ''.join(map(lambda iv: '\n'.join(iv.words_list),
                                   data[speaker].interview_list)) + '\n')





