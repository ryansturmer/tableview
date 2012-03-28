import re, types, os

def listify(l):
    if isinstance(l, str) or isinstance(l, unicode):
        return [l]
    try: iter(l)
    except: l = [l]
    return list(l)

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
            s = file.readline(self).strip()
            if s == '':
                return []
            else:
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

class TableSelector(object):
    def __init__(self, source, mode):
        self.source = source
        self.mode = mode

    def __getitem__(self, item):
        if isinstance(item, slice):
            if self.mode == VectorView.ROW:
                start, stop, step = item.indices(len(self.source.row_index))
                return TableView(self.source.data, ([self.source.row_index[x] for x in range(start, stop, step)], self.source.col_index))
            else: # VectorView.COL    
                start, stop, step = item.indices(len(self.source.col_index))
                return TableView(self.source.data, (self.source.row_index, [self.source.col_index[x] for x in range(start, stop, step)]))
        else: # index, not slice
            if self.mode == VectorView.ROW:
                return VectorView(self.source.data, (self.source.row_index[item], self.source.col_index), type=VectorView.ROW)
            else:
                return VectorView(self.source.data, (self.source.col_index[item], self.source.row_index), type=VectorView.COL)

    def __len__(self):
        return len(self.source.row_index) if self.mode == VectorView.ROW else len(self.source.col_index)

    def __iter__(self):
        return iter([self[i] for i in range(len(self))])

            
class VectorView(object):
    ROW = 0
    COL = 1
    def __init__(self, src, index, type=ROW):
        self.data = src
        self.ordinal, self.index = index
        self.type = type

    def __len__(self):
        return len(self.index)

    def __iter__(self):
        return iter([self[i] for i in range(len(self))])

    def __getitem__(self, item):
        if self.type == VectorView.ROW:
            return self.data[self.ordinal][self.index[item]]
        else:
            return self.data[self.index[item]][self.ordinal]

    def __setitem__(self, a, b):
        if self.type == VectorView.ROW:
            self.data[self.ordinal][self.index[a]] = b
        else:
            self.data[self.index[a]][self.ordinal] = b

    def __str__(self):
        return repr(self)
    def __repr__(self):
        return "<%s:%d items>" % ('Row' if self.type == VectorView.ROW else 'Column', len(self))

class TableView(object):
    def __init__(self, src, index=None):
        self.data = src
        if not index:
            self.row_index = range(len(src))
            self.col_index = range(len(src[0]))
        else:
            self.row_index, self.col_index = index
    
    def __len__(self):
        return len(self.row_index)

    @property
    def rows(self):
        return TableSelector(self, mode=VectorView.ROW)

    @property
    def cols(self):
        return TableSelector(self, mode=VectorView.COL)

    def __iter__(self):
        return iter([self[r] for r in range(len(self))])
    def __getitem__(self, item):
        return self.rows[item]

    def strip_rows(self, selector):
        return self.select_rows(lambda x : not selector(x))
    
    def strip_cols(self, selector):
        return self.select_cols(lambda x : not selector(x))

    def select_rows(self, selector):
        new_row_index = []
        for i, row in enumerate(self.rows):
            if selector(row):
                new_row_index.append(self.row_index[i])
        return TableView(self.data, (new_row_index, self.col_index))

    def select_cols(self, selector):
        new_col_index = []
        for i, col in enumerate(self.cols):
            if selector(col):
                new_col_index.append(self.col_index[i])
        return TableView(self.data, (self.row_index, new_col_index))

    def pretty(self):
        if len(self) == 0:
            return "<Empty Table>"
        retval = ''
        col_widths = [0]*len(self[0])
        for row in self:
            for i, cell in enumerate(row):
                col_widths[i] = max(len(str(cell)), col_widths[i])
        lines = []
        for row in self:
            line = []
            for i,cell in enumerate(row):
                line.append(str(cell) + ' '*(col_widths[i]-len(str(cell))))
            lines.append(line)
        return '\n'.join([' '.join(line) for line in lines])

    def __str__(self):
        return repr(self)
    def __repr__(self):
        return "<Table:%d rows, %d columns>" % (len(self.row_index), len(self.col_index))

def load(filename):
    path, ext = os.path.splitext(filename)
    ext = ext.lower()
    if ext in ('tsv', 'tab', 'txt'):
        with TSVFile(filename) as fp:
            return TableView(fp.readlines())
    else:
        with CSVFile(filename) as fp:
            return TableView(fp.readlines())
