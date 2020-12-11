from MeterRhyme.PoemAnalyser.DBReaderFile import DBReader
from MeterRhyme.PoemAnalyser.Verse import *
from MeterRhyme.PoemAnalyser.MeterAnalyzer2 import MeterAnalyzer1
from MeterRhyme.PoemAnalyser.RhymeAnalyser2 import *


def main():
    dbreader = DBReader({
        'dbtype': 'sqlite',
        'path': '/Users/veram/PycharmProjects/MeterRhyme/database/accents_new.db'})
    dbreader.connect()
    acc = Accentuation(dbreader)
    meter = MeterAnalyzer1()
    rhyme = RhymeAnalyser()
    listOfStih = readText("inputText.txt")

    for Stih in listOfStih:
        StihData = acc.analyze2(Stih)
        print(StihData)
        meter.Hello(StihData)  # акцетуация
        strophica = rhyme.rhyme(Stih.getCleanLines(), StihData)
        print(strophica)
        # print(rhyme.checkTemplate(Template("aabab"),Stih.getCleanLines(),StihData))


main()
