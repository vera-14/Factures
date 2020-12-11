import sqlite3
from MeterRhyme.PoemAnalyser.DBReaderErrorFile import DBReaderError


class DBReader:
    def __init__(self, args):
        dbtypes = {'sqlite'}
        self.__dbtype = args['dbtype']
        try:
            if not self.__dbtype in dbtypes:
                raise (DBReaderError('wrong_dbtype'))

        except DBReaderError as err:
            print(err)

        if args['dbtype'] == 'sqlite':
            self.__init_sqlite(args)

    def __init_sqlite(self, args):
        self.__path = args['path']
        self.__conn = None
        self.__cursor = None

    def __dell__(self):
        self.disconnect()

    def connect(self):
        # better to ask password in
        # this function
        if self.__dbtype == 'sqlite':
            self.__connect_sqlite()

    def __connect_sqlite(self):
        self.__conn = sqlite3.connect(self.__path)
        self.__cursor = self.__conn.cursor()

    def disconnect(self):
        if self.__dbtype == 'sqlite':
            self.__disconnect_sqlite()

    def __disconnect_sqlite(self):
        if self.__conn:
            self.__conn.close()

        self.__conn = None
        self.__cursor = None

    def fetchall(self):
        if self.__dbtype == 'sqlite':
            return self.__fetchall_sqlite()

    def __fetchall_sqlite(self):
        try:
            if self.__cursor:
                return [row for row in self.__cursor]
            else:
                raise (DBReaderError('nocon_fetchall'))

        except DBReaderError as err:
            print(err)

    def search(self, word):
        if self.__dbtype == 'sqlite':
            return self.__execute_sqlite('''
            SELECT accent, word_type
            FROM words
            WHERE word_form = "%(word)s"''' % {
                'word': word})

    def __execute_sqlite(self, query):
        try:
            if self.__cursor:
                self.__cursor.execute(query)
            else:
                raise (DBReaderError('nocon_execute'))

        except DBReaderError as err:
            print(err)
