import re

class Delimiter(object):
    def __init__(self, file):
        self.file = file
        self.__current_line = []
        self.idx = 0
        self.cache = None

    def format(self, l):
        '''
        format takes a list of data and formats it as a row for the file
        '''
        raise NotImplementedError
    def unformat(self, s):
        '''
        unformat takes a row read from the file, and turns it into a list
        '''
        raise NotImplementedError

    def __iter__(self):
        if not self.cache:
            self.cache = self.file.readlines()
        return iter(self.cache)

    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()

    def readline(self):
        while True:
            s = self.file.readline()
            if not s:
                return ''
            else:
                s = s.strip('\r\n')
                retval = self.unformat(s)
                if retval != []:
                    return retval

    def readlines(self):
        retval = []
        while True:
            s = self.readline()
            if not s:
                break
            else:
                retval.append(s)
        return retval

    def read(self):
        try:
            retval = self.__current_line[self.__idx]
            self.__idx += 1
        except:
            self.__idx = 0
            self.__current_line = self.readline()
            if self.__current_line == []:
                return None

    def write(self, data):
	    self.file.write(self.format(data) + "\n")

    def writelines(self, lines):
        for line in lines:
            self.write(line)

class CSVData(Delimiter):

    def __init__(self, file):
        Delimiter.__init__(self, file)
        self._csvregex = re.compile(r',(?=(?:[^"]*"[^"]*")*(?![^"]*"))')

    def format(self, data):
        data = listify(data)
        retval = ''
        for d in data:
            if d == None: d = ''
            retval += ',"%s"' % unicode(d).replace('"', '""')

        return retval.lstrip(",")

    def unformat(self, data):
        if data.strip() == '':
            return []
        data = self._csvregex.split(data)
        for i in range(len(data)):
            try:
                if data[i][0] == '"' and data[i][-1] == '"':
                    data[i] = data[i].strip()[1:-1]
            except:
                pass
        return data

class SimpleDelimiter(Delimiter):
    def __init__(self, file, delimiter):
        self.__delimiter = delimiter
        Delimiter.__init__(self, file)

    def format(self, data):
        data = listify(data)
        return self.__delimiter.join(map(unicode, data))

    def unformat(self, data):
        if data.strip() == '':
            return []
        data = data.split(self.__delimiter)
        return data

class TSVData(SimpleDelimiter):
    def __init__(self, *args, **kwargs):
        SimpleDelimiter.__init__(self, '\t', *args, **kwargs)

class TextData(SimpleDelimiter):
    def __init__(self, *args, **kwargs):
        SimpleDelimiter.__init__(self, ' ', *args, **kwargs)


