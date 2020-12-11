# -*- coding: utf-8 -*-
import collections
import itertools
from MeterRhyme.PoemAnalyser import DBReaderFile
from MeterRhyme.PoemAnalyser.Verse import *
from functools import reduce


class Template():
    """
    Преобразование бувенных строфик в множества рифмующихся строф
    """

    def __init__(self, string, name=None):
        if name is None:
            self.name = string
        else:
            self.name = name
        self.period = len(string)
        d1 = {}
        d2 = {}
        female = ['a', 'c', 'e']
        male = ['b', 'd', 'h', 'k']
        for i, c in enumerate(string):
            if c in female:
                if not c in d1:
                    d1[c] = [i]
                else:
                    d1[c].append(i)
            if c in male:
                if not c in d2:
                    d2[c] = [i]
                else:
                    d2[c].append(i)
        self.structureFemale = list(d1.values())
        self.structureMale = list(d2.values())


class RhymeAnalyser():
    def __init__(self):
        self.vowels = '''АЕЁИОУЫЭЮЯ'''
        self.redVowels = [
            ('А', 'Я'),
            ('О', 'Ё'),
            ('Э', 'Е'),
            ('У', 'Ю'),
            ('Ы', 'И'),
            ('О', 'Е')  # допущение
        ]
        self.similarEnds = [
            ('О', 'А'),
            ('А', 'Ы'),
            ('АЙ', 'О'),
            ('АХ', 'ЫХ'),
            ('Г', 'Х'),
            ('Г', 'К'),
            ('Т', 'Д'),
            ('З', 'С'),
            ('Б', 'П'),
            ('Е', 'И'),
            ('Е', 'Ы'),
            ('Е', 'ЬЕ'),
            ('ЕЙ', 'Е'),
            ('ЕЙ', 'И'),
            ('ЕЙ', 'ОЙ'),
            ('ЕЛ', 'ОЛ'),
            ('ЕШЬ', 'ИШЬ'),
            ('И', 'А'),
            ('И', 'Е'),
            ('И', 'ИЙ'),
            ('И', 'ОЙ'),
            ('И', 'Ы'),
            ('И', 'ЫЙ'),
            ('И', 'ЬЕ'),
            ('И', 'ЬИ'),
            ('И', 'ЬЯ'),
            ('ИВ', 'ОВ'),
            ('ИЙ', 'А'),
            ('ИЙ', 'Е'),
            ('ИЙ', 'ОЙ'),
            ('ИН', 'ЕН'),
            ('ИТ', 'ЕТ'),
            ('К', 'Г'),
            ('О', 'У'),
            ('ОЙ', 'А'),
            ('ОЙ', 'О'),
            ('ОЙ', 'ЫЙ'),
            ('ОМ', 'ЕМ'),
            ('ОМ', 'ИМ'),
            ('ОМ', 'ЫМ'),
            ('ОН', 'ЕН'),
            ('ОР', 'ЕР'),
            ('ТЬ', 'ДЬ'),
            ('У', 'ОЙ'),
            ('У', 'УЙ'),
            ('У', 'ЫЙ'),
            ('УГ', 'ОК'),
            ('Х', 'К'),
            ('Ы', 'ЕЙ'),
            ('Ы', 'О'),
            ('Ы', 'ОЙ'),
            ('Ы', 'У'),
            ('Ы', 'ЫЙ'),
            ('ЫЙ', 'А'),
            ('ЫЙ', 'О'),
            ('ЬЕ', 'ЬИ'),
            ('ЬИ', 'ЬЯ'),
            ('ЬЯ', 'ЬЕ'),
            ('Я', 'Е'),
            ('Я', 'И')
        ]
        self.templates = self.initTemplates()

    def initTemplates(self):
        '''
        Создание шаблонов, преобразование в списки рифмующихся строф
        :return: list
        '''
        result = []
        result.append(Template('bb'))
        result.append(Template('aabb'))
        result.append(Template('bbaa'))
        result.append(Template('aa'))
        result.append(Template('baabab'))
        result.append(Template('baaba'))
        result.append(Template('abababcc'))
        result.append(Template('bababadd'))
        result.append(Template('baabcdcd'))
        result.append(Template('abbaddcchh'))
        result.append(Template('babadd'))
        result.append(Template('babadccd'))
        result.append(Template('abaab'))
        result.append(Template('babaddchch'))
        result.append(Template('ababccddehhekk', "SuperOnegen"))
        result.append(Template('ababccb'))
        result.append(Template('abbccb'))
        result.append(Template('baabc'))
        result.append(Template('baab'))
        result.append(Template('babba'))
        result.append(Template('abbadd'))
        result.append(Template('ababa'))
        result.append(Template('bbaadd'))
        result.append(Template('ababccdd'))
        result.append(Template('bbadad'))
        result.append(Template('ababab'))
        # result.append(Template('ababcdcd'))
        result.append(Template('aabccb'))
        result.append(Template('babbacca'))
        result.append(Template('abab'))
        result.append(Template('babaa'))
        result.append(Template('baba'))
        result.append(Template('bababa'))
        result.append(Template('bbadda'))
        result.append(Template('abbaab'))
        result.append(Template('abba'))
        result.append(Template('aabccb'))
        result.append(Template('bbabaddcb'))
        result.append(Template('ababccdeed'))
        result.append(Template('babaddcc'))
        result.append(Template('aabab'))

        return result

    def rhyme(self, Stih, StihData):
        """
        Определяет максимально подходящий шаблон, процент схожести, либо выдает сообщение о свободной строфике
        :param Stih:
        :param StihData:
        :return: tuple or string
        """
        stat = {}
        for template in self.templates:
            if len(Stih.textList) % template.period == 0 or len(Stih.textList) % template.period == 2:  # 2 для рифмовки aabb
                stat[template.name] = self.checkTemplate(template, Stih, StihData)
        # print(stat)
        if stat == {}:
            FreeStrophica = (1.0, 'свободная')
            return FreeStrophica
        Procents = [(value, key) for key, value in stat.items()]
        if Procents != []:
            maxProcent = max([(value, key) for key, value in stat.items()])

            if maxProcent[0] < 0.8:
                FreeStrophica = (1.0, 'свободная')
                return FreeStrophica
            else:
                return maxProcent

    def functionij(self, template):
        """
        Разбивает элементы списков попарно
        Пример[[1,2,3]]->[[1,2],[2,3],[1,3]]
        :param template:
        :return:list
        """
        structureMF = [template.structureMale, template.structureFemale]
        allpairs = []
        for s in structureMF:
            pair = []
            for indexes in s:
                for i in indexes:
                    for j in indexes:
                        if i < j:
                            pair.append([i, j])
            allpairs.append(pair)
        return allpairs

    def checkTemplate(self, template, Stih, StihData):  # экземпляр класса Template
        '''
        Определяет точность совпадения проверяемого шаблона со стихом
        :param template:
        :param Stih:
        :param StihData:
        :return: float
        '''
        size = len(Stih.textList)
        count = 0
        good = 0
        structureMF = self.functionij(template)
        for s in structureMF:
            for [i, j] in s:
                n = 0
                a = lambda x: x + n * template.period
                while a(j) < size:
                    count += 1
                    if self.isLineRymes(Stih, StihData, a(i), a(j)):
                        good += 1
                    # else:
                    #   print(Stih.textList[i + n * template.period], Stih.textList[j + n * template.period])
                    n += 1

        # проверка на мужской тип рифмы

        if len(template.structureMale) > 0:
            Male = reduce(lambda x, y: x + y, template.structureMale)
            for i in Male:
                count += 1
                if self.isLineMale(StihData, i):
                    good += 1

        if len(template.structureFemale) > 0:
            Female = reduce(lambda x, y: x + y, template.structureFemale)
            for i in Female:
                count += 1
                if self.isLineFemale(StihData, i):
                    good += 1
        assert (count > 0)
        return good / count

    def isLineMale(self, StihData, index):
        return StihData[index][-1] != 0

    def isLineFemale(self, StihData, index):
        return not self.isLineMale(StihData, index)

    def isLineRymes(self, Stih, StihData, index1, index2):
        '''
        Проверка, что две строки рифмуются
        :param Stih:
        :param StihData:
        :param index1:
        :param index2:
        :return: bool
        '''
        if self.isSameRhymingEnds(Stih, StihData, index1, index2):
            if self.isSameAcc(StihData, index1, index2):
                return True
        return False

    def isSameAcc(self, StihData, index1, index2):
        """
        Проверка слов на одинаковые акценты
        :param StihData:
        :param index1:
        :param index2:
        :return: bool
        """
        return StihData[index1][-1] == StihData[index2][-1]

    def isSameRhymingEnds(self, Stih, StihData, index1, index2, MathesSize=2):
        """
        Проверяет совпадают  ли 2 окончания слов
        :param word1:isSameRhymingEnds
        :param word2:
        :param MathesSize:
        :return: bool
        """

        word1 = Stih.textList[index1][-1]
        if word1[-1].endswith('Ь'):
            word1 = word1[:-1]
        word2 = Stih.textList[index2][-1]
        if word2[-1].endswith('Ь'):
            word2 = word2[:-1]
        acc1 = StihData[index1][-1]  # ударение последнего слога в строке
        acc2 = StihData[index2][-1]
        sizeEnd = min(MathesSize, len(word1))
        lineEnd = word1[-sizeEnd:]
        if word2.endswith(lineEnd):
            return True
        else:

            if word1[-1] == word2[-1] and acc1 == acc2 == 1:  # моИ - любвИ #1 - значит ударный
                return True
            if word1[-1] == word2[-1] and word1[-1] not in self.vowels and acc1 == acc2 == 1:  # сиЯл - летАл
                for (end1, end2) in self.redVowels:  # для мною- землею TO DO
                    if (word1[-2] == end1 and word2[-2] == end2) or (word1[-2] == end2 and word2[-2] == end1):
                        return True
                return False
            return self.approximateRhymes(word1, word2)

    def approximateRhymes(self, word1, word2):
        """
        Ищет неточные рифмы через фонетические пары self.similarEnds
        :param word1:
        :param word2:
        :return: bool
        """
        for (end1, end2) in self.similarEnds:
            if len(word1) != len(end1) and len(word2) != len(end2):

                if word1.endswith(end1) and word2.endswith(end2) and word1[-len(end1) - 1] == word2[-len(end2) - 1]:
                    return True
            if len(word1) != len(end2) and len(word2) != len(end1):
                if word1.endswith(end2) and word2.endswith(end1) and word1[-len(end2) - 1] == word2[-len(end1) - 1]:
                    return True
                if (word1[:-1].endswith(end2) and word2[:-1].endswith(end1)) or (
                        word1[:-1].endswith(end1) and word2[:-1].endswith(end2)):
                    # print(end1,end2)#повар-говор
                    return True
        return False
