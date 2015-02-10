import tableview
import pytest

data = [['Number', 'Word', 'Decimal', 'Hex'],
        [0,'zero','0','0x%x' % 0],
        [1,'one','1','0x%x' % 1],
        [2,'two','2','0x%x' % 2],
        [3,'three','3','0x%x' % 3],
        [4,'four','4','0x%x' % 4],
        [5,'five','5','0x%x' % 5],
        [6,'six','6','0x%x' % 6],
        [7,'seven','7','0x%x' % 7],
        [8,'eight','8','0x%x' % 8],
        [9,'nine','9','0x%x' % 9],
        [10,'ten','10','0x%x' % 10]]

data2 = [[1,2,3,4,5],[],[6,7,8,9,10],[11,12,13,14,15],[],[16,17,18,19,20],[21,22,23,24,25],[26,27,28,29,30]]

def test_create():
    table = tableview.TableView(data)
    assert len(table) == 12
    assert len(table.rows) == 12
    assert len(table.cols) == 4

def test_convert():
    table = tableview.TableView(data)
    number_strings = table.cols[2]
    number_strings.convert(int)
    assert list(number_strings) == ['Decimal'] + list(range(11))

def test_column_index():
    table = tableview.TableView(data)
    
    # Positive index
    numbers = table.cols[0]
    assert list(numbers) == ['Number'] + list(range(11))

    # Negative index
    hexes = table.cols[-1]
    assert list(hexes) == ['Hex'] + ['0x%x' % i for i in range(11)]

    # Out of bounds
    with pytest.raises(IndexError):
        invalid = table.cols[4]

def test_row_selection():
    table = tableview.TableView(data)

    zero = table.rows[1]
    zero_direct = table[1]

    assert list(zero) == list(zero_direct)

    assert list(zero) == data[1]

def test_split_rows():
    # Sanity check incoming data before mangling
    table = tableview.TableView(data2)
    assert len(table) == 8

    subtables = table.split_rows()
    
    # Correct number and length of subtables
    assert len(subtables) == 3
    assert len(subtables[0]) == 1
    assert len(subtables[1]) == 2
    assert len(subtables[2]) == 3
    
    # Check first row data of each subtable
    assert list(subtables[0][0]) == data2[0]
    assert list(subtables[1][0]) == data2[2]
    assert list(subtables[2][0]) == data2[5]

