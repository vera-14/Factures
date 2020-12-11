#! /usr/bin/env python
# -*- coding: utf-8 -*-
import re
from bitarray import bitarray
from MeterRhyme.PoemAnalyser import DBReaderFile



class Verse():
    def __init__(self, name, textList):
        self.name = name
        self.textList = textList

    @staticmethod
    def getLine(line):
        '''
        Возвращает строку без знаков препинания и постронних символов
        :param line:
        :return: list
        '''
        return re.findall(r'[А-ЯЁ]+', re.sub(r'[<>]','', line).upper())

    @staticmethod
    def filterEmptyLines(lines):
        '''
        Возвращает список строк без пустых строк.
        :param lines:
        :return: list
        '''
        return [i for i in filter(lambda s: len(s) > 0, lines)]

    def getCleanLines(self):
        '''
        Возвращает экземпляр класса Verse от полей name - имя стиха, Verse.filterEmptyLines(ftext) - очищенные строки стиха от пункуации, и пустых строк
        :return: <class 'PoemAnalyzer.Verse.Verse'>
        '''
        ftext = [Verse.getLine(line) for line in self.textList]
        return Verse(self.name, Verse.filterEmptyLines(ftext))





class Accentuation:
    def __init__(self,dbreader):
        self.vowels = '''АЕЁИОУЫЭЮЯ'''
        self._dbreader = dbreader
        self.syllable_list = []
        self.line_syllables = []

    def analyze(self, Stih):
        '''
        Возвращает список списков акцентуации для всех строк не однозначностями
        :param Stih:
        :return: list
        '''
        numline = -1
        self.line_syllables = []
        for line in Stih.textList:

            wordArray = Verse.getLine(line)
            nsyll = 0
            first_syll = 0
            if len(wordArray) > 0 and wordArray[0] != '':
                self.line_syllables.append([])
                numline += 1

            for word in wordArray:
                if word != '':
                    first_syll = self.wordAnalyze(word, numline, first_syll)
        return self.line_syllables

    def analyze2(self,Stih):
        '''
        Возращает список списков акцентуации с решением неоднозначначности расстановки
        :param Stih:
        :return: list
        '''
        self.analyze(Stih)
        return self.xSolve()

    def xSolve(self):
        '''
        Решение проблем в неоднозначности расстановки ударений
        :return:list
        '''
        for i in range(len(self.line_syllables)):
            for j in range(len(self.line_syllables[i])):
                if self.line_syllables[i][j] == 'x':
                    if self.syllable_list[j][0] > self.syllable_list[j][1]:
                        self.line_syllables[i][j] = 0
                    else:
                        self.line_syllables[i][j] = 1
        return self.line_syllables

    def wordAnalyze(self, word, numline, first_syll):
        self._dbreader.search(word)
        info = self._dbreader.fetchall()
        #print("info", info)
        #print(word, info)
        nvowels = self.getNOfVowels(word)
        if nvowels == 0:
            return first_syll

        self.__syllable_count_control(numline, first_syll, nvowels)
        if len(info) == 0:
            for i in range(nvowels):
                self.syllable_list[first_syll + i][2] += 1
                self.line_syllables[numline][first_syll + i] = 'x'

            return first_syll + nvowels

        cbits = self.__getWordSyllableArray(info, nvowels)
        numofvar = sum(cbits)
        for i in range(len(cbits)):
            if numofvar > 1:
                if cbits[i] == 1:
                    self.syllable_list[first_syll + i][2] += 1
                    self.line_syllables[numline][first_syll + i] = 'x'
                else:
                    self.syllable_list[first_syll + i][0] += 1

            else:
                if cbits[i] == 1:
                    self.syllable_list[first_syll + i][1] += 1
                    self.line_syllables[numline][first_syll + i] = 1
                else:
                    self.syllable_list[first_syll + i][0] += 1
        return first_syll + nvowels

    def __getWordSyllableArray(self, info, nvowels):
        cbits = bitarray('0' * nvowels)
        for el in info:
            if el[0] != None:
                cbits[nvowels - el[0] - 1] = 1
        return cbits

    def __syllable_count_control(self, numline, first_syll, nvowels):
        while len(self.syllable_list) < first_syll + nvowels:
            self.syllable_list.append([0, 0, 0])

        while len(self.line_syllables[numline]) < first_syll + nvowels:
            self.line_syllables[numline].append(0)

    def getNOfVowels(self, word):
        word = word.upper()
        res = 0
        for ch in word:
            if ch in self.vowels:
                res += 1

        return res

def readText(name):
    '''
    Чтение файла, разбиение корпуса на стихи
    :param name:
    :return: list
    '''
    with open(name, 'r', encoding='utf-8') as poemFile:

        allpoem = []
        poem = []
        flag = False
        names = []
        for line in poemFile:
            if line[0:3] == '$$$':
                #print(line)
                #line = line.replace("\n", "")
                names.append(line)
                flag = True
                poem = []
            else:
                if line[0:3] == '***':
                    #print("poem:",poem)
                    p = Verse(names[0], poem)
                    allpoem.append(p)
                    names = []

                    #allpoem.append(poem)
                    flag = False
                else:
                    if flag:
                        poem.append(line)
        return allpoem

