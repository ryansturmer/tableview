import pytest, tableview

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

def test_create():
    table = tableview.TableView(data)
    assert len(table) == 12
    assert len(table.rows) == 12
    assert len(table.cols) == 4

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
