import sqlite3 as lite
import sys

class Logger(object):
    def __init__(self, type, config):
        if type == 'csv':
            self.logger = CsvLogger(config['filename'])
        if type == 'sqlite':
            self.logger = SQLiteLogger(config)
        if type == 'none':
            self.logger = NoLogger()

    def log(self, logItems):
        self.logger.log(logItems)

class NoLogger(object):
    def log(self, logItems):
        pass

class CsvLogger(object):
    def __init__(self, filename):
        self.filename = filename

    def log(self, logItems):
        print logItems.values()
        with open(self.filename, 'a') as logfile:
            logfile.write('%s\n' % ','.join(str(item) for item in logItems.values()))

class SQLiteLogger(object):
    def __init__(self, config):
        self.filename = config['filename']
        self.style = config['style']

        if self.style != 'ping' and self.style != 'speed':
            raise Exception('Unknown Table Type %s' % self.style)

    def log(self, logItems):
        try:
            con = lite.connect(self.filename)
            if self.style == 'ping':
                con.execute('CREATE TABLE IF NOT EXISTS Ping(ID INTEGER PRIMARY KEY, Date TEXT, Success TEXT);')
                con.execute('INSERT INTO Ping(Date,Success) VALUES (?,?);', (logItems['date'], logItems['success']))
            elif self.style == 'speed':
                con.execute('CREATE TABLE IF NOT EXISTS Speed(ID INTEGER PRIMARY KEY, Date TEXT, Upload REAL, Download REAL);')
                con.execute('INSERT INTO Speed(Date, Upload, Download) VALUES (?,?,?)', (logItems['date'], logItems['upload'], logItems['download']))
            else:
                raise Exception('Unknown Table Type %s' % self.style)

            con.commit()
        except lite.Error, e:
            if con:
                con.rollback()
            print 'Error %s:' % e.args[0]
            sys.exit(1)

        finally:
            if con:
                con.close()



