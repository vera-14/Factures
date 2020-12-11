# -*- coding: utf-8 -*-
from collections import Counter
from itertools import combinations
from MeterRhyme.PoemAnalyser.Verse import *


class MeterAnalyzer1():
    def __init__(self):
        self._ri = []
        self._k = []
        self._r = []
        self._dr = []
        self._condNum = None
        self._subCondNum = None
        self.line_syllables = None


        self.masks = {
            "ямб": [0, 1],
            "хорей": [1, 0],
            "дактиль": [1, 0, 0],
            "амфибрахий": [0, 1, 0],
            "анапест": [0, 0, 1]
        }

        self.resultCodes = {
            1: {
                1: "Вольный", #"неравностопный метрический стих"
                2: "Вольный", #"неравностопный метрический стих"
                3: "Вольный", #"неравностопный метрический стих"
                0: "дисметрический стих",
            },
            2: {
                1: "э. д. ",

                #1: "неурегулированный {k}-акцентный тонический стих",
                #2: "4-сложный {k}-акцентный тактовик",
                #3: "3-сложный {k}-акцентный тактовик",
                #4: "3-сложный {k}-акцентный дольник",
                #5: "2-сложный {k}-акцентный дольник",

            },
            3: {
                0: "неурегулированный {K}-стопный силлабо-тониеский стих",
            },
            4: {
                1: "хорей",
                2: "ямб",
                3: "дактиль",
                4: "амфибрахий",
                5: "анапест",
                6: "пэон-1",
                7: "пэон-2",
                8: "пэон-3",
                9: "пэон-4",
                10: "пэнтон-1",
                11: "пэнтон-2",
                12: "пэнтон-3",
                13: "пэнтон-4",
                14: "пэнтон-5",
                0: "многосложный размер",
            },
        }

    def Hello(self, StihData):
        """
        Определение метра и стопности
        :param StihData:
        :return:
        """
        self.line_syllables = StihData
        self.countLineStats() # параметры
        self.analyzeStats(0.9) #статистика по параметрам
        #Классификация по условиям
        if self._condNum == 1:
            #print("TEST")
            res = self.__analyzeCondNum1()

        if self._condNum == 2:
            #print("TEST1")
            res = self.__analyzeCondNum2()

        if self._condNum == 4:
            #print("TEST2")
            res = self.__analyzeCondNum4()
        if self._condNum == 5:
            #print("TEST3")
            res = self.__analyzeCondNum5()
        return res
            #print(res, self.stopCount(), 'из hello')

    def stopCount(self):
        '''
        Считает параметры: число слогов в строке, лист межакцентных расстояний для ст
        :return:
        '''
        allAcc = self.line_syllables
        allLen = [len(i) for i in allAcc]
        p = Counter(allLen).most_common()
        percMostCommon = p[0][1] / len(allLen)
        if percMostCommon >= 0.4:
            length = p[0][0]
            res = self.__analyzeCondNum5()
            mask = self.masks[res]
            return length // len(mask)
            #return Counter(mask * (length // len(mask)) + mask[:(length % len(mask))])[1]

    def __analyzeCondNum1(self):
        tcmbs = combinations(self._dr, 2)
        diffs = [abs(x[0] - x[1]) for x in tcmbs]
        flag2 = all([x % 2 == 0 for x in diffs])
        flag3 = all([x % 3 == 0 for x in diffs])
        flag5 = all([x % 5 == 0 for x in diffs])
        if flag2 or flag3 or flag5:
            self._subCondNum = 1
            res = (self.resultCodes[1][1], self.__analyzeCondNum5())
            return res[1]
        else:
            self._subCondNum = 2
            res = (self.__analyzeCondNum5(),  self.stopCount())
            return res[0]

    def __calcBooleanPCT(self, flags):
        lst = Counter(flags).most_common()
        if lst[0][0]:
            return float(lst[0][1]) / len(flags)
        else:
            if len(lst) <= 1:
                return float(lst[0][1]) / len(flags)
            return float(lst[1][1]) / len(flags)

    def __analyzeCondNum2(self):
        flags = [max(lst[1: self._k[n]]) > 4 for n, lst in enumerate(self._ri)]
        pct1 = self.__calcBooleanPCT(flags)
        if pct1 != 0:
            res = ('tut2', self.resultCodes[2][1])
            return res[1]
        '''
        flags = [0 < max(lst[1: self._k[n]]) < 4 for n, lst in enumerate(self._ri)]
        pct2 = self.__calcBooleanPCT(flags)
        if pct2 != 0:
            print("tut3",self.resultCodes[2][2])
        flags = [-1 < max(lst[1: self._k[n]]) < 3 for n, lst in enumerate(self._ri)]
        pct3 = self.__calcBooleanPCT(flags)
        if pct3 != 0:
            print("tut4",self.resultCodes[2][3])
        flags = [0 < max(lst[1: self._k[n]]) < 3 for n, lst in enumerate(self._ri)]
        pct4 = self.__calcBooleanPCT(flags)
        if pct4 != 0:
            print("tut5",self.resultCodes[2][4])

        flags = [-1 < max(lst[1: self._k[n]]) < 2 for n, lst in enumerate(self._ri)]
        pct5 = self.__calcBooleanPCT(flags)
        if pct5 != 0:
            print("tut6",self.resultCodes[2][5])
        lst = [pct1, pct2, pct3, pct4, pct5]
        self._subCondNum = lst.index(max(lst)) + 1
        '''
    def __analyzeCondNum4(self):
        # предполагаем, что слогов больше 2
        self._subCondNum = 0
        for i in range(1, 5):
            for j in range(i + 1):
                self._subCondNum += 1
                if (self._ri[0][1] == i and
                        self._ri[0][0] == j):
                    res = (self.stopCount(), self.resultCodes[4][self._subCondNum])
                    return res[1]


    def __analyzeCondNum5(self):

        errors = {}
        for key in self.masks:
            pattern = self.masks[key]
            errors[key] = 0
            for line in self.line_syllables:
                for i in range(len(line)):
                    errors[key] += int(line[i] != pattern[i % len(pattern)])
        return min(errors, key=errors.get)

    def countLineStats(self):
        '''
        Подсчет параметров, k- ударные слоги, dr -общее число слого минус клаузула, ri - междуакцентный интервал, r - общее число слогов
        :return:
        '''
        self._k = []
        self._dr = []
        self._r = []
        self._ri = []
        for i in range(len(self.line_syllables)):
            self._ri.append([])
            ri = 0
            r = len(self.line_syllables[i])
            self._r.append(r)
            self._k.append(0)
            for j in range(r):
                if self.line_syllables[i][j] == 1:
                    self._k[i] += 1
                    self._ri[i].append(ri)
                    ri = 0
                else:
                    ri += 1

            self._ri[i].append(ri)
            self._dr.append(self._r[i] - self._ri[i][-1])
        #print(self._k)
        #print(self._dr)
        #print(self._r)
        #print(self._ri)
    def analyzeStats(self, acc):
        """
        Анализ статистики параметров
        :param acc:
        :return:
        """
        pct_dr = float(Counter(self._dr).most_common()[0][1]) / len(self._dr)
        pct_k = float(Counter(self._k).most_common()[0][1]) / len(self._k)
        lst_ri = []
        for line in self._ri:
            lst_ri += line

        best_acc = -1.
        pct_ri = float(Counter(lst_ri).most_common()[0][1]) / len(lst_ri)
        self._condNum = None
        if pct_dr < acc and pct_k < acc:
            self._condNum = 1
            best_acc = pct_dr * pct_k

        if pct_dr < acc and pct_k >= acc and pct_ri < acc:
            tmp_acc = pct_dr * pct_k * pct_ri
            if tmp_acc > best_acc:
                self._condNum = 2
                best_acc = tmp_acc

        if pct_dr < acc and pct_k >= acc and pct_ri >= acc:
            tmp_acc = pct_dr * pct_k * pct_ri
            if tmp_acc > best_acc:
                self._condNum = 3
                best_acc = tmp_acc

        if pct_dr >= acc and pct_k >= acc and pct_ri >= acc:
            tmp_acc = pct_dr * pct_k * pct_ri
            if tmp_acc > best_acc:
                self._condNum = 4
                best_acc = tmp_acc

        if pct_dr >= acc and pct_k < acc and pct_ri < acc:
            tmp_acc = pct_dr * pct_k * pct_ri
            if tmp_acc > best_acc:
                self._condNum = 5
                best_acc = tmp_acc

        if self._condNum == None and acc > 0.1:
            nacc = 0.9 * acc
            #print('[!] Change accuracy limit to {}.'.format(nacc))
            self.analyzeStats(nacc)
