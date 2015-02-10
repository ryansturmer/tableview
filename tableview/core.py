import re, types, os

__title__ = 'tableview'
__version__ = '0.1.0'
__author__ = 'Ryan Sturmer'
__license__ = 'MIT'
__copyright__ = 'Copyright 2012 Ryan Sturmer'
__docformat__ = 'restructuredtext'

def listify(l):
    '''
    Turn any non-string, non-unicode iterable into a list.
    '''
    if isinstance(l, str) or isinstance(l, unicode):
        return [l]
    try: iter(l)
    except: l = [l]
    return list(l)

class TableSelector(object):
    '''
    TableSelector used internally for iterating over rows and columns
    '''
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
    
    def __delitem__(self, item):
        if self.mode == VectorView.ROW:
            del self.source.row_index[item]
        else:
            del self.source.col_index[item]
                
    def __len__(self):
        return len(self.source.row_index) if self.mode == VectorView.ROW else len(self.source.col_index)

    def __iter__(self):
        return iter([self[i] for i in range(len(self))])

            
class VectorView(object):
    '''
    View of a single row or column of data
    '''
    ROW = 0
    COL = 1
    def __init__(self, src, index, type=ROW):
        self.data = src
        self.ordinal, self.index = index
        self.type = type

    def pretty(self):
        '''
        Return a pretty printed string of this vector
        '''
        return (' ' if self.type == VectorView.ROW else '\n').join(map(str, self))

    def __len__(self):
        return len(self.index)

    def __iter__(self):
        return iter([self[i] for i in range(len(self))])

    def __getitem__(self, item):
        if isinstance(item, slice):
            start, stop, step = item.indices(len(self.index))
            new_index = [self.index[i] for i in range(start, stop, step)]
            return VectorView(self.data, (self.ordinal, new_index), self.type)
        else:
            if self.type == VectorView.ROW:
                j = self.index[item]
                try:
                    return self.data[self.ordinal][j]
                except:
                    return None

            else:
                i = self.index[item]
                try:
                    return self.data[i][self.ordinal]
                except:
                    return None

    def __setitem__(self, a, b):
        if self.type == VectorView.ROW:
            self.data[self.ordinal][self.index[a]] = b
        else:
            self.data[self.index[a]][self.ordinal] = b

    @property
    def empty(self):
        return not reduce(lambda x,y : x or y, self, False)
    
    def convert(self, f, quiet=True):
        for idx, value in enumerate(self):
            try:
                self[idx] = f(value)
            except:
                if not quiet:
                    raise

    def __str__(self):
        return repr(self)
    def __repr__(self):
        return "<%s:%d items>" % ('Row' if self.type == VectorView.ROW else 'Column', len(self))

class TableView(object):
    '''
    Represents a view of a tabular data source.
    '''
    def __init__(self, src, index=None):
        self.data = src
        if not index:
            self.row_index = range(len(src))
            self.col_index = range(max(map(len, src)))
        else:
            self.row_index, self.col_index = index
   
    def __len__(self):
        return len(self.row_index)

    def _split(self, selector, f):
        f = f or (lambda x : x.empty)
        start = None
        ranges = []
        for i,row in enumerate(selector):
            if f(row):
                if start != None:
                    ranges.append((start, i))
                    start = None
            else:
                if start == None:
                    start = i

        if start != None:
            ranges.append((start,i+1))
        return [selector[slice(*r)] for r in ranges]

    def split_rows(self, f=None):
        return self._split(self.rows, f)

    def split_cols(self, f=None):
        return self._split(self.cols, f)
    
    def split(self,f=None):
        return self.split_rows(f)

    def pick_rows(self, *x):
        return TableView(self.data, (x, self.col_index))

    def pick_cols(self, *x):
        return TableView(self.data, (self.row_index, x))
 
    @property
    def dataset(self):
        import tablib
        d = tablib.Dataset()
        for row in self:
            d.append(row)
        return d

    @property
    def csv(self):
        return self.dataset.csv

    @property
    def json(self):
        return self.dataset.json

    @property
    def rows(self):
        return TableSelector(self, mode=VectorView.ROW)

    @property
    def cols(self):
        return TableSelector(self, mode=VectorView.COL)

    @property
    def raw(self):
        return [list(row) for row in self]

    def __iter__(self):
        return iter([self[r] for r in range(len(self))])
    def __getitem__(self, item):
        return self.rows[item]
    def __delitem__(self, i):
        del self.row_index[i]

    def convert(self, f, quiet=True):
        for row in self:
            row.convert(f, quiet)

    def strip_rows(self, selector):
        '''
        Return a new TableView without the rows that match the provided selector.
        Parameters:
          selector - A function that takes a single argument, a table row, and returns 
                     True for a row that is to be stripped, and False otherwise.
        '''
        return self.select_rows(lambda x : not selector(x))
    
    def strip_cols(self, selector):
        '''
        Return a new TableView without the rows that match the provided selector.
        Parameters:
          selector - A function that takes a single argument, a table column, and returns 
                     True for a column that is to be stripped, and False otherwise.
        '''
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
        '''
        Return a pretty printed string of this table.
        '''
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
                s = str(cell) if (cell != None) else ''
                line.append(s + ' '*(col_widths[i]-len(s)))
            lines.append(line)
        return '\n'.join([' '.join(line) for line in lines])

    def __str__(self):
        return repr(self)
    def __repr__(self):
        return "<Table:%d rows, %d columns>" % (len(self.row_index), len(self.col_index))

from files import TSVFile, CSVFile
def load(filename):
    '''
    Load a table from a text file on disk and return a TableView that represents it.
    Function uses the file extension to determine the filetype:
    .tsv .tab .txt = Tab-Delimited Text
         Otherwise = Comma-Delimited Text
    None will be substituted for all missing values.
    '''
    path, ext = os.path.splitext(filename)
    ext = ext.strip('.').lower()
    if ext in ('tsv', 'tab', 'txt'):
        with TSVFile(filename) as fp:
            source_data = fp.readlines()
    else:
        with CSVFile(filename) as fp:
            source_data = fp.readlines()

    maxlen = 0
    for row in source_data:
        maxlen = max(len(row), maxlen)

    for row in source_data:
        row.extend([None]*(maxlen-len(row)))

    return TableView(source_data)
