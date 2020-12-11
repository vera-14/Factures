# -*- coding: utf-8 -*-
from ExcelExport import *
from JSONExport import *


def main():
    author = input()
    if author == 'Pushkin':
        ExcelPushkin()
        JSONPushkin()
    if author == 'Tolstoy':
        ExcelTolstoy()
        JSONTolstoy()


main()
