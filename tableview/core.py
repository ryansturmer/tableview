import re, types, os

def listify(l):
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

from files import TSVFile, CSVFile
def load(filename):
    path, ext = os.path.splitext(filename)
    ext = ext.lower()
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