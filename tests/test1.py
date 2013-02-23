d = [['Name', 'Age', 'Drink', 'Color'],
     ['Ryan', 30, 'Tea', 'Purple'],
     ['Michael', 31, 'Coffee', 'Blue'],
     ['Keith', 40, 'Diet Coke', 'Maroon'],
     ['Brent', 26, 'Coffee', 'Blue'],
     ['Craig', 35, 'Coffee', 'Red']]

import tableview

t = tableview.TableView(d)

print "Full Table"
print t.pretty()

t2 = t.select_cols(lambda x : x[0] != 'Age')

print "\nAge Removed:"
print t2.pretty()

del t2[0]

print "\nHeaders Removed:"
print t2.pretty()

del t2.cols[1]

print "\nMichael Removed:"
print t2.pretty()
