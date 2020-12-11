# -*- coding: utf-8 -*-
from FormingDB import *
from MeterRhyme.PoemAnalyser.DBReaderFile import DBReader
from MeterRhyme.PoemAnalyser.MeterAnalyzer2 import MeterAnalyzer1
from MeterRhyme.PoemAnalyser.RhymeAnalyser2 import *
import json


def JSONInputPoem():
    dbreader = DBReader({
        'dbtype': 'sqlite',
        'path': '/Users/veram/PycharmProjects/Factures/MeterRhyme/database/accents_new.db'})
    dbreader.connect()
    acc = Accentuation(dbreader)
    meter = MeterAnalyzer1()
    rhyme = RhymeAnalyser()
    listOfStih = readText("/Users/veram/PycharmProjects/Factures/MeterRhyme/inputPoem.txt")

    n = 0
    for Stih in listOfStih:
        poemstihdata = acc.analyze2(Stih)
        poemmeter = meter.Hello(poemstihdata)
        poemstrophica = rhyme.rhyme(Stih.getCleanLines(), poemstihdata)
        n = n+1
        print('\nПараметры входного стихотворения:', Stih.name, poemstrophica[1], poemmeter, meter.stopCount())
        if poemstrophica[1] != 'свободная':

            sql1 = "SELECT * FROM samples WHERE strophica=? and meter=? and stopnost=?"
            cur.execute(sql1, (poemstrophica[1], poemmeter, meter.stopCount()))
            result = cur.fetchall()
            if result == []:
                print('Фактура не найдена')

            else:
                print('Номер соответствующей фактуры:', result[0][0])
                print('Пример строфы с такой же фактурой:\n', result[0][7], '\n', result[0][4], '\n', '№', result[0][5],
                      ',', result[0][6], 'год')
            outputdata = {"initial_parameters": {"strophica": poemstrophica[1],
                                                 "meter": poemmeter, "stopCount": meter.stopCount()},
                          "facture_number": result[0][0],
                          "facture_example": {"example_name": result[0][7], "example_strophe": result[0][4],
                                              "example_number": result[0][5], "example_year": result[0][6]}}
            #print(outputdata)
            with open("Output.json", "w") as write_file:
                json.dump(outputdata, write_file, indent=3)

def JSONPushkin():
    dbreader = DBReader({
        'dbtype': 'sqlite',
        'path': '/Users/veram/PycharmProjects/Factures/MeterRhyme/database/accents_new.db'})
    dbreader.connect()
    acc = Accentuation(dbreader)
    meter = MeterAnalyzer1()
    rhyme = RhymeAnalyser()
    listOfStih = readText("/Users/veram/PycharmProjects/Factures/MeterRhyme/pushkinCorpus.txt")

    n = 0
    for Stih in listOfStih:
        poemstihdata = acc.analyze2(Stih)
        poemmeter = meter.Hello(poemstihdata)
        poemstrophica = rhyme.rhyme(Stih.getCleanLines(), poemstihdata)
        n = n+1

        if poemstrophica[1] != 'свободная':
            print('\nПараметры входного стихотворения:', Stih.name, poemstrophica[1], poemmeter, meter.stopCount())

            sql1 = "SELECT * FROM samples WHERE strophica=? and meter=? and stopnost=?"
            cur.execute(sql1, (poemstrophica[1], poemmeter, meter.stopCount()))
            result = cur.fetchall()
            if result == []:
                print('Фактура не найдена')

            else:
                print('Номер соответствующей фактуры:', result[0][0])
                print('Пример строфы с такой же фактурой:\n', result[0][7], '\n', result[0][4], '\n', '№', result[0][5],
                      ',', result[0][6], 'год')
            outputdata = {"initial_parameters": {"strophica": poemstrophica[1],
                                                 "meter": poemmeter, "stopCount": meter.stopCount()},
                          "facture_number": result[0][0],
                          "facture_example": {"example_name": result[0][7], "example_strophe": result[0][4],
                                              "example_number": result[0][5], "example_year": result[0][6]}}
            #print(outputdata)
            with open("Output.json", "w", encoding='utf-8') as write_file:
                json.dump(outputdata, write_file)

def JSONTolstoy():
    dbreader = DBReader({
        'dbtype': 'sqlite',
        'path': '/Users/veram/PycharmProjects/MeterRhyme/database/accents_new.db'})
    dbreader.connect()
    acc = Accentuation(dbreader)
    meter = MeterAnalyzer1()
    rhyme = RhymeAnalyser()
    listOfStih = readText("/Users/veram/PycharmProjects/Factures/MeterRhyme/Tolstoy1.txt")
    n = 0
    for Stih in listOfStih:
        poemstihdata = acc.analyze2(Stih)
        poemmeter = meter.Hello(poemstihdata)
        poemstrophica = rhyme.rhyme(Stih.getCleanLines(), poemstihdata)
        n = n + 1

        if poemstrophica[1] != 'свободная':
            print('\nПараметры входного стихотворения:', Stih.name, poemstrophica[1], poemmeter, meter.stopCount())

            sql1 = "SELECT * FROM samples WHERE strophica=? and meter=? and stopnost=?"
            cur.execute(sql1, (poemstrophica[1], poemmeter, meter.stopCount()))
            result = cur.fetchall()
            if result == []:
                print('Фактура не найдена')

            else:
                print('Номер соответствующей фактуры:', result[0][0])
                print('Пример строфы с такой же фактурой:\n', result[0][7], '\n', result[0][4], '\n', '№', result[0][5],
                      ',', result[0][6], 'год')
            outputdata = {"initial_parameters": {"strophica": poemstrophica[1],
                                                 "meter": poemmeter, "stopCount": meter.stopCount()},
                          "facture_number": result[0][0],
                          "facture_example": {"example_name": result[0][7], "example_strophe": result[0][4],
                                              "example_number": result[0][5], "example_year": result[0][6]}}
            #print(outputdata)
            with open("Output.json", "w", encoding='utf-8') as write_file:
                json.dump(outputdata, write_file)
