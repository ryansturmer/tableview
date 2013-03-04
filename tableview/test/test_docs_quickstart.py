import tableview, pytest

data = [['Name', 'Age', 'Drink', 'Color'],
       ['Ryan', 30, 'Tea', 'Purple'],
       ['Michael', 31, 'Coffee', 'Blue'],
       ['Keith', 40, 'Diet Coke', 'Maroon'],
       ['Brent', 26, 'Coffee', 'Blue'],
       ['Craig', '??', 'Turquoise', 'Red']]

def test_pretty_printing():
    table = tableview.TableView(data)
    s = table.pretty()
    s_reference = 'Name    Age Drink     Color \nRyan    30  Tea       Purple\nMichael 31  Coffee    Blue  \nKeith   40  Diet Coke Maroon\nBrent   26  Coffee    Blue  \nCraig   ??  Turquoise Red   '
    assert s == s_reference

def test_rows_and_columns():
    table = tableview.TableView(data)
    assert list(table[0]) == data[0]
    assert list(table.rows[0]) == data[0]
    assert list(table.cols[0]) == [row[0] for row in data]

def test_removing_data_from_a_view():
    table = tableview.TableView(data)
    del table.rows[0]
    assert list(table[0]) == list(data[1])
    del table.cols[0]
    assert len(table.cols) == len(data[0]) - 1
    assert len(table.rows) == len(data) - 1
    assert list(table.cols[1]) == [row[2] for row in data[1:]]

def test_selecting_rows_and_columns():
    table = tableview.TableView(data)
    selection = table.select_rows(lambda row : row[2] == 'Coffee')
    assert len(selection) == 2
    assert list(selection[0]) == data[2]
    assert list(selection[1]) == data[4]
    selection = table.select_cols(lambda col : col[0] in ('Name', 'Drink'))
    assert len(selection.cols) == 2
    assert list(selection.cols[0]) == [row[0] for row in data]
    assert list(selection.cols[1]) == [row[2] for row in data]

def test_stripping_rows_and_columns():
    table = tableview.TableView(data)
    selection = table.strip_rows(lambda row : row[2] == 'Coffee')
    assert list(selection[0]) == data[0]
    assert list(selection[1]) == data[1]
    assert list(selection[2]) == data[3]

