
class DBReaderError(Exception):
    def __init__(self, key):
        self.key = key
        self.messages = {
            'wrong_dbtype' : '''
            [!] Database type is wrong.
            ''',
            'nocon_execute' : '''
        [!] Error in execute(self, text) function:
        No connection.
            ''',
            'nocon_fetchall' : '''
        [!] Error in fetchall(self) function:
        No connection.
            '''}
        
    def __str__(self):
        return self.messages[self.key]

    
