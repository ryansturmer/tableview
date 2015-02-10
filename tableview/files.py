import re

class DelimitedFile(file):
    def __init__(self, *args, **kwargs):
        file.__init__(self, *args, **kwargs)
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
            self.cache = self.readlines()
        return iter(self.cache)

    def readline(self):
        while True:
            s = file.readline(self)
            if not s:
                return ''
            else:
                s = s.strip()
                retval = self.unformat( s)
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
	    file.write(self, self.format(data) + "\n")

    def writelines(self, lines):
        for line in lines:
            self.write(line)

class CSVFile(DelimitedFile):

    def __init__(self, *args, **kwargs):
        DelimitedFile.__init__(self, *args, **kwargs)
        self._csvregex = re.compile(r',(?=(?:[^"]*"[^"]*")*(?![^"]*"))')

    def format(self, data):
        data = listify(data)
        retval = ''
        for d in data:
            if d == None: d = ''
            retval += ',"%s"' % str(d).replace('"', '""')

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

class SimpleDelimitedFile(DelimitedFile):
    def __init__(self, delimiter, *args, **kwargs):
        self.__delimiter = delimiter
        DelimitedFile.__init__(self, *args, **kwargs)

    def format(self, data):
        data = listify(data)
        return self.__delimiter.join(map(str, data))

    def unformat(self, data):
        if data.strip() == '':
            return []
        data = data.split(self.__delimiter)
        return data

class TSVFile(SimpleDelimitedFile):
    def __init__(self, *args, **kwargs):
        SimpleDelimitedFile.__init__(self, '\t', *args, **kwargs)

class TextFile(SimpleDelimitedFile):
    def __init__(self, *args, **kwargs):
        SimpleDelimitedFile.__init__(self, ' ', *args, **kwargs)


