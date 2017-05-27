# модуль, содержащий определение класса, описывающего интервью

from speaker import Speaker
import re




# определение класса, описывающего интервью

class Interview():

    import re

    # регулярное выражение для поиска последовательности
    # символов, представляющих слово
    
    p_word = re.compile(r"(([\wа-яё]+)([-'])?)+",
                        re.IGNORECASE | re.MULTILINE | re.ASCII)

    # регулярное выражение для разделения слов по дефису, если после дефиса
    # не "то" или "нибудь"
 
    p_split = re.compile(r"(?!(?![\wа-яё']+-(то|нибудь))-(то|нибудь))-",
                         re.IGNORECASE | re.ASCII) 

    # регулярное выражение для предварительной очистки текста

    p_remove = re.compile(
            r"((?!\([^\)]*\n)(?:\([^\)]*[^\(]*\)))|"      
            r"((?!\[[^\]]*\n)(?:\[[^\]]*[^\[]*\]))|"
            r"( (?:[\wа-яё])\\)|(^(?:[\wа-яё])\")|(\"(?:[\wа-яё])\")|"
            r"([^\wа-яё](?:нрзб)[^\wа-яё])|"
            r"((?=[\wа-яё'-]+\=)(?:(?:(?:[\wа-яё]+)(?:[-'])?)+\=))",
            re.IGNORECASE | re.MULTILINE | re.ASCII)


    

    # инициализирующий метод класса
    
    def __init__(self, text, speaker =
                 Speaker(name = "default", age = None)):

        self.text = text
        self.speaker = speaker
        self.dialect_list = {}
        self.words_list = self.__get_words_list()




    # свойство, позволяющее получить количество словофором в тексте интервью

    @property
    def words_count(self):
        return len(self.words_list)




    # метод для получения списка словоформ, содержащихся в тексте интервью;
    # вызывается при инициализации внутри инициализирующего метода

    def __get_words_list(self):
        txt = Interview.p_remove.sub("  ", self.text.lower())

        words_not_split = list(map(lambda m: m.group(0),
                                   Interview.p_word.finditer(txt)))

        words_split = []
        for word in words_not_split:
            words_split += [w for w in Interview.p_split.split(word)
                            if (w and w != '')]

        return words_split




    # метод для подсчета количества диалектных слов в тексте интервью
    # (подсчет производится для каждого  диалектного слова по отдельности,
    # т.е. составляется словарь, в котором ключом является диалектное слово,
    # а значением - количество его вхождений в текст интервью);
    # если параметр recount установлен в True, то словарь диалектных
    # слов интервью предварительно очищается; если recount установлен в False,
    # то происходит пополнение словаря диалектных слов новыми словами,
    # встретившимися в переданном методу списке диалектных слов
    # (аргумент dialect_words_list)
    
    def dialect_count(self, dialect_words_list, recount = True):

        if recount:
            self.dialect_list.clear()
            

        for d_word in dialect_words_list:
            
            if d_word in self.dialect_list:
                continue

            d_word_low = d_word.lower()

            reg_exp = ''

            if (d_word_low[-1] == "'"):
                reg_exp = r"\b(" + d_word_low[:-1] + r")'"
            else:
                reg_exp = r"\b(" + d_word_low + r")(?!')\b"
                
            found_d_words = re.findall(reg_exp, '  '.join(self.words_list))

            if len(found_d_words):
                self.dialect_list[d_word] = len(found_d_words)



    


